import pycparser.c_parser
import pycparser.c_lexer
from pycparser import c_ast
try:
    import pycparser.ply.yacc as yacc
except ImportError:
    import ply.yacc as yacc


class ParserImproved(pycparser.c_parser.CParser):
    def __init__(self):
        super(ParserImproved, self).__init__(yacc_optimize=False)

    def p_struct_or_union_specifier_4(self, p):
        """
        struct_or_union_specifier : struct_or_union ID COLON ID brace_open struct_declaration_list brace_close
                                  | struct_or_union TYPEID COLON ID \
                                          brace_open struct_declaration_list brace_close
                                  | struct_or_union ID COLON TYPEID brace_open struct_declaration_list brace_close
                                  | struct_or_union TYPEID COLON TYPEID \
                                          brace_open struct_declaration_list brace_close
        """
        if p[1] != 'struct':
            self.error(p, 'Only structure inheritance supported')
        p[0] = StructImproved(
            name=p[2],
            decls=p[6],
            parent=p[4],
            coord=self._coord(p.lineno(2))
        )

    def error(self, p, msg=None):
        if p:
            self._parse_error(
                'before: %s' % p.value if msg is None else msg,
                self._coord(lineno=p.lineno,
                            column=self.clex.find_tok_column(p)))
        else:
            self._parse_error('At end of input', self.clex.filename)


class StructImproved(c_ast.Struct):
    def __init__(self, name, decls, parent, coord=None):
        super(StructImproved, self).__init__(name, decls, coord)
        self.parent = parent
