from .types import *


class Expression:
    def __init__(self, type_info, ast_node=None):
        self.type_info = type_info
        self.ast_node = ast_node


class ConstantExpression(Expression):
    def __init__(self, value, type, ast_node=None):
        self.value = value
        self.type = type
        Expression.__init__(self,
                            PtrTypeInfo(ScalarTypeInfo('char')) if type == 'string' else ScalarTypeInfo(type),
                            ast_node)

    def __str__(self):
        if self.type == 'string':
            return '"%s"' % self.value
        return self.value


class VariableExpression(Expression):
    def __init__(self, name, scope, ast_node=None):
        self.name = name
        self.scope = scope
        var_info = scope.find_symbol(name)
        if isinstance(var_info, VariableInfo):
            if isinstance(var_info.scope.owner, StructTypeInfo):
                if ('static' in var_info.storage) or isinstance(var_info.type, FuncTypeInfo):
                    ast_node.name = '%s_%s' % (var_info.scope.owner.name, name)
                else:
                    ast_node = c_ast.StructRef(
                        c_ast.ID('this'),
                        '->',
                        c_ast.ID(name),
                        ast_node.coord
                    )
            elif isinstance(var_info.scope.owner, LambdaFuncTypeInfo):
                if 'closure' in var_info.storage:
                    ast_node = c_ast.StructRef(
                        c_ast.ID('__closure_data'),
                        '->',
                        c_ast.ID(name),
                        ast_node.coord
                    )
                    if 'link' in var_info.attrs:
                        ast_node = c_ast.UnaryOp('*', ast_node, ast_node.coord)
            Expression.__init__(self, var_info.type, ast_node)
        else:
            Expression.__init__(self, None, ast_node)

    def __str__(self):
        return self.name


class UnaryExpression(Expression):
    def __init__(self, op, operand, ast_node=None):
        self.op = op
        self.operand = operand
        if op == 'sizeof':
            Expression.__init__(self, ScalarTypeInfo('int'), ast_node)
            return
        operand_type_info = operand.type_info
        ast_node.expr = operand.ast_node
        if op == '&':
            Expression.__init__(self, PtrTypeInfo(operand_type_info), ast_node)
        elif op == '*':
            assert isinstance(operand_type_info, PtrTypeInfo)
            Expression.__init__(self, operand_type_info.base_type, ast_node)
        else:
            Expression.__init__(self, operand_type_info, ast_node)

    def __str__(self):
        return '%s(%s)' % (self.op, self.operand)


class BinaryExpression(Expression):
    def __init__(self, op, left, right, ast_node=None):
        self.op = op
        self.left = left
        self.right = right
        left_type_info = left.type_info
        self.right = TypeInfo.make_safe_cast(right, left_type_info)
        if self.right is None:
            self.right = right # Warning
        if isinstance(ast_node, c_ast.Assignment):
            ast_node.lvalue = self.left.ast_node
            ast_node.rvalue = self.right.ast_node
        else:
            ast_node.left = self.left.ast_node
            ast_node.right = self.right.ast_node
        right_type_info = right.type_info
        if op in ('==', '!=', '>', '<', '>=', '<='):
            Expression.__init__(self, ScalarTypeInfo('_Bool'), ast_node)
        else:
            Expression.__init__(self, left_type_info, ast_node)

    def __str__(self):
        return '(%s) %s (%s)' % (self.left, self.op, self.right)


class TernaryExpression(Expression):
    def __init__(self, cond, true_value, false_value, ast_node=None):
        self.cond = cond
        self.true_value = true_value
        self.false_value = false_value
        ast_node.cond = self.cond.ast_node
        ast_node.iftrue = self.true_value.ast_node
        ast_node.iffalse = self.false_value.ast_node
        true_type_info = true_value.type_info
        false_type_info = false_value.type_info
        Expression.__init__(self, true_type_info, ast_node)

    def __str__(self):
        return '(%s) ? (%s) : (%s)' % (self.cond, self.true_value, self.false_value)


class CastExpression(Expression):
    def __init__(self, operand, type_info, ast_node=None):
        self.operand = operand
        self.type_info = type_info
        ast_node.expr = operand.ast_node
        Expression.__init__(self, type_info, ast_node)

    def __str__(self):
        return 'TypeCast(%s, %s)' % (self.operand, self.type_info)


class SubscriptExpression(Expression):
    def __init__(self, array, index, ast_node=None):
        self.array = array
        self.index = index
        ast_node.name = array.ast_node
        assert isinstance(array.type_info, (ArrayTypeInfo, PtrTypeInfo))
        Expression.__init__(self, array.type_info.base_type, ast_node)

    def __str__(self):
        return '%s[%s]' % (self.array, self.index)


class MemberExpression(Expression):
    def __init__(self, value, member_name, type, ast_node=None):
        self.value = value
        self.member_name = member_name
        self.type = type
        ast_node.name = value.ast_node
        type_info = self.value.type_info
        if type == '->':
            if isinstance(type_info, PtrTypeInfo):
                type_info = type_info.base_type
            else:
                type_info = None
        self.struct_type_info = type_info
        if isinstance(type_info, StructTypeInfo):
            assert type_info.scope is not None
            type_info = type_info.scope.find_symbol(
                member_name[-1] if isinstance(member_name, tuple) else member_name, True
            )
            if isinstance(type_info, VariableInfo):
                type_info = type_info.type
                ast_node_ = self.struct_type_info.fix_member_access(ast_node)
                value.ast_node = ast_node.name
                ast_node = ast_node_
            else:
                type_info = None
        Expression.__init__(self, type_info, ast_node)

    def __str__(self):
        return '(%s)%s%s' % (self.value, self.type, self.member_name)


