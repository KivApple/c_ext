import pycparserext.ext_c_lexer
try:
    from pycparser.ply.lex import TOKEN
except ImportError:
    from ply.lex import TOKEN


class LexerImproved(pycparserext.ext_c_lexer.GnuCLexer):
    def __init__(self, error_func, on_lbrace_func, on_rbrace_func,
                 type_lookup_func):
        self.keywords = list(self.keywords)
        self.keywords.append('VIRTUAL')
        self.keywords.append('YIELD')
        self.keyword_map['virtual'] = 'VIRTUAL'
        self.keyword_map['yield'] = 'YIELD'
        self.keywords = tuple(self.keywords)
        self.tokens = list(self.tokens)
        self.tokens.append('VIRTUAL')
        self.tokens.append('YIELD')
        self.tokens = tuple(self.tokens)
        super(LexerImproved, self).__init__(error_func, on_lbrace_func, on_rbrace_func,
                 type_lookup_func)

    @TOKEN(r'([a-zA-Z_$]|::)([0-9a-zA-Z_$]|::)*')
    def t_ID(self, t):
        t.value = tuple(t.value.split('::'))
        if len(t.value) == 1:
            t.value = t.value[0]
        return super(LexerImproved, self).t_ID(t)
