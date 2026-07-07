from keywords import get_token_type
from token import Token
class CLexer(object):
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line = 1
        self.col = 1
        self.token = []
    
    def tokenize(self):
        while self.pos < len(self.code):
            self.skipspace()
        
            if self.pos >= len(self.code):
                break
        
            char = self.current_char()
        
        # Comments
            if char == '/' and self.peek_char() in ['/', '*']:
                self.skipcomment()
                continue
        
        # Strings
            if char == '"':
                value = self.read_string()
                self.add_token('TOK_STRING', value)
                continue
        
        # Numbers
            if char.isdigit():
                value = self.read_number()
                self.add_token('TOK_NUMBER', str(value))
                continue
        
        # Identifiers & keywords
            if char.isalpha() or char == '_':
                value = self.read_identifier()
                token_type = get_token_type(value, 'C')  # from keywords.py
                self.add_token(token_type, value)
                continue
        
        # Operators & delimiters
            if char in '+-*/%=<>!&|^~(){}[];:,.\n':
                value = self.read_operator()
                self.add_token('TOK_OPERATOR', value)
                continue
        
        # Unknown char
            self.advance()
    
    # Add EOF token
        self.add_token('TOK_EOF', '')
        return self.token

    def current_char(self):
        if self.pos >= len(self.code):
            return ''
        return self.code[self.pos]

    def peek_char(self):
        if self.pos + 1 < len(self.code):
            return self.code[self.pos + 1]
        else:
            return ''
    
    def advance(self):
        if self.current_char() == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        self.pos += 1

    def skipspace(self):
        while self.current_char() and self.current_char().isspace():
            self.advance()

    def skipcomment(self):
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            self.advance() 
            return()

        if self.current_char() == '/' and self.peek_char() == '*':
            self.advance()
            self.advance()
            while self.current_char() and not (self.current_char() == '*' and self.peek_char() == '/'):
                if self.current_char() == '\n':
                    self.line += 1
                    self.col = 1
                else:
                    self.col += 1
                self.pos += 1
            if self.current_char() == '*' and self.peek_char() == '/':
                self.advance()
                self.advance()
            return()

    def read_string(self):
        string = ''
        self.advance()  # Skip the opening quote
        while self.current_char() and self.current_char() != '"':
            if self.current_char() == '\\' and self.peek_char() == '"':
                string += '"'
                self.advance()
                self.advance()
            else:
                string += self.current_char()
                self.advance()
        if self.current_char() == '"':
            self.advance()  # Skip the closing quote
        return string

    def read_number(self):
        number = ''
        while self.current_char() and self.current_char().isdigit():
            number += self.current_char()
            self.advance()
    
        if self.current_char() == '.' and self.peek_char().isdigit():
            number += self.current_char()
            self.advance()
            while self.current_char() and self.current_char().isdigit():
                number += self.current_char()
                self.advance()
            return float(number)
    
        return int(number)

    def read_identifier(self):
        identifier = ''
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            identifier += self.current_char()
            self.advance()
        return identifier

    def read_operator(self):
        char = self.current_char()
        next_char = self.peek_char()
        
        twochar = char + next_char
        if twochar in ['++', '--', '==', '!=', '<=', '>=', '&&', '||', '+=', '-=', '*=', '/=', '%=']:
            self.advance()
            self.advance()
            return twochar
        else:
            self.advance()
            return char

    def add_token(self, type, value):
        self.token.append(Token(type, value, self.line, self.col))