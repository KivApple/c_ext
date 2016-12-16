import copy
from collections import OrderedDict
from six import iteritems

import pycparser.c_ast as c_ast
from pycparserext.ext_c_parser import TypeDeclExt, ArrayDeclExt, FuncDeclExt

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
        self.structs_with_declared_methods = set()
        self.node_path = list()
        self.cur_lambda_id = 0
        self.lambdas_capture_lists = dict()

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
        args_types = list()
        args = OrderedDict()
        if node.args is not None:
            for arg_decl in node.args.params:
                if isinstance(arg_decl, c_ast.Decl):
                    arg_type_info = self.visit(arg_decl.type)
                    args_types.append(arg_type_info)
                    if arg_decl.name is not None:
                        args[arg_decl.name] = arg_type_info
                elif isinstance(arg_decl, c_ast.Typename):
                    arg_type_info = self.visit(arg_decl.type)
                    args_types.append(arg_type_info)
                    if arg_decl.name is not None:
                        args[arg_decl.name] = arg_type_info
                elif isinstance(arg_decl, c_ast.EllipsisParam):
                    args_types.append(None)
                    break
        type_info = FuncTypeInfo(return_type, args_types, args)
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
                            tmp = symbol.type
                            if not isinstance(tmp, PtrTypeInfo):
                                tmp = PtrTypeInfo(tmp)
                            if TypeInfo.is_compatible(type_info, tmp):
                                fail = False
                if fail:
                    raise CodeSyntaxError('Symbol %s already defined in current scope' % node.name, node.coord)
            var_info = VariableInfo(node.name, type_info, node.storage, coord=node.coord)
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
        free = True
        if (len(self.node_path) > 0) and isinstance(self.node_path[-1], c_ast.StructRef):
            if self.node_path[-1].name != node:
                free = False
        if free and ('member' in self.scope.attrs):
            symbol_name = node.name
            symbol_scope = self.scope
            struct_type_info = None
            if isinstance(node.name, tuple):
                assert len(node.name) == 2
                struct_type_info = self.scope.find_symbol('struct %s' % node.name[0])
                if not isinstance(struct_type_info, StructTypeInfo):
                    raise CodeSyntaxError('%s is not a structure name' % node.name[0], node)
                symbol_scope = struct_type_info.scope
                symbol_name = node.name[1]
            symbol = symbol_scope.find_symbol(symbol_name, True)
            if isinstance(symbol, VariableInfo):
                if 'member' in symbol.attrs:
                    this_ptr = VariableExpression('this', self.scope, c_ast.ID('this', node.coord))
                    return MemberExpression(
                        this_ptr,
                        node.name,
                        '->',
                        c_ast.StructRef(this_ptr.ast_node, '->', c_ast.ID(node.name, node.coord), node.coord)
                    )
        if free:
            i = len(self.node_path) - 1
            while i >= 0:
                n = self.node_path[i]
                if isinstance(n, c_ast.FuncDef):
                    capture_list = self.lambdas_capture_lists.get(n.decl.name, list())
                    for capture_item in capture_list:
                        link = capture_item[0] == '&'
                        if link:
                            capture_item = capture_item[1:]
                        if capture_item == node.name:
                            closure_ptr = VariableExpression(
                                '__closure_data__',
                                self.scope,
                                c_ast.ID('__closure_data__')
                            )
                            val = MemberExpression(
                                closure_ptr,
                                node.name,
                                '->',
                                c_ast.StructRef(closure_ptr.ast_node, '->', c_ast.ID(node.name))
                            )
                            if link:
                                val = UnaryExpression('*', val, c_ast.UnaryOp('*', val.ast_node))
                            return val
                    break
                i -= 1
        return VariableExpression(node.name, self.scope, node)

    def visit_UnaryOp(self, node):
        assert isinstance(node, c_ast.UnaryOp)
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
            i = 0
            while i < len(node.block_items):
                retval = self.visit(node.block_items[i])
                if isinstance(retval, Expression):
                    node.block_items[i] = retval.ast_node
                for decl in self.scheduled_tmp_decls:
                    node.block_items.insert(i, decl)
                    i += 1
                self.scheduled_tmp_decls.clear()
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
        assert isinstance(var_info.type, FuncTypeInfo)
        for name, type_info in iteritems(var_info.type.args):
            self.scope.add_symbol(name, VariableInfo(name, type_info, list()))
        if isinstance(name_, tuple):
            assert len(name_) == 2
            type_info = self.scope.find_symbol('struct %s' % name_[0])
            if isinstance(type_info, StructTypeInfo):
                self.scope.parents.insert(0, type_info.scope)
                self.scope.attrs.add('member')
                type_info.fix_func_implementation(node, name_[1], self)
            else:
                raise CodeSyntaxError('%s is not a structure name' % name_[0], node.coord)
        self.split_async_func(node)
        self.visit(node.body)
        self.scope = prev_scope

    def visit_LambdaFunc(self, node):
        assert isinstance(node, LambdaFunc)
        func_name = '__lambda_%s__' % (self.cur_lambda_id)
        self.lambdas_capture_lists[func_name] = node.capture_list
        self.cur_lambda_id += 1
        prev_scope = self.scope
        self.scope = Scope(self.scope)
        return_type_info = self.visit(node.return_type)
        args_types = list()
        if node.args:
            for arg in node.args.params:
                if isinstance(arg, c_ast.Decl):
                    args_types.append(self.visit(arg.type))
                elif isinstance(arg, c_ast.Typename):
                    args_types.append(self.visit(arg.type))
                elif isinstance(arg, c_ast.EllipsisParam):
                    args_types.append(None)
        self.scope = prev_scope
        type_info = LambdaFuncTypeInfo(func_name, return_type_info, args_types, node, self)
        return LambdaFuncExpression(type_info, node)

    def schedule_decl(self, decl, prepend=False):
        if not isinstance(decl, (list, tuple)):
            assert decl is not None
            self.scheduled_decls.append((decl, prepend))
        else:
            self.scheduled_decls += [(d, prepend) for d in decl]

    def schedule_tmp_decl(self, decl):
        self.scheduled_tmp_decls.append(decl)

    def split_async_func(self, node):
        pass
