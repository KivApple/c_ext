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

    def to_decl(self):
        return None

    @staticmethod
    def make_safe_cast(expression, type_info):
        if expression.type_info:
            return expression.type_info.safe_cast(expression, type_info)
        return expression

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

    def to_decl(self):
        node = c_ast.IdentifierType(self.name.split(' '))
        node = c_ast.TypeDecl(None, self.quals, node)
        return node


class StructTypeInfo(TypeInfo):
    VTABLE_TYPE_NAME_FMT = '%s_VTable'
    VTABLE_NAME_FMT = '%s_vtable'
    VTABLE_LINK_NAME = '__vtable'
    VTABLE_PARENT_LINK_NAME = '__parent'
    VTABLE_NAME_LINK_NAME = '__name'

    next_id = 0

    def __init__(self, kind, name, ast_transformer):
        TypeInfo.__init__(self)
        self.ast_transformer = ast_transformer
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

    def make_this_ptr(self):
        return c_ast.Decl(
            'this',
            list(), list(), list(),
            c_ast.PtrDecl(
                ['const'],
                c_ast.TypeDecl(
                    'this',
                    list(),
                    c_ast.Struct(self.name, None)
                )
            ),
            None, None
        )

    def make_method_prototype(self, decl):
        assert isinstance(decl, c_ast.Decl)
        name = '%s_%s' % (self.name, decl.name)
        decl = copy.deepcopy(decl)
        decl.name = name
        tmp = decl.type
        while hasattr(tmp, 'type'):
            if isinstance(tmp, c_ast.TypeDecl):
                if tmp.declname is not None:
                    tmp.declname = name
                    break
            elif isinstance(tmp, c_ast.FuncDecl):
                if 'static' not in decl.storage:
                    if tmp.args is None:
                        tmp.args = c_ast.ParamList(list())
                    if (len(tmp.args.params) == 0) or (tmp.args.params[0].name != 'this'):
                        tmp.args.params.insert(0, self.make_this_ptr())
            tmp = tmp.type
        decl.storage.clear()
        decl.storage = ['extern']
        return decl

    def make_vtable_field(self, decl):
        assert isinstance(decl, c_ast.Decl)
        assert isinstance(decl.type, c_ast.FuncDecl)
        assert 'virtual' in decl.storage
        args = decl.type.args if copy.deepcopy(decl.type.args) else c_ast.ParamList(list())
        if (len(args.params) == 0) or (args.params[0].name != 'this'):
            args.params.insert(0, self.make_this_ptr())
        return c_ast.Decl(
            decl.name,
            list(), list(), list(),
            c_ast.PtrDecl(
                list(),
                c_ast.FuncDecl(
                    args,
                    decl.type.type
                )
            ),
            None, None,
            decl.coord
        )

    def initialize_vtable_fields_dict(self, fields):
        fields[self.VTABLE_PARENT_LINK_NAME] = c_ast.Decl(
            self.VTABLE_PARENT_LINK_NAME,
            list(), list(), list(),
            c_ast.PtrDecl(
                list(),
                c_ast.TypeDecl(
                    self.VTABLE_PARENT_LINK_NAME,
                    ['const'],
                    c_ast.Struct(
                        self.VTABLE_TYPE_NAME_FMT % self.parent.name,
                        None
                    ) if self.parent is not None else c_ast.IdentifierType(['void'])
                )
            ),
            None, None
        )
        fields[self.VTABLE_NAME_LINK_NAME] = c_ast.Decl(
            self.VTABLE_NAME_LINK_NAME,
            list(), list(), list(),
            c_ast.PtrDecl(
                list(),
                c_ast.TypeDecl(
                    self.VTABLE_NAME_LINK_NAME,
                    ['const'],
                    c_ast.IdentifierType(['char'])
                )
            ),
            None, None
        )

    def get_vtable_fields(self, include_parent=True):
        if self.ast_node is None:
            return None
        fields = OrderedDict()
        if self.parent is not None:
            if include_parent:
                fields = self.parent.get_vtable_fields()
                self.has_vtable = self.parent.has_vtable
        self.initialize_vtable_fields_dict(fields)
        for decl in self.ast_node.decls:
            if isinstance(decl, c_ast.Decl):
                if isinstance(decl.type, c_ast.FuncDecl):
                    if 'virtual' in decl.storage:
                        args = decl.type.args if decl.type.args else c_ast.ParamList(list())
                        if (len(args.params) == 0) or (args.params[0].name != 'this'):
                            args.params.insert(0, self.make_this_ptr())
                        new_decl = self.make_vtable_field(decl)
                        fields[new_decl.name] = new_decl
        self.has_vtable = len(fields) > 2
        return fields if self.has_vtable else None

    def get_fields(self, include_parent=True):
        if self.ast_node is None:
            return None
        fields = OrderedDict()
        if self.parent is not None:
            if include_parent:
                fields = self.parent.get_fields()
            self.has_vtable = self.parent.has_vtable
        for decl in self.ast_node.decls:
            if isinstance(decl, c_ast.Decl):
                if isinstance(decl.type, c_ast.FuncDecl):
                    if 'virtual' in decl.storage:
                        self.has_vtable = True
                    continue
                if 'static' in decl.storage:
                    continue
                fields[decl.name] = decl
        if self.has_vtable:
            vtable_fields = self.get_vtable_fields()
            fields[self.VTABLE_LINK_NAME] = c_ast.Decl(
                self.VTABLE_LINK_NAME,
                list(), list(), list(),
                c_ast.PtrDecl(
                    list(),
                    c_ast.TypeDecl(
                        self.VTABLE_LINK_NAME,
                        ['const'],
                        c_ast.Struct(self.VTABLE_TYPE_NAME_FMT % self.name,
                                     [decl for name, decl in iteritems(vtable_fields)])
                    )
                ),
                None, None
            )
        return fields

    def get_toplevel_decls(self, include_parent=False):
        if self.ast_node is None:
            return None
        decls = list()
        if self.parent is not None:
            if include_parent:
                decls = self.parent.get_toplevel_decls()
        if self.has_vtable:
            vtable_name = self.VTABLE_NAME_FMT % self.name
            decls.append(
                c_ast.Decl(
                    vtable_name,
                    list(), ['extern'], list(),
                    c_ast.TypeDecl(
                        vtable_name,
                        ['const'],
                        c_ast.Struct(self.VTABLE_TYPE_NAME_FMT % self.name, None)
                    ),
                    None, None,
                    self.ast_node.coord
                )
            )
        for decl in self.ast_node.decls:
            if isinstance(decl.type, c_ast.FuncDecl):
                if 'virtual' in decl.storage:
                    if decl.init is not None:
                        continue
            if isinstance(decl.type, c_ast.FuncDecl) or 'static' in decl.storage:
                decls.append(self.make_method_prototype(decl))
        return decls

    def to_decl(self):
        flag_name = 'struct %s declared' % self.name
        make_full_decls = self.name is None
        if not make_full_decls:
            make_full_decls = flag_name not in self.ast_transformer.root_scope.attrs
        if self.ast_node is None:
            make_full_decls = False
        if make_full_decls:
            self.ast_transformer.root_scope.attrs.add(flag_name)
            node = c_ast.Struct(self.name, list(), self.ast_node.coord)
            node.decls = [decl for name, decl in iteritems(self.get_fields())]
            toplevel_decls = self.get_toplevel_decls()
            self.ast_transformer.schedule_decl(toplevel_decls)
            return c_ast.TypeDecl(None, self.quals, node)
        return c_ast.TypeDecl(None, self.quals, c_ast.Struct(self.name, None))

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
                    c_ast.StructRef(expression.ast_node.name, '->', c_ast.ID(self.VTABLE_LINK_NAME)),
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
            vtable_name = self.VTABLE_NAME_FMT % self.name
            vtable_symbol = ast_transformer.scope.find_symbol(vtable_name)
            if vtable_symbol is not None:
                if 'extern' in vtable_symbol.storage:
                    vtable_symbol = None
            if vtable_symbol is None:
                vtable_values = OrderedDict()
                if (self.parent is None) or not self.parent.has_vtable:
                    vtable_values[self.VTABLE_PARENT_LINK_NAME] = c_ast.Constant('int', '0')
                else:
                    vtable_values[self.VTABLE_PARENT_LINK_NAME] = c_ast.UnaryOp('&',
                                                                c_ast.ID(self.VTABLE_NAME_FMT % self.parent.name))
                vtable_values[self.VTABLE_NAME_LINK_NAME] = c_ast.Constant('string', '\"%s\"' % self.name)
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
                ast_transformer.schedule_decl(
                    c_ast.Decl(
                        vtable_name, ['const'], list(), list(),
                        c_ast.TypeDecl(vtable_name, ['const'],
                                       c_ast.Struct(self.VTABLE_TYPE_NAME_FMT % self.name, None)),
                        c_ast.InitList([value for key, value in iteritems(vtable_values)]),
                        None,
                        node.coord
                    )
                )
            i, j = 0, 0
            while i < len(node.body.block_items):
                n = node.body.block_items[i]
                if self.contains_construct_call(n):
                    j = i + 1
                i += 1
            node.body.block_items.insert(
                j,
                c_ast.Assignment(
                    '=',
                    c_ast.StructRef(c_ast.ID('this'), '->', c_ast.ID(self.VTABLE_LINK_NAME)),
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

    @staticmethod
    def contains_construct_call(n):
        if isinstance(n, c_ast.UnaryOp):
            return StructTypeInfo.contains_construct_call(n.expr)
        if isinstance(n, c_ast.BinaryOp):
            return StructTypeInfo.contains_construct_call(n.left) or StructTypeInfo.contains_construct_call(n.right)
        if isinstance(n, c_ast.Assignment):
            return StructTypeInfo.contains_construct_call(n.lvalue) or \
                StructTypeInfo.contains_construct_call(n.rvalue)
        if isinstance(n, c_ast.ArrayRef):
            return StructTypeInfo.contains_construct_call(n.name) or \
                StructTypeInfo.contains_construct_call(n.subscript)
        if isinstance(n, c_ast.StructRef):
            return StructTypeInfo.contains_construct_call(n.name)
        if isinstance(n, c_ast.FuncCall):
            if isinstance(n.name, c_ast.StructRef):
                if isinstance(n.name.name, c_ast.ID):
                    if n.name.name.name == 'this':
                        if isinstance(n.name.field, c_ast.ID):
                            if isinstance(n.name.field.name, tuple):
                                if len(n.name.field.name) == 2:
                                    if n.name.field.name[1] == 'construct':
                                        return True
            elif isinstance(n.name, c_ast.ID):
                if isinstance(n.name.name, tuple):
                    if len(n.name.name) == 2:
                        if n.name.name[1] == 'construct':
                            return True
            if n.args is not None:
                for arg in n.args.exprs:
                    if StructTypeInfo.contains_construct_call(arg):
                        return True
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
            return tmp.safe_cast(expression, type_info)
        return None

    def to_decl(self):
        return c_ast.PtrDecl(list(), self.base_type.to_decl())


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
                        dst_type_decl = c_ast.Typename(None, type_info.quals, type_info.to_decl())
                        return CastExpression(expression, type_info, c_ast.Cast(dst_type_decl, expression.ast_node))
        return None

    def to_decl(self):
        return_type_decl = self.return_type.to_decl()
        if not isinstance(return_type_decl, c_ast.TypeDecl):
            return_type_decl = c_ast.TypeDecl(None, list(), return_type_decl)
        node = c_ast.FuncDecl(c_ast.ParamList(list()), return_type_decl)
        for arg_type in self.args_types:
            if arg_type is not None:
                arg_type_decl = arg_type.to_decl()
                arg_type_decl = c_ast.Typename(None, list(), arg_type_decl)
            else:
                arg_type_decl = c_ast.EllipsisParam()
            node.args.params.append(arg_type_decl)
        return node


class LambdaFuncTypeInfo(FuncTypeInfo):
    LAMBDA_FUNC_NAME_FMT = '__lambda_%s'
    CLOSURE_LINK_NAME = '__closure'
    CLOSURE_DATA_TYPE_NAME_FMT = '%s_ClosureData'
    CLOSURE_DATA_LINK_NAME = '__closure_data'
    CLOSURE_FUNC_LINK_NAME = '__fn'
    CLOSURE_DATA_NAME_FMT = '%s_data'

    def __init__(self, name, return_type, args_types, ast_node, ast_transformer):
        FuncTypeInfo.__init__(self, return_type, args_types)
        self.name = name
        self.ast_node = ast_node
        self.ast_transformer = ast_transformer

    def safe_cast(self, expression, type_info):
        from .error import CodeSyntaxError
        use_closure = False
        if isinstance(type_info, PtrTypeInfo):
            if isinstance(type_info.base_type, PtrTypeInfo):
                use_closure = True
        if not use_closure and self.ast_node.capture_list:
            raise CodeSyntaxError('Cannot convert closure to function pointer', self.ast_node.coord)
        params = self.ast_node.args.params if self.ast_node.args else list()
        body = self.ast_node.body.block_items
        if use_closure:
            params = [c_ast.Decl(
                self.CLOSURE_LINK_NAME, list(), list(), list(),
                c_ast.PtrDecl(
                    ['const'],
                    c_ast.TypeDecl(
                        self.CLOSURE_LINK_NAME,
                        list(),
                        c_ast.IdentifierType(['void'])
                    )
                ),
                None, None
            )] + params
            closure_data_type_name = self.CLOSURE_DATA_TYPE_NAME_FMT % self.name
            closure_struct_members = [
                c_ast.Decl(
                    self.CLOSURE_FUNC_LINK_NAME,
                    list(), list(), list(),
                    c_ast.PtrDecl(
                        list(),
                        c_ast.FuncDecl(
                            c_ast.ParamList(params),
                            c_ast.TypeDecl(
                                self.CLOSURE_FUNC_LINK_NAME,
                                self.ast_node.return_type.type.quals,
                                self.ast_node.return_type.type.type
                            )
                        )
                    ),
                    None, None
                )
            ]
            for capture_item in self.ast_node.capture_list:
                link = capture_item[0] == '&'
                if link:
                    capture_item = capture_item[1:]
                symbol = self.ast_transformer.scope.find_symbol(capture_item)
                if isinstance(symbol, VariableInfo):
                    type_decl = symbol.type.to_decl()
                    tmp = type_decl
                    while not isinstance(tmp, c_ast.TypeDecl):
                        tmp = tmp.type
                    tmp.declname = capture_item
                    closure_struct_members.append(
                        c_ast.Decl(
                            capture_item,
                            list(), list(), list(),
                            c_ast.PtrDecl(list(), type_decl) if link else type_decl,
                            None, None
                        )
                    )
                else:
                    raise CodeSyntaxError('Variable %s not found' % capture_item, self.ast_node.coord)
            self.ast_transformer.schedule_decl(
                c_ast.Struct(
                    closure_data_type_name,
                    closure_struct_members,
                    self.ast_node.coord
                ), True
            )
            body = [
                c_ast.Decl(
                    self.CLOSURE_DATA_LINK_NAME,
                    list(), list(), list(),
                    c_ast.PtrDecl(
                        ['const'],
                        c_ast.TypeDecl(
                            self.CLOSURE_DATA_LINK_NAME,
                            list(),
                            c_ast.Struct(closure_data_type_name, None)
                        )
                    ),
                    c_ast.ID(self.CLOSURE_LINK_NAME), None
                )
            ] + body
            closure_data_name = self.CLOSURE_DATA_NAME_FMT % self.name
            self.ast_transformer.schedule_tmp_decl(
                c_ast.Decl(
                    closure_data_name,
                    list(), list(), list(),
                    c_ast.PtrDecl(
                        ['const'],
                        c_ast.TypeDecl(
                            closure_data_name,
                            list(),
                            c_ast.Struct(closure_data_type_name, None)
                        )
                    ),
                    c_ast.FuncCall(
                        c_ast.ID('malloc'),
                        c_ast.ExprList([
                            c_ast.UnaryOp('sizeof', c_ast.Struct(closure_data_type_name, None))
                        ])
                    ), None
                )
            )
            self.ast_transformer.schedule_tmp_decl(
                c_ast.Assignment(
                    '=',
                    c_ast.StructRef(c_ast.ID(closure_data_name), '->', c_ast.ID(self.CLOSURE_FUNC_LINK_NAME)),
                    c_ast.ID(self.name),
                    self.ast_node.coord
                )
            )
            for capture_item in self.ast_node.capture_list:
                link = capture_item[0] == '&'
                if link:
                    capture_item = capture_item[1:]
                value = c_ast.ID(capture_item)
                if link:
                    value = c_ast.UnaryOp('&', value)
                self.ast_transformer.schedule_tmp_decl(
                    c_ast.Assignment(
                        '=',
                        c_ast.StructRef(c_ast.ID(closure_data_name), '->', c_ast.ID(capture_item)),
                        value,
                        self.ast_node.coord
                    )
                )
        self.ast_transformer.schedule_decl(
            c_ast.FuncDef(
                c_ast.Decl(
                    self.name,
                    list(),
                    ['static'],
                    list(),
                    c_ast.FuncDecl(
                        c_ast.ParamList(params),
                        c_ast.TypeDecl(
                            self.name,
                            self.ast_node.return_type.type.quals,
                            self.ast_node.return_type.type.type
                        )
                    ),
                    None,
                    None
                ),
                None,
                c_ast.Compound(body),
                self.ast_node.coord
            ),
            True
        )
        from .scope import Scope
        from .expression import VariableExpression
        if use_closure:
            return VariableExpression(
                closure_data_name,
                Scope(),
                c_ast.Cast(
                    c_ast.Typename(
                        None, list(),
                        c_ast.PtrDecl(
                            list(),
                            c_ast.TypeDecl(
                                None,
                                list(),
                                c_ast.IdentifierType(['void'])
                            )
                        )
                    ),
                    c_ast.ID(closure_data_name),
                    self.ast_node.coord
                )
            )
        return VariableExpression(self.name, Scope(),
                                  c_ast.ID(self.name, self.ast_node.coord))


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
                    dst_type_decl = base_type.to_decl()
                    if not isinstance(dst_type_decl, c_ast.TypeDecl):
                        dst_type_decl = c_ast.TypeDecl(None, list(), dst_type_decl)
                    return CastExpression(expression, type_info,
                                          c_ast.Cast(c_ast.PtrDecl(type_info.quals, dst_type_decl),
                                                                                    expression.ast_node))
            if TypeInfo.is_compatible(self.base_type, base_type):
                return expression
        return None

    def to_decl(self):
        base_type_decl = self.base_type.to_decl()
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
