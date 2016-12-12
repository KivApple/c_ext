import copy
from collections import OrderedDict
from six import iteritems
import pycparser.c_ast as c_ast
from .parser import StructImproved
from .scope import Scope
from .types import *
from .expression import *


class ASTTransformer(c_ast.NodeVisitor):
    def __init__(self):
        self.scope = None
        self.methods_decls = list()
        self.structs_with_declared_methods = set()

    def visit_FileAST(self, node):
        self.scope = Scope(self.scope)
        new_ext = list()
        for decl in node.ext:
            self.visit(decl)
            new_ext.append(decl)
            for method_decl in self.methods_decls:
                new_ext.append(method_decl)
            self.methods_decls.clear()
        node.ext = new_ext
        self.scope = self.scope.parents[0]

    def visit_IdentifierType(self, node):
        assert isinstance(node, c_ast.IdentifierType)
        full_type_name = ' '.join(node.names)
        type_info = self.scope.find_symbol(full_type_name)
        if type_info is not None:
            assert isinstance(type_info, TypeInfo)
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
            assert isinstance(parent, StructTypeInfo)
        type_info = None
        if node.name is not None:
            type_info = self.scope.find_symbol('%s %s' % (kind, node.name))
        if type_info is None:
            type_info = StructTypeInfo(kind, node.name)
            type_info.scope = Scope()
            if node.name is not None:
                self.scope.add_symbol('%s %s' % (kind, node.name), type_info)
        if (node.decls is not None) and (len(type_info.scope.parents) == 0):
            prev_scope = self.scope
            self.scope = type_info.scope
            self.scope.parents.append(parent.scope if parent is not None else None)
            self.scope.parents.append(prev_scope)
            self.generic_visit(node)
            type_info.parent = parent
            type_info.scope = self.scope
            type_info.ast_node = node
            self.scope = prev_scope
            methods_decls = type_info.make_methods_decls()
            if methods_decls:
                assert type_info.name is not None
                assert self.scope.parents[0] is None
                self.methods_decls += methods_decls
        return type_info

    def visit_TypeDecl(self, node):
        assert isinstance(node, c_ast.TypeDecl)
        type_info = self.visit(node.type)
        if isinstance(node.type, c_ast.Struct):
            node.type = type_info.to_ast(node.type.decls is not None)
        type_info = type_info.clone()
        type_info.quals += node.quals
        return type_info

    def visit_ArrayDecl(self, node):
        assert isinstance(node, c_ast.ArrayDecl)
        type_info = self.visit(node.type)
        dim = None
        if node.dim is not None:
            dim = self.visit(node.dim)
        return ArrayTypeInfo(type_info, dim)

    def visit_FuncDecl(self, node):
        assert isinstance(node, c_ast.FuncDecl)
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
            assert isinstance(struct_type_info, StructTypeInfo)
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
            node.type = type_info.to_ast(node.type.decls is not None)
        var_info = None
        if node.name is not None:
            var_info = VariableInfo(node.name, type_info, node.storage)
            self.scope.add_symbol(node.name, var_info)
            if node.init is not None:
                init = self.visit(node.init)
                init = TypeInfo.make_safe_cast(init, type_info)
                if init is not None:
                    node.init = init.ast_node
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
        return SubscriptExpression(self.visit(node.name), self.visit(node.subscript))

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
        return CallExpression(func, args, node)

    def visit_Assignment(self, node):
        assert isinstance(node, c_ast.Assignment)
        return BinaryExpression(node.op, self.visit(node.lvalue), self.visit(node.rvalue), node)

    def visit_FuncDef(self, node):
        assert isinstance(node, c_ast.FuncDef)
        var_info = self.visit(node.decl)
        prev_scope = self.scope
        self.scope = Scope(self.scope)
        assert isinstance(var_info.type, FuncTypeInfo)
        for name, type_info in iteritems(var_info.type.args):
            self.scope.add_symbol(name, VariableInfo(name, type_info, list()))
        self.visit(node.body)
        self.scope = prev_scope
