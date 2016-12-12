import pycparserext.ext_c_parser
from pycparser import c_ast
from .lexer import LexerImproved
try:
    import pycparser.ply.yacc as yacc
except ImportError:
    import ply.yacc as yacc


class ParserImproved(pycparserext.ext_c_parser.GnuCParser):
    def __init__(self, **kwargs):
        self.lexer_class = LexerImproved
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
            storage_specs = p[1]
            del p.slice[1]
            super(ParserImproved, self).p_struct_declaration_1(p)
            for decl in p[0]:
                decl.storage.append(storage_specs)
        else:
            super(ParserImproved, self).p_struct_declaration_1(p)

    def p_struct_declaration_2(self, p):
        """ struct_declaration : specifier_qualifier_list abstract_declarator SEMI
                               | storage_class_specifier specifier_qualifier_list abstract_declarator SEMI
        """
        if len(p) == 5:
            storage_specs = p[1]
            del p.slice[1]
            super(ParserImproved, self).p_struct_declaration_2(p)
            for decl in p[0]:
                decl.storage.append(storage_specs)
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

    def p_struct_declarator_1(self, p):
        """ struct_declarator : declarator EQUALS constant_expression
                              | declarator
        """
        if len(p) == 2:
            p[0] = {'decl': p[1], 'bitsize': None}
        else:
            p[0] = {'decl': p[1], 'bitsize': None, 'init': p[3]}

    def p_identifier(self, p):
        """ identifier  : TYPEID DOUBLECOLON ID
                        | ID DOUBLECOLON ID
                        | ID
        """
        if len(p) == 4:
            p[0] = c_ast.ID((p[1], p[3]), self._coord(p.lineno(1)))
        else:
            p[0] = c_ast.ID(p[1], self._coord(p.lineno(1)))

    def p_direct_declarator_1(self, p):
        """ direct_declarator   : identifier
        """
        p[0] = c_ast.TypeDecl(
            declname=p[1].name,
            type=None,
            quals=None,
            coord=self._coord(p.lineno(1)))

    def p_postfix_expression_4(self, p):
        """ postfix_expression  : postfix_expression PERIOD identifier
                                | postfix_expression PERIOD TYPEID
                                | postfix_expression ARROW identifier
                                | postfix_expression ARROW TYPEID
        """
        field = c_ast.ID(p[3], self._coord(p.lineno(3))) if isinstance(p[3], str) else p[3]
        p[0] = c_ast.StructRef(p[1], p[2], field, p[1].coord)

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
