from collections import OrderedDict
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
        self.has_vtable = False
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
        node = c_ast.Struct(self.name, list() if verbose else None, self.ast_node.coord if verbose else None)\
            if node is None else node
        if verbose and (self.scope is not None):
            if self.parent is not None:
                assert not self.parent.quals
                self.parent.to_ast(True, node)
                if self.parent.has_vtable:
                    self.has_vtable = True
            for decl in self.ast_node.decls:
                if isinstance(decl, c_ast.Decl):
                    if 'static' in decl.storage:
                        continue
                    if isinstance(decl.type, c_ast.FuncDecl):
                        if 'virtual' in decl.storage:
                            if not self.has_vtable:
                                self.has_vtable = True
                        continue
                node.decls.append(decl)
        if self.has_vtable and node.decls is not None:
            vtable_decl = c_ast.Decl(
                '__vtable__', list(), list(), list(),
                c_ast.PtrDecl(list(), c_ast.TypeDecl(
                    '__vtable__', ['const'],
                    c_ast.Struct('%s_VTable' % self.name, None)
                )),
                None, None
            )
            if (self.parent is not None) and self.parent.has_vtable:
                i = 0
                while i < len(node.decls):
                    if node.decls[i].name == '__vtable__':
                        node.decls[i] = vtable_decl
                        break
                    i += 1
            else:
                node.decls.append(vtable_decl)
        node = c_ast.TypeDecl(None, self.quals, node, node.coord)
        return node

    def make_methods_decls(self, vtable=False):
        methods_decls = list()
        virtual_methods_decls = list()
        for name, symbol in iteritems(self.scope.symbols):
            if isinstance(symbol, VariableInfo):
                type_info = symbol.type
                if isinstance(type_info, FuncTypeInfo):
                    assert self.name is not None
                    virtual = 'virtual' in symbol.storage
                    if vtable and not virtual:
                        continue
                    full_name = '%s_%s' % (self.name, name)
                    func_type_decl = type_info.to_ast(False)
                    func_type_decl.type.declname = full_name
                    if 'static' not in symbol.storage:
                        func_type_decl.args.params.insert(0,
                            c_ast.Typename(None, list(),
                                c_ast.PtrDecl(list(),
                                    c_ast.TypeDecl(None, list(), c_ast.Struct(self.name, None))
                                )
                            )
                        )
                    elif len(func_type_decl.args.params) == 0:
                        func_type_decl.args = None
                    if symbol.init is None:
                        methods_decls.append(c_ast.Decl(full_name, list(), list(), list(),
                                                        func_type_decl, None, None, symbol.coord))
                    if virtual:
                        func_type_decl = c_ast.FuncDecl(
                            func_type_decl.args,
                            c_ast.TypeDecl(name, func_type_decl.type.quals, func_type_decl.type.type)
                        )
                        func_type_decl = c_ast.PtrDecl(list(), func_type_decl)
                        virtual_methods_decls.append(c_ast.Decl(name, list(), list(), list(),
                                                                func_type_decl, None, None, symbol.coord))
                elif 'static' in symbol.storage:
                    full_name = '%s_%s' % (self.name, name)
                    type_decl = type_info.to_ast(False)
                    tmp = type_decl
                    while not isinstance(tmp, c_ast.TypeDecl):
                        tmp = tmp.type
                    if isinstance(tmp.type, c_ast.FuncDecl):
                        tmp = tmp.type
                        while not isinstance(tmp, c_ast.TypeDecl):
                            tmp = tmp.type
                        assert isinstance(tmp, c_ast.TypeDecl)
                        tmp.declname = full_name
                    else:
                        tmp.declname = full_name
                    methods_decls.append(c_ast.Decl(full_name, list(), ['extern'], list(),
                                                    type_decl, None, None, symbol.coord))
                symbol.attrs.add('member')
        if self.parent is not None:
            virtual_methods_decls = self.parent.make_methods_decls(True) + virtual_methods_decls
        if (len(virtual_methods_decls) > 0) and not vtable:
            virtual_decls = OrderedDict()
            for decl in virtual_methods_decls:
                virtual_decls[decl.name] = decl
            vtable_decl = c_ast.Struct('%s_VTable' % self.name, [decl for name, decl in iteritems(virtual_decls)])
            if self.parent is None:
                vtable_decl.decls.insert(
                    0,
                    c_ast.Decl(
                        '__parent__', list(), list(), list(),
                        c_ast.PtrDecl(list(), c_ast.TypeDecl(
                            '__parent__', ['const'],
                            c_ast.IdentifierType(['void'])
                        )),
                        None, None
                    )
                )
            else:
                vtable_decl.decls.insert(
                    0,
                    c_ast.Decl(
                        '__parent__', list(), list(), list(),
                        c_ast.PtrDecl(list(), c_ast.TypeDecl(
                            '__parent__', ['const'],
                            c_ast.Struct('%s_VTable' % self.parent.name, None)
                        )),
                        None, None
                    )
                )
            vtable_decl.decls.insert(
                1,
                c_ast.Decl(
                    '__name__', list(), list(), list(),
                    c_ast.PtrDecl(list(), c_ast.TypeDecl(
                        '__name__', ['const'],
                        c_ast.IdentifierType(['char'])
                    )),
                    None, None
                )
            )
            vtable_name = '%s_vtable' % self.name
            vtable_decl = c_ast.TypeDecl(vtable_name, ['const'], vtable_decl)
            vtable_decl = c_ast.Decl(
                vtable_name, list(), ['extern'], list(), vtable_decl, None, None,
                self.ast_node.coord
            )
            methods_decls.insert(0, vtable_decl)
        return methods_decls if not vtable else virtual_methods_decls

    def fix_method_call(self, node, expression):
        from .expression import MemberExpression
        assert isinstance(expression, MemberExpression)
        symbol = self.scope.symbols.get(expression.member_name)
        if symbol is not None:
            assert isinstance(symbol, VariableInfo)
            if not isinstance(symbol.type, FuncTypeInfo):
                return
            full_name = '%s_%s' % (self.name, expression.member_name)
            if ('virtual' not in symbol.storage) or (expression.type == '.'):
                node.name = c_ast.ID(full_name)
            else:
                node.name = c_ast.StructRef(
                    c_ast.StructRef(expression.ast_node.name, '->', c_ast.ID('__vtable__')),
                    '->', c_ast.ID(expression.member_name)
                )
            if 'static' not in symbol.storage:
                if node.args is None:
                    node.args = c_ast.ExprList(list())
                this_type_info = PtrTypeInfo(self)
                this_ptr = expression.value
                if not isinstance(this_ptr.type_info, PtrTypeInfo):
                    from .expression import UnaryExpression
                    this_ptr = UnaryExpression('&', this_ptr, c_ast.UnaryOp('&', this_ptr.ast_node))
                this_ptr = TypeInfo.make_safe_cast(this_ptr, this_type_info)
                node.args.exprs.insert(0, this_ptr.ast_node)
        elif self.parent is not None:
            self.parent.fix_method_call(node, expression)
        elif isinstance(node.name, c_ast.ID):
            symbol = self.scope.find_symbol(node.name.name)
            assert isinstance(symbol.type, FuncTypeInfo)
            if node.args is None:
                node.args = c_ast.ExprList(list())
            this_type_info = symbol.type.args_types[0]\
                if len(symbol.type.args_types) > 0 else expression.value.type_info
            this_ptr = expression.value
            if not isinstance(this_ptr.type_info, PtrTypeInfo):
                from .expression import UnaryExpression
                this_ptr = UnaryExpression('&', this_ptr, c_ast.UnaryOp('&', this_ptr.ast_node))
            this_ptr = TypeInfo.make_safe_cast(this_ptr, this_type_info)
            node.args.exprs.insert(0, this_ptr.ast_node)

    def fix_member_access(self, node):
        assert isinstance(node, c_ast.StructRef)
        if isinstance(node.field.name, tuple):
            if node.field.name[0] != self.name:
                if self.parent is not None:
                    return self.parent.fix_member_access(node)
            member_name = node.field.name[-1]
            full_name = '%s_%s' % (self.name, member_name)
            return c_ast.ID(full_name)
        else:
            member_name = node.field.name
        symbol = self.scope.symbols.get(member_name)
        if symbol is not None:
            if 'static' in symbol.storage:
                full_name = '%s_%s' % (self.name, member_name)
                return c_ast.ID(full_name)
        elif self.parent is not None:
            return self.parent.fix_member_access(node)
        return node

    def fix_member_implementation(self, node, name):
        assert isinstance(node, c_ast.Decl)
        if isinstance(node.type, c_ast.FuncDecl):
            symbol = self.scope.find_symbol(name)
            assert isinstance(symbol, VariableInfo)
            if 'static' not in symbol.storage:
                if node.type.args is None:
                    node.type.args = c_ast.ParamList(list())
                node.type.args.params.insert(0, c_ast.Decl('this', list(), list(), list(),
                    c_ast.PtrDecl(['const'],
                        c_ast.TypeDecl('this', list(), c_ast.Struct(self.name, None))
                    ),
                None, None))

    def fix_func_implementation(self, node, name, ast_transformer):
        assert isinstance(node, c_ast.FuncDef)
        if name == 'construct':
            if node.body.block_items is None:
                node.body.block_items = list()
            vtable_name = '%s_vtable' % self.name
            vtable_symbol = ast_transformer.scope.find_symbol(vtable_name)
            if vtable_symbol is not None:
                if 'extern' in vtable_symbol.storage:
                    vtable_symbol = None
            if vtable_symbol is None:
                vtable_values = OrderedDict()
                if (self.parent is None) or not self.parent.has_vtable:
                    vtable_values['__parent__'] = c_ast.Constant('int', '0')
                else:
                    vtable_values['__parent__'] = c_ast.UnaryOp('&', c_ast.ID('%s_vtable' % self.parent.name))
                vtable_values['__name__'] = c_ast.Constant('string', '\"%s\"' % self.name)
                class_list = [self]
                tmp = self.parent
                while tmp is not None:
                    class_list.append(tmp)
                    tmp = tmp.parent
                class_list.reverse()
                for cls in class_list:
                    for key, value in iteritems(cls.scope.symbols):
                        if isinstance(value, VariableInfo):
                            if isinstance(value.type, FuncTypeInfo):
                                if 'virtual' in value.storage:
                                    if value.init is None:
                                        vtable_values[key] = c_ast.ID('%s_%s' % (cls.name, key))
                                    else:
                                        vtable_values[key] = value.init.ast_node
                ast_transformer.scheduled_decls.insert(
                    0,
                    c_ast.Decl(
                        vtable_name, ['const'], list(), list(),
                        c_ast.TypeDecl(vtable_name, ['const'], c_ast.Struct('%s_VTable' % self.name, None)),
                        c_ast.InitList([value for key, value in iteritems(vtable_values)]),
                        None,
                        node.coord
                    )
                )
            i, j = 0, 0
            while i < len(node.body.block_items):
                n = node.body.block_items[i]
                if isinstance(n, c_ast.FuncCall):
                    if isinstance(n.name, c_ast.StructRef):
                        if isinstance(n.name.name, c_ast.ID):
                            if n.name.name.name == 'this':
                                if isinstance(n.name.field, c_ast.ID):
                                    if isinstance(n.name.field.name, tuple):
                                        if len(n.name.field.name) == 2:
                                            if n.name.field.name[1] == 'construct':
                                                j = i + 1
                    elif isinstance(n.name, c_ast.ID):
                        if isinstance(n.name.name, tuple):
                            if len(n.name.name) == 2:
                                if n.name.name[1] == 'construct':
                                    j = i + 1
                i += 1
            node.body.block_items.insert(
                j + 1,
                c_ast.Assignment(
                    '=',
                    c_ast.StructRef(c_ast.ID('this'), '->', c_ast.ID('__vtable__')),
                    c_ast.UnaryOp('&', c_ast.ID(vtable_name))
                )
            )

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
    def __init__(self, return_type, args_types, args=None):
        TypeInfo.__init__(self)
        self.return_type = return_type
        self.args_types = args_types
        self.args = args

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
            if arg_type is not None:
                arg_type_decl = arg_type.to_ast(verbose)
                arg_type_decl = c_ast.Typename(None, list(), arg_type_decl)
            else:
                arg_type_decl = c_ast.EllipsisParam()
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
        return c_ast.PtrDecl(self.quals, base_type_decl)


class VariableInfo:
    def __init__(self, name, type, storage, coord=None):
        self.name = name
        self.type = type
        self.storage = storage
        self.init = None
        self.attrs = set()
        self.coord = coord

    def __str__(self):
        return 'Variable(%s, %s)' % (self.name, self.type)