class CallExpression(Expression):
    cur_closure_func_id = 0

    def __init__(self, value, args, ast_node, ast_transformer):
        self.ast_tranformer = ast_transformer
        self.value = value
        self.args = args
        ast_node.name = value.ast_node
        type_info = self.value.type_info
        if isinstance(type_info, PtrTypeInfo):
            type_info = type_info.base_type
        if isinstance(type_info, PtrTypeInfo):
            type_info = type_info.base_type
            tmp_name = '__tmp_closure_%s__' % CallExpression.cur_closure_func_id
            CallExpression.cur_closure_func_id += 1
            type_decl = PtrTypeInfo(PtrTypeInfo(type_info)).to_decl()
            type_decl.type.type.type.declname = tmp_name
            ast_transformer.schedule_tmp_decl(
                c_ast.Decl(
                    tmp_name,
                    list(),
                    list(),
                    list(),
                    type_decl,
                    value.ast_node,
                    None
                )
            )
            tmp_ast_node = c_ast.ID(tmp_name, None)
            ast_node.name = tmp_ast_node
            from .scope import Scope
            args.insert(0, VariableExpression(tmp_name, Scope(), tmp_ast_node))
            args[0].type_info = PtrTypeInfo(ScalarTypeInfo('void'))
            if ast_node.args is None:
                ast_node.args = c_ast.ExprList(list())
            ast_node.args.exprs.insert(0, tmp_ast_node)
            ast_node.name = c_ast.UnaryOp('*', ast_node.name, ast_node.name.coord)
        if isinstance(type_info, FuncTypeInfo):
            i = 0
            if type_info.args and (type_info.args[0].name == 'this'):
                if ast_node.args is None:
                    ast_node.args = c_ast.ExprList(list())
                if isinstance(value, MemberExpression):
                    assert isinstance(value.struct_type_info, StructTypeInfo)
                    if value.type == '.':
                        args.insert(0, UnaryExpression('&', value.value, c_ast.UnaryOp('&', value.ast_node)))
                    else:
                        args.insert(0, value.value)
                    ast_node.args.exprs.insert(0, args[0].ast_node)
                else:
                    ast_node.args.exprs.insert(0, c_ast.ID('this'))
                    args.insert(0, VariableExpression('this', ast_transformer.scope, ast_node.args.exprs[0]))
            args_types = [arg.type_info for arg in args]
            while i < len(args_types):
                src_arg_type = args_types[i]
                if i >= len(type_info.args):
                    break
                if type_info.args[i] is None:
                    break
                dst_arg_type = type_info.args[i].type_info
                casted = TypeInfo.make_safe_cast(args[i], dst_arg_type)
                if casted is None:
                    casted = args[i] # Warning
                ast_node.args.exprs[i] = casted.ast_node
                i += 1
            while i < len(args):
                ast_node.args.exprs[i] = args[i].ast_node
                i += 1
            while i < len(type_info.args):
                if type_info.args[i] is None:
                    break
                default_value = type_info.args[i].default_value
                if default_value is not None:
                    if ast_node.args is None:
                        ast_node.args = c_ast.ExprList(list())
                    ast_node.args.exprs.append(default_value.ast_node)
                else:
                    break
                i += 1
            if i == len(type_info.args) - 1:
                if isinstance(type_info.return_type, ScalarTypeInfo) and type_info.return_type.name == 'void':
                    last_arg = type_info.args[i]
                    if isinstance(last_arg, FuncArgInfo):
                        if isinstance(last_arg.type_info, PtrTypeInfo):
                            if isinstance(last_arg.type_info.base_type, PtrTypeInfo):
                                if isinstance(last_arg.type_info.base_type.base_type, FuncTypeInfo):
                                    if len(last_arg.type_info.base_type.base_type.args) == 1:
                                        callback_arg = last_arg.type_info.base_type.base_type.args[0]
                                        if isinstance(callback_arg.type_info, PtrTypeInfo):
                                            if isinstance(callback_arg.type_info.base_type, ScalarTypeInfo):
                                                if callback_arg.type_info.base_type.name == 'void':
                                                    if ast_node.args is None:
                                                        ast_node.args = c_ast.ExprList(list())
                                                    ast_node.args.exprs.append(
                                                        c_ast.ID(LambdaFuncTypeInfo.CLOSURE_LINK_NAME)
                                                    )
                                                    ast_transformer.need_async_call = True
            Expression.__init__(self, type_info.return_type, ast_node)
        else:
            Expression.__init__(self, None, ast_node)

    def __str__(self):
        return '%s(%s)' % (self.value, ', '.join([str(arg) for arg in self.args]))


class LambdaFuncExpression(Expression):
    def __init__(self, type_info, ast_node):
        Expression.__init__(self, type_info, ast_node)
