class CodeSyntaxError(Exception):
    def __init__(self, message, coord=None):
        self.message = message
        self.coord = coord

    def __str__(self):
        if self.coord is None:
            return self.message
        return '%s:%s: %s' % (self.coord.file, self.coord.line, self.message)
