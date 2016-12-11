import pycparser.c_parser
from pycparser import c_ast
from .lexer import LexerImproved
try:
    import pycparser.ply.yacc as yacc
except ImportError:
    import ply.yacc as yacc


class ParserImproved(pycparser.c_parser.CParser):
    def __init__(self, **kwargs):
        kwargs['lex_optimize'] = kwargs.get('lex_optimize', False)
        kwargs['yacc_optimize'] = kwargs.get('yacc_optimize', False)
        kwargs['lexer'] = kwargs.get('lexer', LexerImproved)
        super(ParserImproved, self).__init__(**kwargs)

    def p_storage_class_specifier(self, p):
        """ storage_class_specifier : AUTO
                                    | REGISTER
                                    | STATIC
                                    | EXTERN
                                    | VIRTUAL
                                    | TYPEDEF
        """
        p[0] = p[1]

    def p_struct_declaration_1(self, p):
        """ struct_declaration : specifier_qualifier_list struct_declarator_list_opt SEMI
                               | storage_class_specifier specifier_qualifier_list struct_declarator_list_opt SEMI
        """
        if len(p) == 5:
            new_p = [p[0], p[2], p[3], p[4]]
            super(ParserImproved, self).p_struct_declaration_1(new_p)
            p[0] = new_p[0]
            for decl in p[0]:
                decl.storage.append(p[1])
        else:
            super(ParserImproved, self).p_struct_declaration_1(p)

    def p_struct_declaration_2(self, p):
        """ struct_declaration : specifier_qualifier_list abstract_declarator SEMI
                               | storage_class_specifier specifier_qualifier_list abstract_declarator SEMI
        """
        if len(p) == 5:
            new_p = [p[0], p[2], p[3], p[4]]
            super(ParserImproved, self).p_struct_declaration_2(p)
            p[0] = new_p[0]
            for decl in p[0]:
                decl.storage.append(p[1])
        else:
            super(ParserImproved, self).p_struct_declaration_2(p)

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

    def p_identifier(self, p):
        """ identifier  : TYPEID DOUBLECOLON ID
                        | ID DOUBLECOLON ID
                        | ID
        """
        if len(p) == 4:
            p[0] = c_ast.ID(p[3], self._coord(p.lineno(1)))
        else:
            p[0] = c_ast.ID(p[1], self._coord(p.lineno(1)))

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
