class Token(object):
    def __init__(self, type, value, line, col):
        self.type = type
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        return 'Token({type, value, line, col})'.format(
            type = self.type, value = self.value, line = self.line, col = self.col)

    