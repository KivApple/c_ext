import copy
from collections import OrderedDict
from six import iteritems

import pycparser.c_ast as c_ast
from pycparserext.ext_c_parser import TypeDeclExt, ArrayDeclExt, FuncDeclExt, AttributeSpecifier

from .error import CodeSyntaxError
from .parser import StructImproved, LambdaFunc
from .scope import Scope
from .types import *
from .expression import *


class ASTTransformer(c_ast.NodeVisitor):
    def __init__(self):
        self.scope = None
        self.root_scope = None
        self.scheduled_decls = list()
        self.scheduled_tmp_decls = list()
        self.node_path = list()
        self.cur_lambda_id = 0
        self.lambdas = dict()
        self.need_async_call = False
        self.next_async_func_id = 0
        self.next_async_state_id = 1
        self.func_async_states = OrderedDict()
        self.local_ids = set()
        self.local_ids_in_cur_async_state = set()
        self.func_async_state_decls = OrderedDict()
        self.async_returns = list()
        self.id_translate_table = dict()

    def visit(self, node):
        self.node_path.append(node)
        retval = super(ASTTransformer, self).visit(node)
        del self.node_path[-1]
        return retval

    def visit_FileAST(self, node):
        self.root_scope = Scope()
        self.scope = self.root_scope
        i = 0
        while i < len(node.ext):
            i = self.visit_DeclByIndex(node.ext, i)
        self.scope = None
        self.root_scope = None

    def visit_DeclByIndex(self, lst, i):
        scheduled_secls = self.scheduled_decls
        self.scheduled_decls = list()
        self.visit(lst[i])
        j = 0
        while j < len(self.scheduled_decls):
            if self.scheduled_decls[j][1]:
                lst.insert(i, self.scheduled_decls[j][0])
                i = self.visit_DeclByIndex(lst, i)
            j += 1
        i += 1
        j = 0
        while j < len(self.scheduled_decls):
            if not self.scheduled_decls[j][1]:
                lst.insert(i, self.scheduled_decls[j][0])
                i = self.visit_DeclByIndex(lst, i)
            j += 1
        self.scheduled_decls = scheduled_secls
        return i

    def visit_IdentifierType(self, node):
        assert isinstance(node, c_ast.IdentifierType)
        full_type_name = ' '.join(node.names)
        type_info = self.scope.find_symbol(full_type_name)
        if type_info is not None:
            if not isinstance(type_info, TypeInfo):
                raise CodeSyntaxError('%s is not name of type' % full_type_name, node.coord)
            return type_info
        return ScalarTypeInfo(full_type_name)

    def visit_Enum(self, node):
        assert isinstance(node, c_ast.Enum)
        return ScalarTypeInfo('int')

    def visit_Struct(self, node):
        return self.visit_StructOrUnion(node)

    def visit_StructImproved(self, node):
        return self.visit_StructOrUnion(node)

    def visit_Union(self, node):
        return self.visit_StructOrUnion(node)

    def visit_StructOrUnion(self, node):
        assert isinstance(node, (c_ast.Struct, c_ast.Union))
        kind = 'union' if isinstance(node, c_ast.Union) else 'struct'
        parent = None
        if isinstance(node, StructImproved):
            parent = self.scope.find_symbol('struct %s' % node.parent)
            if not isinstance(parent, StructTypeInfo):
                raise CodeSyntaxError('%s is not name of struct type' % node.parent, node.coord)
        type_info = None
        if node.name is not None:
            type_info = self.scope.find_symbol('%s %s' % (kind, node.name))
        if type_info is None:
            type_info = StructTypeInfo(kind, node.name, self)
            type_info.scope = Scope()
            type_info.scope.attrs.add('struct')
            type_info.scope.owner = type_info
            if node.name is not None:
                self.root_scope.add_symbol('%s %s' % (kind, node.name), type_info)
        if node.decls is not None:
            prev_scope = self.scope
            self.scope = type_info.scope
            self.scope.symbols.clear()
            self.scope.parents.clear()
            self.scope.parents.append(parent.scope if parent is not None else None)
            self.scope.parents.append(prev_scope)
            self.generic_visit(node)
            type_info.parent = parent
            type_info.scope = self.scope
            type_info.ast_node = node
            self.scope = prev_scope
        return type_info

    def visit_TypeDecl(self, node):
        assert isinstance(node, (c_ast.TypeDecl, TypeDeclExt))
        type_info = self.visit(node.type)
        if isinstance(node.type, c_ast.Struct):
            node.type = type_info.to_decl()
        type_info = type_info.clone()
        type_info.quals += node.quals
        return type_info

    def visit_TypeDeclExt(self, node):
        return self.visit_TypeDecl(node)

    def visit_ArrayDecl(self, node):
        assert isinstance(node, (c_ast.ArrayDecl, ArrayDeclExt))
        type_info = self.visit(node.type)
        dim = None
        if node.dim is not None:
            dim = self.visit(node.dim)
        return ArrayTypeInfo(type_info, dim)

    def visit_ArrayDeclExt(self, node):
        assert isinstance(node, ArrayDeclExt)
        return self.visit_ArrayDecl(node)

    def visit_FuncDecl(self, node):
        assert isinstance(node, (c_ast.FuncDecl, FuncDeclExt))
        return_type = self.visit(node.type)
        args = list()
        if node.args is not None:
            for arg_decl in node.args.params:
                if isinstance(arg_decl, c_ast.Decl):
                    arg_type_info = self.visit(arg_decl.type)
                    init = self.visit(arg_decl.init) if arg_decl.init is not None else None
                    args.append(FuncArgInfo(arg_decl.name, arg_type_info, init))
                    arg_decl.init = None
                elif isinstance(arg_decl, c_ast.Typename):
                    arg_type_info = self.visit(arg_decl.type)
                    args.append(FuncArgInfo(arg_decl.name, arg_type_info, None))
                elif isinstance(arg_decl, c_ast.EllipsisParam):
                    args.append(None)
                    break
        type_info = FuncTypeInfo(return_type, args)
        return type_info

    def visit_FuncDeclExt(self, node):
        assert isinstance(node, FuncDeclExt)
        return self.visit_FuncDecl(node)

    def visit_PtrDecl(self, node):
        assert isinstance(node, c_ast.PtrDecl)
        type_info = self.visit(node.type)
        type_info = PtrTypeInfo(type_info, node.quals)
        return type_info

    def visit_Typename(self, node):
        assert isinstance(node, c_ast.Typename)
        return self.visit(node.type)

    def visit_Decl(self, node):
        assert isinstance(node, c_ast.Decl)
        if isinstance(self.scope.owner, StructTypeInfo):
            self.scope.owner.fix_member_declaration(node)
        elif (len(self.node_path) >= 2) and isinstance(self.node_path[-2], (c_ast.Compound, c_ast.For)):
            if node.name not in self.scope.symbols:
                prefix = node.name
                i = 0
                while self.scope.find_symbol(node.name) is not None:
                    i += 1
                    node.name = '%s_%s' % (prefix, i)
                if i > 0:
                    self.id_translate_table[prefix] = node.name
                    tmp = node.type
                    while not isinstance(tmp, c_ast.TypeDecl):
                        tmp = node.type
                    tmp.declname = node.name
        if isinstance(node.name, tuple):
            assert len(node.name) == 2
            struct_type_info = self.scope.find_symbol("struct %s" % node.name[0])
            if not isinstance(struct_type_info, StructTypeInfo):
                raise CodeSyntaxError('%s is not structure name' % node.name[0], node.coord)
            member_name = node.name[1]
            new_name = '%s_%s' % (struct_type_info.name, member_name)
            node.name = new_name
            tmp = node.type
            while not isinstance(tmp, c_ast.TypeDecl):
                tmp = tmp.type
            tmp.declname = new_name
            struct_type_info.fix_member_implementation(node, member_name)
        type_info = self.visit(node.type)
        if isinstance(node.type, c_ast.Struct):
            node.type = type_info.to_decl()
        var_info = None
        if node.name is not None:
            symbol = self.scope.find_symbol(node.name, True)
            if symbol is not None:
                fail = True
                if isinstance(symbol, VariableInfo):
                    if symbol.type.__class__ == type_info.__class__:
                        if 'extern' in symbol.storage:
                            fail = False
                        elif isinstance(type_info, FuncTypeInfo):
                            if 'struct' in self.scope.attrs:
                                fail = False
                            else:
                                tmp = symbol.type
                                if not isinstance(tmp, PtrTypeInfo):
                                    tmp = PtrTypeInfo(tmp)
                                if TypeInfo.is_compatible(type_info, tmp):
                                    fail = False
                if fail:
                    raise CodeSyntaxError('Symbol %s already defined in current scope' % node.name, node.coord)
            var_info = VariableInfo(node.name, type_info, node.storage, self.scope, coord=node.coord)
            if 'struct' in self.scope.attrs:
                var_info.attrs.add('member')
            self.scope.add_symbol(node.name, var_info)
            if node.init is not None:
                init = self.visit(node.init)
                if init is not None:
                    self.scope.symbols[node.name].init = init
                    init = TypeInfo.make_safe_cast(init, type_info)
                    if init is not None:
                        node.init = init.ast_node
                        self.scope.symbols[node.name].init = init
                    else:
                        pass # Warning
        if 'static' not in node.storage:
            tmp = self.scope
            while tmp is not None:
                if isinstance(tmp.owner, FuncTypeInfo):
                    self.local_ids.add(var_info.name)
                    self.local_ids_in_cur_async_state.add(var_info.name)
                    break
                if len(tmp.parents) == 0:
                    break
                tmp = tmp.parents[0]
        return var_info

    def visit_Typedef(self, node):
        assert isinstance(node, c_ast.Typedef)
        type_info = self.visit(node.type)
        self.scope.add_symbol(node.name, type_info)

    def visit_Constant(self, node):
        assert isinstance(node, c_ast.Constant)
        return ConstantExpression(node.value, node.type, node)

    def visit_ID(self, node):
        assert isinstance(node, c_ast.ID)
        node.name = self.id_translate_table.get(node.name, node.name)
        symbol_scope = self.scope
        symbol_name = node.name
        if isinstance(node.name, tuple):
            if len(node.name) != 2:
                raise CodeSyntaxError('Only struct_id::member_name format is supported')
            struct_type_info = self.scope.find_symbol('struct %s' % node.name[0])
            if not isinstance(struct_type_info, StructTypeInfo):
                raise CodeSyntaxError('%s is not a structure name' % node.name[0], node)
            symbol_scope = struct_type_info.scope
            symbol_name = node.name[1]
        elif symbol_name in self.local_ids:
            if symbol_name not in self.local_ids_in_cur_async_state:
                self.func_async_state_decls[symbol_name] = True
                self.local_ids_in_cur_async_state.add(symbol_name)
            elif symbol_name not in self.scope.symbols:
                tmp = self.scope
                while (tmp is not None) and not isinstance(tmp.owner, c_ast.FuncDef):
                    if isinstance(tmp.owner, (c_ast.While, c_ast.DoWhile, c_ast.For)):
                        self.func_async_state_decls[symbol_name] = True
                        self.local_ids_in_cur_async_state.add(symbol_name)
                        break
                    tmp = tmp.parents[-1]
        return VariableExpression(symbol_name, symbol_scope, node)

    def visit_UnaryOp(self, node):
        assert isinstance(node, c_ast.UnaryOp)
        if node.op == '&':
            tmp = node.expr
            while not isinstance(tmp, c_ast.ID):
                if isinstance(tmp, c_ast.StructRef):
                    tmp = tmp.name
                elif isinstance(tmp, c_ast.ArrayRef):
                    tmp = tmp.name
                else:
                    break
            if isinstance(tmp, c_ast.ID):
                self.func_async_state_decls[tmp.name] = True
                self.local_ids_in_cur_async_state.add(tmp.name)
        return UnaryExpression(node.op, self.visit(node.expr), node)

    def visit_BinaryOp(self, node):
        assert isinstance(node, c_ast.BinaryOp)
        return BinaryExpression(node.op, self.visit(node.left), self.visit(node.right), node)

    def visit_TernaryOp(self, node):
        assert isinstance(node, c_ast.TernaryOp)
        return TernaryExpression(node.cond, node.iftrue, node.iffalse, node)

    def visit_Cast(self, node):
        assert isinstance(node, c_ast.Cast)
        type_info = self.visit(node.to_type)
        return CastExpression(self.visit(node.expr), type_info, node)

    def visit_ArrayRef(self, node):
        assert isinstance(node, c_ast.ArrayRef)
        return SubscriptExpression(self.visit(node.name), self.visit(node.subscript), node)

    def visit_StructRef(self, node):
        assert isinstance(node, c_ast.StructRef)
        assert isinstance(node.field, c_ast.ID)
        return MemberExpression(self.visit(node.name), node.field.name, node.type, node)

    def visit_FuncCall(self, node):
        assert isinstance(node, c_ast.FuncCall)
        args = list()
        if node.args is not None:
            for arg in node.args.exprs:
                args.append(self.visit(arg))
        func = self.visit(node.name)
        if self.need_async_call:
            raise CodeSyntaxError('Async call should not be a part of a complex expression', node.coord)
        return CallExpression(func, args, node, self)

    def visit_Assignment(self, node):
        assert isinstance(node, c_ast.Assignment)
        return BinaryExpression(node.op, self.visit(node.lvalue), self.visit(node.rvalue), node)

    def visit_Compound(self, node):
        assert isinstance(node, c_ast.Compound)
        if node.block_items is not None:
            prev_scope = self.scope
            self.scope = Scope(self.scope)
            self.scope.attrs = prev_scope.attrs
            self.scope.owner = self.node_path[-2]
            i = 0
            while i < len(node.block_items):
                retval = self.visit(node.block_items[i])
                if isinstance(retval, Expression):
                    node.block_items[i] = retval.ast_node
                for decl in self.scheduled_tmp_decls:
                    node.block_items.insert(i, decl)
                    i += 1
                self.scheduled_tmp_decls.clear()
                if self.need_async_call:
                    async_state_label_name = '__async_state_%i' % self.next_async_state_id
                    self.func_async_states[self.next_async_state_id] = async_state_label_name
                    return_node = c_ast.Return(None, node.block_items[i].coord)
                    self.async_returns.append(return_node)
                    node.block_items.insert(i + 1, return_node)
                    node.block_items.insert(i + 2, c_ast.Label(async_state_label_name, None,
                        node.block_items[i].coord))
                    node.block_items.insert(i, c_ast.Assignment(
                        '=',
                        c_ast.StructRef(
                            c_ast.ID(LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME), '->', c_ast.ID('__state')
                        ),
                        c_ast.Constant('int', str(self.next_async_state_id)),
                        node.block_items[i].coord
                    ))
                    i += 1
                    self.next_async_state_id += 1
                    self.need_async_call = False
                    self.local_ids_in_cur_async_state.clear()
                i += 1
            self.scope = prev_scope

    def visit_If(self, node):
        assert isinstance(node, c_ast.If)
        value = self.visit(node.cond)
        node.cond = value.ast_node
        if node.iftrue is not None:
            self.visit(node.iftrue)
        if node.iffalse is not None:
            self.visit(node.iffalse)

    def visit_While(self, node):
        assert isinstance(node, c_ast.While)
        value = self.visit(node.cond)
        node.cond = value.ast_node
        if node.stmt is not None:
            self.visit(node.stmt)

    def visit_DoWhile(self, node):
        assert isinstance(node, c_ast.DoWhile)
        if node.stmt is not None:
            self.visit(node.stmt)
        value = self.visit(node.cond)
        node.cond = value.ast_node

    def visit_Switch(self, node):
        assert isinstance(node, c_ast.Switch)
        value = self.visit(node.cond)
        node.cond = value.ast_node
        self.visit(node.stmt)

    def visit_Return(self, node):
        assert isinstance(node, c_ast.Return)
        if node.expr:
            value = self.visit(node.expr)
            i = len(self.node_path) - 1
            while i >= 0:
                n = self.node_path[i]
                if isinstance(n, c_ast.FuncDef):
                    symbol = self.scope.find_symbol(n.decl.name)
                    assert isinstance(symbol, VariableInfo)
                    assert isinstance(symbol.type, FuncTypeInfo)
                    type_info = symbol.type.return_type
                    value = TypeInfo.make_safe_cast(value, type_info)
                    break
                i -= 1
            node.expr = value.ast_node

    def visit_FuncDef(self, node):
        assert isinstance(node, c_ast.FuncDef)
        name_ = node.decl.name
        var_info = self.visit(node.decl)
        prev_scope = self.scope
        self.scope = Scope(self.scope)
        self.scope.owner = self.lambdas.get(node.decl.name, var_info.type)
        assert isinstance(var_info.type, FuncTypeInfo)
        for arg in var_info.type.args:
            if arg is not None:
                self.scope.add_symbol(arg.name, VariableInfo(arg.name, arg.type_info, list(), self.scope))
        self.local_ids.clear()
        self.local_ids_in_cur_async_state.clear()
        self.id_translate_table.clear()
        self.func_async_state_decls.clear()
        if isinstance(name_, tuple):
            assert len(name_) == 2
            type_info = self.scope.find_symbol('struct %s' % name_[0])
            if isinstance(type_info, StructTypeInfo):
                self.scope.parents.insert(0, type_info.scope)
                self.scope.attrs.add('member')
                type_info.fix_func_implementation(node, name_[1], self)
            else:
                raise CodeSyntaxError('%s is not a structure name' % name_[0], node.coord)
        if isinstance(self.scope.owner, LambdaFuncTypeInfo):
            for capture_item in self.scope.owner.capture_list:
                symbol = VariableInfo(capture_item.name, capture_item.type_info, ['closure'], self.scope)
                if capture_item.link:
                    symbol.attrs.add('link')
                self.scope.add_symbol(symbol.name, symbol)
        self.func_async_states.clear()
        self.async_returns.clear()
        self.visit(node.body)
        if len(self.func_async_states) > 0:
            i = 0
            static_async_state_storage = False
            while i < len(node.decl.funcspec):
                if isinstance(node.decl.funcspec[i], AttributeSpecifier):
                    if node.decl.funcspec[i].exprlist is not None:
                        if len(node.decl.funcspec[i].exprlist.exprs) == 1:
                            if isinstance(node.decl.funcspec[i].exprlist.exprs[0], c_ast.ID):
                                if node.decl.funcspec[i].exprlist.exprs[0].name == 'static_async_state':
                                    static_async_state_storage = True
                                    del node.decl.funcspec[i]
                                    break
                i += 1
            args_names = list()
            if node.decl.type.args is not None:
                for arg_decl in node.decl.type.args.params:
                    if isinstance(arg_decl, c_ast.EllipsisParam):
                        raise CodeSyntaxError('Async functions cannot be variadic', node.coord)
                    elif isinstance(arg_decl, c_ast.Decl):
                        self.func_async_state_decls[arg_decl.name] = arg_decl
                        args_names.append(arg_decl.name)
            if not isinstance(node.decl.type.type, c_ast.TypeDecl)\
                or not isinstance(node.decl.type.type.type, c_ast.IdentifierType)\
                or ' '.join(node.decl.type.type.type.names) != 'void':
                raise CodeSyntaxError('Async functions cannot return value', node.coord)
            decl = node.decl
            func_body_name = '__async_func_%s' % self.cur_lambda_id
            self.schedule_decl(decl, True)
            wrapper_func_body = list()
            if static_async_state_storage:
                state_storage_name = '%s_storage' % LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME
                wrapper_func_body += [
                    c_ast.Decl(
                        state_storage_name,
                        list(), ['static'], list(),
                        c_ast.TypeDecl(
                            state_storage_name,
                            list(),
                            c_ast.Struct(
                                LambdaFuncTypeInfo.CLOSURE_DATA_TYPE_NAME_FMT % func_body_name,
                                None
                            )
                        ),
                        None, None
                    ),
                    c_ast.Decl(
                        LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME,
                        list(), list(), list(),
                        c_ast.PtrDecl(
                            list(),
                            c_ast.TypeDecl(
                                LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME,
                                list(),
                                c_ast.Struct(
                                    LambdaFuncTypeInfo.CLOSURE_DATA_TYPE_NAME_FMT % func_body_name,
                                    None
                                )
                            )
                        ),
                        c_ast.UnaryOp(
                            '&',
                            c_ast.ID(state_storage_name)
                        ),
                        None
                    )
                ]
            else:
                wrapper_func_body.append(c_ast.Decl(
                        LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME,
                        list(), list(), list(),
                        c_ast.PtrDecl(
                            list(),
                            c_ast.TypeDecl(
                                LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME,
                                list(),
                                c_ast.Struct(
                                    LambdaFuncTypeInfo.CLOSURE_DATA_TYPE_NAME_FMT % func_body_name,
                                    None
                                )
                            )
                        ),
                        c_ast.FuncCall(
                            c_ast.ID('malloc'),
                            c_ast.ExprList([
                                c_ast.UnaryOp('sizeof', c_ast.Struct(
                                    LambdaFuncTypeInfo.CLOSURE_DATA_TYPE_NAME_FMT % func_body_name,
                                    None
                                ))
                            ])
                        ),
                        None
                    ))
            wrapper_func_body += \
                [
                    c_ast.Assignment(
                        '=',
                        c_ast.StructRef(c_ast.ID(LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME),
                                        '->', c_ast.ID('__state')),
                        c_ast.Constant('int', '0')
                    )
                ] + \
                [c_ast.Assignment(
                    '=',
                    c_ast.StructRef(c_ast.ID(LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME),
                                    '->', c_ast.ID(arg_name)),
                    c_ast.ID(arg_name)
                ) for arg_name in args_names] + \
                [
                    c_ast.FuncCall(
                        c_ast.ID(func_body_name),
                        c_ast.ExprList([
                            c_ast.ID(LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME)
                        ])
                    )
                ]
            self.schedule_decl(c_ast.FuncDef(
                decl, None,
                c_ast.Compound(wrapper_func_body),
                decl.coord
            ))
            node.decl = c_ast.Decl(
                func_body_name,
                list(), ['static'], list(),
                c_ast.FuncDecl(
                    c_ast.ParamList([
                        c_ast.Decl(
                            LambdaFuncTypeInfo.CLOSURE_LINK_NAME,
                            list(), list(), list(),
                            c_ast.PtrDecl(
                                ['const'],
                                c_ast.TypeDecl(
                                    LambdaFuncTypeInfo.CLOSURE_LINK_NAME,
                                    list(),
                                    c_ast.IdentifierType(['void'])
                                )
                            ),
                            None, None
                        )
                    ]),
                    c_ast.TypeDecl(
                        func_body_name,
                        list(),
                        c_ast.IdentifierType(['void'])
                    )
                ),
                None, None,
                decl.coord
            )
            node.body.block_items.insert(0, self.make_async_state_switch())
            self.schedule_decl(c_ast.Decl(
                None, list(), list(), list(),
                c_ast.Struct(
                    LambdaFuncTypeInfo.CLOSURE_DATA_TYPE_NAME_FMT % func_body_name,
                    self.make_async_state_struct_fields_list()
                ),
                None, None,
                node.coord
            ), True)
            node.body.block_items.insert(0, c_ast.Decl(
                LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME,
                list(), list(), list(),
                c_ast.PtrDecl(
                    ['const'],
                    c_ast.TypeDecl(
                        LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME,
                        list(),
                        c_ast.Struct(
                            LambdaFuncTypeInfo.CLOSURE_DATA_TYPE_NAME_FMT % func_body_name,
                            None
                        )
                    )
                ),
                c_ast.ID(LambdaFuncTypeInfo.CLOSURE_LINK_NAME),
                None
            ))
            node.body.block_items.append(c_ast.Label(
                '__exit',
                c_ast.FuncCall(
                    c_ast.ID('free'),
                    c_ast.ExprList([
                        c_ast.ID(LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME)
                    ])
                ) if not static_async_state_storage else c_ast.Return(None)
            ))
            self.cur_lambda_id += 1
        self.async_returns.clear()
        self.func_async_state_decls.clear()
        self.local_ids_in_cur_async_state.clear()
        self.local_ids.clear()
        self.id_translate_table.clear()
        self.scope = prev_scope

    def visit_LambdaFunc(self, node):
        assert isinstance(node, LambdaFunc)
        func_name = LambdaFuncTypeInfo.LAMBDA_FUNC_NAME_FMT % self.cur_lambda_id
        self.cur_lambda_id += 1
        prev_scope = self.scope
        self.scope = Scope(self.scope)
        return_type_info = self.visit(node.return_type)
        args = list()
        if node.args:
            for arg in node.args.params:
                if isinstance(arg, c_ast.Decl):
                    type_info = self.visit(arg.type)
                    args.append(FuncArgInfo(arg.name, type_info, None))
                elif isinstance(arg, c_ast.Typename):
                    type_info = self.visit(arg.type)
                    args.append(FuncArgInfo(arg.name, type_info, None))
                elif isinstance(arg, c_ast.EllipsisParam):
                    args.append(None)
        self.scope = prev_scope
        type_info = LambdaFuncTypeInfo(func_name, return_type_info, args, node, self)
        self.lambdas[func_name] = type_info
        return LambdaFuncExpression(type_info, node)

    def schedule_decl(self, decl, prepend=False):
        if not isinstance(decl, (list, tuple)):
            assert decl is not None
            self.scheduled_decls.append((decl, prepend))
        else:
            self.scheduled_decls += [(d, prepend) for d in decl]

    def schedule_tmp_decl(self, decl):
        self.scheduled_tmp_decls.append(decl)

    def make_async_state_switch(self):
        switch_node = c_ast.Switch(
            c_ast.StructRef(c_ast.ID(LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME), '->', c_ast.ID('__state')),
            c_ast.Compound(list())
        )
        switch_node.stmt.block_items.append(
            c_ast.Case(
                c_ast.Constant('int', '0'),
                [c_ast.Break()]
            )
        )
        for id, label in iteritems(self.func_async_states):
            switch_node.stmt.block_items.append(
                c_ast.Case(
                    c_ast.Constant('int', str(id)),
                    [c_ast.Goto(label)]
                )
            )
        switch_node.stmt.block_items.append(
            c_ast.Default(
                [c_ast.Goto('__exit')]
            )
        )
        return switch_node

    def make_async_state_struct_fields_list(self):
        state_struct_fields = list()
        state_struct_fields.append(c_ast.Decl(
            LambdaFuncTypeInfo.CLOSURE_FUNC_LINK_NAME,
            list(), list(), list(),
            c_ast.PtrDecl(
                list(),
                c_ast.TypeDecl(
                    LambdaFuncTypeInfo.CLOSURE_FUNC_LINK_NAME,
                    list(),
                    c_ast.IdentifierType(['void'])
                )
            ),
            None, None
        ))
        state_struct_fields.append(c_ast.Decl(
            '__state',
            list(), list(), list(),
            c_ast.TypeDecl(
                '__state',
                list(),
                c_ast.IdentifierType(['int'])
            ),
            None, None
        ))
        self.fix_async_func(self.node_path[-1])
        for field_name, field_decl in iteritems(self.func_async_state_decls):
            if isinstance(field_decl, c_ast.Decl):
                state_struct_fields.append(field_decl)
        return state_struct_fields

    def fix_async_func(self, node):
        if isinstance(node, c_ast.FuncDef):
            node.body = self.fix_async_func(node.body)
        elif isinstance(node, c_ast.Decl):
            node.init = self.fix_async_func(node.init)
            if node.name in self.func_async_state_decls:
                init = node.init
                node.init = None
                self.func_async_state_decls[node.name] = node
                if init is not None:
                    return c_ast.Assignment(
                        '=',
                        c_ast.StructRef(
                            c_ast.ID(LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME), '->',
                            c_ast.ID(node.name)
                        ),
                        init,
                        node.coord
                    )
                return None
        elif isinstance(node, c_ast.BinaryOp):
            node.left = self.fix_async_func(node.left)
            node.right = self.fix_async_func(node.right)
            return node
        elif isinstance(node, c_ast.UnaryOp):
            node.expr = self.fix_async_func(node.expr)
        elif isinstance(node, c_ast.Assignment):
            node.lvalue = self.fix_async_func(node.lvalue)
            node.rvalue = self.fix_async_func(node.rvalue)
        elif isinstance(node, c_ast.FuncCall):
            node.name = self.fix_async_func(node.name)
            node.args = self.fix_async_func(node.args)
        elif isinstance(node, c_ast.ExprList):
            i = 0
            while i < len(node.exprs):
                node.exprs[i] = self.fix_async_func(node.exprs[i])
                i += 1
        elif isinstance(node, c_ast.If):
            node.cond = self.fix_async_func(node.cond)
            node.iftrue = self.fix_async_func(node.iftrue)
            node.iffalse = self.fix_async_func(node.iffalse)
        elif isinstance(node, c_ast.While):
            node.cond = self.fix_async_func(node.cond)
            node.stmt = self.fix_async_func(node.stmt)
        elif isinstance(node, c_ast.DoWhile):
            node.cond = self.fix_async_func(node.cond)
            node.stmt = self.fix_async_func(node.stmt)
        elif isinstance(node, c_ast.For):
            node.init = self.fix_async_func(node.init)
            node.cond = self.fix_async_func(node.cond)
            node.next = self.fix_async_func(node.next)
            node.stmt = self.fix_async_func(node.stmt)
        elif isinstance(node, c_ast.Switch):
            node.cond = self.fix_async_func(node.cond)
            node.stmt = self.fix_async_func(node.stmt)
        elif isinstance(node, c_ast.Compound):
            i = 0
            while i < len(node.block_items):
                node.block_items[i] = self.fix_async_func(node.block_items[i])
                if node.block_items[i] is None:
                    del node.block_items[i]
                else:
                    i += 1
        elif isinstance(node, c_ast.ArrayRef):
            node.name = self.fix_async_func(node.name)
            node.subscript = self.fix_async_func(node.subscript)
        elif isinstance(node, c_ast.StructRef):
            node.name = self.fix_async_func(node.name)
        elif isinstance(node, c_ast.ID):
            if node.name in self.func_async_state_decls:
                return c_ast.StructRef(
                    c_ast.ID(LambdaFuncTypeInfo.CLOSURE_DATA_LINK_NAME), '->',
                    c_ast.ID(node.name)
                )
        elif isinstance(node, c_ast.Return):
            if node.expr is not None:
                raise CodeSyntaxError('Async function cannot return value', node.coord)
            if node not in self.async_returns:
                return c_ast.Goto('__exit', node.coord)
        return node
