import pycparser.c_lexer


class LexerImproved(pycparser.c_parser.CLexer):
    def __init__(self, error_func, on_lbrace_func, on_rbrace_func,
                 type_lookup_func):
        self.keywords = list(self.keywords)
        self.keywords.append('VIRTUAL')
        self.keyword_map['virtual'] = 'VIRTUAL'
        self.keywords = tuple(self.keywords)
        self.tokens = list(self.tokens)
        self.tokens.append('VIRTUAL')
        self.tokens.append('DOUBLECOLON')
        self.tokens = tuple(self.tokens)
        self.t_DOUBLECOLON = '::'
        super(LexerImproved, self).__init__(error_func, on_lbrace_func, on_rbrace_func,
                 type_lookup_func)
