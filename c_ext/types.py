from six import iteritems
import copy
import pycparser.c_ast as c_ast


class TypeInfo:
    def __init__(self):
        self.quals = list()

    def clone(self):
        copied = copy.copy(self)
        copied.quals = copy.deepcopy(self.quals)
        return copied

    def safe_cast(self, expression, type_info):
        return None

    def to_ast(self):
        return None

    @staticmethod
    def make_safe_cast(expression, type_info):
        return expression.type_info.safe_cast(expression, type_info)

    @staticmethod
    def is_compatible(src_type_info, dst_type_info):
        from .expression import Expression
        expression = Expression(src_type_info)
        return TypeInfo.make_safe_cast(expression, dst_type_info) is not None


class ScalarTypeInfo(TypeInfo):
    def __init__(self, name):
        TypeInfo.__init__(self)
        self.name = name

    def __str__(self):
        return '%s%s' % ((' '.join(self.quals) + ' ') if self.quals else '', self.name)

    def safe_cast(self, expression, type_info=None):
        from .expression import ConstantExpression
        if isinstance(type_info, ScalarTypeInfo):
            return expression
        if isinstance(expression, ConstantExpression) and isinstance(type_info, PtrTypeInfo):
            if expression.value == '0':
                return expression
        return None

    def to_ast(self, verbose=True):
        node = c_ast.IdentifierType(self.name.split(' '))
        if self.quals:
            node = c_ast.TypeDecl(None, self.quals, node)
        return node


class StructTypeInfo(TypeInfo):
    next_id = 0

    def __init__(self, kind, name):
        TypeInfo.__init__(self)
        self.kind = kind
        self.name = name
        self.parent = None
        self.scope = None
        self.ast_node = None
        self.id = StructTypeInfo.next_id
        StructTypeInfo.next_id += 1

    def __str__(self):
        return '%s%s%s(%s)' % (
            (' '.join(self.quals) + ' ') if self.quals else '',
            self.kind,
            ' %s' % self.name if self.name is not None else '',
            self.scope
        )

    def to_ast(self, verbose=True, node=None):
        node = c_ast.Struct(self.ast_node.name, list() if verbose else None, self.ast_node.coord)\
            if node is None else node
        if verbose and (self.scope is not None):
            if self.parent is not None:
                assert not self.parent.quals
                self.parent.to_ast(True, node)
            for decl in self.ast_node.decls:
                if isinstance(decl, c_ast.Decl):
                    if isinstance(decl.type, c_ast.FuncDecl):
                        continue
                node.decls.append(decl)
        if self.quals:
            node = c_ast.TypeDecl(None, self.quals, node, node.coord)
        return node

    def make_methods_decls(self):
        methods_decls = list()
        for name, type in iteritems(self.scope.symbols):
            if isinstance(type, VariableInfo):
                type_info = type.type
                if isinstance(type_info, FuncTypeInfo):
                    assert self.name is not None
                    full_name = '%s_%s' % (self.name, name)
                    func_type_decl = type_info.to_ast(False)
                    func_type_decl.type.declname = full_name
                    func_type_decl.args.params.insert(0,
                        c_ast.Typename(None, list(),
                            c_ast.PtrDecl(list(),
                                c_ast.TypeDecl(None, list(), c_ast.Struct(self.name, None))
                            )
                        )
                    )
                    methods_decls.append(c_ast.Decl(full_name, list(), list(), list(),
                                                    func_type_decl, None, None))
        return methods_decls

    def safe_cast(self, expression, type_info):
        return None

    def inherited_from(self, type_info):
        if isinstance(type_info, StructTypeInfo):
            if self.id == type_info.id:
                return True
            if self.parent is not None:
                return self.parent.inherited_from(type_info)
        return False


class ArrayTypeInfo(TypeInfo):
    def __init__(self, base_type, dim):
        TypeInfo.__init__(self)
        self.base_type = base_type
        self.dim = dim

    def __str__(self):
        return 'Array(%s, %s)' % (self.base_type, self.dim)

    def safe_cast(self, expression, type_info):
        if isinstance(type_info, PtrTypeInfo):
            tmp = PtrTypeInfo(self.base_type)
            return tmp.make_safe_cast(expression, type_info)
        return None

    def to_ast(self, verbose=True):
        return c_ast.PtrDecl(list(), self.base_type.to_ast(verbose))


