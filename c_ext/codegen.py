from pycparser.c_generator import CGenerator as CGeneratorBaseBuggy


class CGeneratorBase(CGeneratorBaseBuggy):
    def __init__(self):
        super(CGeneratorBase, self).__init__()
        self.last_coord = None

    # bug fix
    def visit_UnaryOp(self, n):
        operand = self._parenthesize_unless_simple(n.expr)
        if n.op == 'p++':
            return '%s++' % operand
        elif n.op == 'p--':
            return '%s--' % operand
        elif n.op == 'sizeof':
            # Always parenthesize the argument of sizeof since it can be
            # a name.
            return 'sizeof(%s)' % self.visit(n.expr)
        else:
            # avoid merging of "- - x" or "__real__varname"
            return '%s %s' % (n.op, operand)
