import pycparser.c_ast as c_ast
from pycparserext.ext_c_generator import GnuCGenerator


class CodeGenerator(GnuCGenerator):
    def __init__(self, emit_line_numbers=True):
        super(CodeGenerator, self).__init__()
        self.cur_filename = None
        self.cur_line_number = 0
        self.emit_line_numbers = emit_line_numbers

    def visit_FileAST(self, n):
        s = ''
        for ext in n.ext:
            s += self.emit_line_number(ext)
            if isinstance(ext, c_ast.FuncDef):
                s += self.visit(ext)
            elif isinstance(ext, c_ast.Pragma):
                s += self.visit(ext) + '\n'
                self.cur_line_number += 1
            else:
                s += self.visit(ext) + ';\n'
                self.cur_line_number += 1
        return s

    def visit_FuncDef(self, n):
        s = self.visit(n.decl)
        self.indent_level = 0
        s += '\n'
        self.cur_line_number += 1
        param_decls = list()
        if n.param_decls:
            for p in n.param_decls:
                param_decls.append(self.visit(p))
                self.cur_line_number += 1
            s += ';\n'.join(param_decls) + ';\n'
        s += self.visit(n.body)
        s += '\n'
        self.cur_line_number += 1
        return s

    def visit_Compound(self, n):
        s = self._make_indent() + '{\n'
        self.cur_line_number += 1
        self.indent_level += 2
        if n.block_items:
            s += ''.join(self._generate_stmt(stmt) for stmt in n.block_items)
        self.indent_level -= 2
        s += self._make_indent() + '}\n'
        self.cur_line_number += 1
        return s

    def visit_If(self, n):
        s = 'if ('
        if n.cond: s += self.visit(n.cond)
        s += ')\n'
        self.cur_line_number += 1
        s += self._generate_stmt(n.iftrue, add_indent=True)
        if n.iffalse:
            s += self._make_indent() + 'else\n'
            self.cur_line_number += 1
            s += self._generate_stmt(n.iffalse, add_indent=True)
        return s

    def visit_For(self, n):
        s = 'for ('
        if n.init: s += self.visit(n.init)
        s += ';'
        if n.cond: s += ' ' + self.visit(n.cond)
        s += ';'
        if n.next: s += ' ' + self.visit(n.next)
        s += ')\n'
        self.cur_line_number += 1
        s += self._generate_stmt(n.stmt, add_indent=True)
        return s

    def visit_While(self, n):
        s = 'while ('
        if n.cond: s += self.visit(n.cond)
        s += ')\n'
        self.cur_line_number += 1
        s += self._generate_stmt(n.stmt, add_indent=True)
        return s

    def visit_DoWhile(self, n):
        s = 'do\n'
        self.cur_line_number += 1
        s += self._generate_stmt(n.stmt, add_indent=True)
        s += self._make_indent() + 'while ('
        if n.cond: s += self.visit(n.cond)
        s += ');'
        return s

    def visit_Switch(self, n):
        s = 'switch (' + self.visit(n.cond) + ')\n'
        self.cur_line_number += 1
        s += self._generate_stmt(n.stmt, add_indent=True)
        return s

    def visit_Case(self, n):
        s = 'case ' + self.visit(n.expr) + ':\n'
        self.cur_line_number += 1
        for stmt in n.stmts:
            s += self._generate_stmt(stmt, add_indent=True)
        return s

    def visit_Default(self, n):
        s = 'default:\n'
        self.cur_line_number += 1
        for stmt in n.stmts:
            s += self._generate_stmt(stmt, add_indent=True)
        return s

    def visit_Label(self, n):
        s = n.name + ':\n' + self._generate_stmt(n.stmt)
        self.cur_line_number += 1
        return s

    def _generate_struct_union(self, n, name):
        s = name + ' ' + (n.name or '')
        if n.decls:
            s += '\n'
            self.cur_line_number += 1
            s += self._make_indent()
            self.indent_level += 2
            s += '{\n'
            self.cur_line_number += 1
            for decl in n.decls:
                s += self._generate_stmt(decl)
            self.indent_level -= 2
            s += self._make_indent() + '}'
        return s

    def _generate_stmt(self, n, add_indent=False):
        s = self.emit_line_number(n)
        s += super(CodeGenerator, self)._generate_stmt(n, add_indent)
        if (len(s) > 0) and (s[-1] == '\n'):
            self.cur_line_number += 1
        return s

    def emit_line_number(self, n):
        if not self.emit_line_numbers:
            return ''
        if n is None:
            return ''
        if (n.coord.line != self.cur_line_number) or (n.coord.file != self.cur_filename):
            self.cur_filename = n.coord.file
            self.cur_line_number = n.coord.line
            return '#line %s "%s"\n' % (self.cur_line_number, self.cur_filename)
        return ''
