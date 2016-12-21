import pycparserext.ext_c_parser
from pycparser import c_ast
from .lexer import LexerImproved
try:
    import pycparser.ply.yacc as yacc
except ImportError:
    import ply.yacc as yacc


class ParserImproved(pycparserext.ext_c_parser.GnuCParser):
    def __init__(
            self,
            lex_optimize=False,
            lextab='lextab',
            yacc_optimize=False,
            yacctab='yacctab',
            yacc_debug=False,
            taboutputdir='',
            write_tables=False):
        self.lexer_class = LexerImproved
        self.clex = self.lexer_class(
            error_func=self._lex_error_func,
            on_lbrace_func=self._lex_on_lbrace_func,
            on_rbrace_func=self._lex_on_rbrace_func,
            type_lookup_func=self._lex_type_lookup_func)

        self.clex.build(
            optimize=lex_optimize,
            lextab=lextab,
            outputdir=taboutputdir
        )
        self.tokens = self.clex.tokens

        self.OPT_RULES.append('lambda_capture_list')
        self.OPT_RULES.append('lambda_storage_spec')

        for rule in self.OPT_RULES:
            self._create_opt_rule(rule)

        self.ext_start_symbol = "translation_unit_or_empty"

        self.cparser = yacc.yacc(
            module=self,
            start=self.ext_start_symbol,
            debug=yacc_debug,
            optimize=yacc_optimize,
            tabmodule=yacctab,
            outputdir=taboutputdir,
            write_tables=write_tables)

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

    def p_lambda_storage_spec(self, p):
        """ lambda_storage_spec : STATIC
        """
        p[0] = p[1]

    def p_lambda_capture_item(self, p):
        """ lambda_capture_item : ID
                                | AND ID
        """
        if len(p) == 3:
            p[0] = '&%s' % p[2]
        else:
            p[0] = p[1]

    def p_lambda_capture_list(self, p):
        """ lambda_capture_list : lambda_capture_list COMMA lambda_capture_item
                                | lambda_capture_item
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_lambda_func(self, p):
        """ lambda_func : lambda_storage_spec_opt LBRACKET lambda_capture_list_opt RBRACKET LPAREN parameter_type_list_opt RPAREN compound_statement
                        | lambda_storage_spec_opt LBRACKET lambda_capture_list_opt RBRACKET LPAREN parameter_type_list_opt RPAREN ARROW type_name compound_statement
        """
        if len(p) == 9:
            p[0] = LambdaFunc(
                p[6],
                c_ast.Typename(
                    None, list(),
                    c_ast.TypeDecl(None, list(), c_ast.IdentifierType(['void']))
                ),
                p[8],
                p[3],
                p[1],
                self._coord(p.lineno(1))
            )
        else:
            p[0] = LambdaFunc(
                p[6],
                p[9],
                p[10],
                p[3],
                p[1],
                self._coord(p.lineno(1))
            )

    def p_primary_expression_6(self, p):
        """ primary_expression : lambda_func
        """
        p[0] = p[1]

    def p_parameter_declaration_1(self, p):
        """ parameter_declaration   : declaration_specifiers declarator
                                    | declaration_specifiers declarator EQUALS constant_expression
        """
        super(ParserImproved, self).p_parameter_declaration_1(p)
        if len(p) == 5:
            p[0].init = p[4]

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


class LambdaFunc(c_ast.Node):
    def __init__(self, args, return_type, body, capture_list, storage, coord=None):
        self.args = args
        self.return_type = return_type
        self.body = body
        self.capture_list = capture_list
        self.storage = storage
        self.coord = coord

    def children(self):
        nodelist = list()
        if self.return_type is not None:
            nodelist.append(('return_type', self.return_type))
        if self.args is not None:
            nodelist.append(('args', self.args))
        if self.body is not None:
            nodelist.append(('body', self.body))
        return nodelist