class FuncTypeInfo(TypeInfo):
    def __init__(self, return_type, args_types):
        TypeInfo.__init__(self)
        self.return_type = return_type
        self.args_types = args_types

    def __str__(self):
        return 'Func(%s) -> %s' % (', '.join(['%s' % type for type in self.args_types]), self.return_type)

    def safe_cast(self, expression, type_info):
        if isinstance(type_info, PtrTypeInfo):
            if isinstance(type_info.base_type, ScalarTypeInfo) and (type_info.base_type.name == 'void'):
                return expression
            func_info = type_info.base_type
            if isinstance(func_info, FuncTypeInfo):
                if TypeInfo.is_compatible(self.return_type, func_info.return_type):
                    compatible = True
                    i = 0
                    while i < len(func_info.args_types):
                        if i >= len(self.args_types):
                            compatible = False
                            break
                        if self.args_types[i] is None:
                            break
                        if not TypeInfo.is_compatible(func_info.args_types[i], self.args_types[i]):
                            compatible = False
                            break
                        i += 1
                    if compatible:
                        from .expression import CastExpression
                        dst_type_decl = c_ast.Typename(None, type_info.quals, type_info.to_ast(False))
                        return CastExpression(expression, type_info, c_ast.Cast(dst_type_decl, expression.ast_node))
        return None

    def to_ast(self, verbose=True):
        return_type_decl = self.return_type.to_ast(verbose)
        if not isinstance(return_type_decl, c_ast.TypeDecl):
            return_type_decl = c_ast.TypeDecl(None, list(), return_type_decl)
        node = c_ast.FuncDecl(c_ast.ParamList(list()), return_type_decl)
        for arg_type in self.args_types:
            arg_type_decl = arg_type.to_ast(verbose)
            arg_type_decl = c_ast.Typename(None, list(), arg_type_decl)
            node.args.params.append(arg_type_decl)
        return node


class PtrTypeInfo(TypeInfo):
    def __init__(self, base_type, quals=list()):
        TypeInfo.__init__(self)
        self.quals = quals
        self.base_type = base_type

    def __str__(self):
        return '%sPtr(%s)' % ((' '.join(self.quals) + ' ') if self.quals else '', self.base_type)

    def safe_cast(self, expression, type_info):
        if isinstance(type_info, ScalarTypeInfo) and (type_info.name == '_Bool'):
            return expression
        if isinstance(type_info, PtrTypeInfo):
            base_type = type_info.base_type
            if isinstance(base_type, ScalarTypeInfo) and (base_type.name == 'void'):
                return expression
            if isinstance(self.base_type, ScalarTypeInfo) and (self.base_type.name == 'void'):
                return expression
            if isinstance(self.base_type, FuncTypeInfo):
                return self.base_type.safe_cast(expression, type_info)
            if isinstance(base_type, StructTypeInfo) and isinstance(self.base_type, StructTypeInfo):
                if base_type.id == self.base_type.id:
                    return expression
                if self.base_type.inherited_from(base_type):
                    from .expression import CastExpression
                    dst_type_decl = base_type.to_ast(False)
                    if not isinstance(dst_type_decl, c_ast.TypeDecl):
                        dst_type_decl = c_ast.TypeDecl(None, list(), dst_type_decl)
                    return CastExpression(expression, type_info,
                                          c_ast.Cast(c_ast.PtrDecl(type_info.quals, dst_type_decl),
                                                                                    expression.ast_node))
            if TypeInfo.is_compatible(self.base_type, base_type):
                return expression
        return None

    def to_ast(self, verbose=True):
        base_type_decl = self.base_type.to_ast(verbose)
        if not isinstance(base_type_decl, c_ast.TypeDecl):
            base_type_decl = c_ast.TypeDecl(None, list(), base_type_decl)
        return c_ast.PtrDecl(self.quals, base_type_decl)


class VariableInfo:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return 'Variable(%s, %s)' % (self.name, self.type)
