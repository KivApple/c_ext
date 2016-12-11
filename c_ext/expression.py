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
        assert isinstance(var_info, VariableInfo)
        Expression.__init__(self, var_info.type, ast_node)

    def __str__(self):
        return self.name


class UnaryExpression(Expression):
    def __init__(self, op, operand, ast_node=None):
        self.op = op
        self.operand = operand
        operand_type_info = operand.type_info
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
        assert isinstance(self.right, Expression)
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
        true_type_info = true_value.type_info
        false_type_info = false_value.type_info
        Expression.__init__(self, true_type_info, ast_node)

    def __str__(self):
        return '(%s) ? (%s) : (%s)' % (self.cond, self.true_value, self.false_value)


class CastExpression(Expression):
    def __init__(self, operand, type_info, ast_node=None):
        self.operand = operand
        self.type_info = type_info
        Expression.__init__(self, type_info, ast_node)

    def __str__(self):
        return 'TypeCast(%s, %s)' % (self.operand, self.type_info)


class SubscriptExpression(Expression):
    def __init__(self, array, index, ast_node=None):
        self.array = array
        self.index = index
        assert isinstance(array.type_info, ArrayTypeInfo)
        Expression.__init__(self, array.type_info.base_type, ast_node)

    def __str__(self):
        return '%s[%s]' % (self.array, self.index)


class MemberExpression(Expression):
    def __init__(self, value, member_name, type, ast_node=None):
        self.value = value
        self.member_name = member_name
        self.type = type
        type_info = self.value.type_info
        if type == '->':
            assert isinstance(type_info, PtrTypeInfo)
            type_info = type_info.base_type
        assert isinstance(type_info, StructTypeInfo)
        assert type_info.scope is not None
        type_info = type_info.scope.find_symbol(member_name)
        assert type_info is not None
        Expression.__init__(self, type_info, ast_node)

    def __str__(self):
        return '(%s)%s%s' % (self.value, self.type, self.member_name)


class CallExpression(Expression):
    def __init__(self, value, args, ast_node=None):
        self.value = value
        self.args = args
        type_info = self.value.type_info
        if isinstance(type_info, PtrTypeInfo):
            type_info = type_info.base_type
        assert isinstance(type_info, FuncTypeInfo)
        args_types = [arg.type_info for arg in args]
        i = 0
        while i < len(args_types):
            src_arg_type = args_types[i]
            assert i < len(type_info.args_types)
            dst_arg_type = type_info.args_types[i]
            if dst_arg_type is None:
                break
            casted = TypeInfo.make_safe_cast(args[i], dst_arg_type)
            assert isinstance(casted, Expression)
            if ast_node is not None:
                ast_node.args.exprs[i] = casted.ast_node
            i += 1
        Expression.__init__(self, type_info.return_type, ast_node)

    def __str__(self):
        return '%s(%s)' % (self.value, ', '.join([str(arg) for arg in self.args]))
