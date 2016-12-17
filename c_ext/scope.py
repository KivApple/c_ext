from collections import OrderedDict
from six import iteritems


class Scope:
    def __init__(self, *parents):
        self.parents = list(parents)
        self.symbols = OrderedDict()
        self.attrs = set()
        self.owner = None

    def add_symbol(self, name, symbol):
        self.symbols[name] = symbol

    def find_symbol(self, name, strict=False):
        symbol = self.symbols.get(name)
        if symbol is None:
            for parent in self.parents:
                if parent is None:
                    continue
                symbol = parent.find_symbol(name, strict)
                if symbol is not None:
                    break
                if strict:
                    break
        return symbol

    def __str__(self):
        s = ', '.join(['%s -> %s' % (name, value) for name, value in iteritems(self.symbols)])
        if len(self.parents) == 0:
            return s
        if self.parents[0] is None:
            return s
        ps = str(self.parents[0])
        if len(ps) == 0:
            return s
        return '%s, %s' % (s, ps)
