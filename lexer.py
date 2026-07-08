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
            if char == '"' or char == "'":
                quote = char
                value = self.read_string(quote)
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
            if char in '+-*/%=<>!&|^~(){}[];:,.':
                op = self.read_operator()
    
    # Map operator to token type
                op_map = {
        '+': 'TOK_PLUS',
        '-': 'TOK_MINUS',
        '*': 'TOK_STAR',
        '/': 'TOK_SLASH',
        '%': 'TOK_PERCENT',
        '=': 'TOK_ASSIGN',
        '<': 'TOK_LT',
        '>': 'TOK_GT',
        '!': 'TOK_NOT',
        '&': 'TOK_BITAND',
        '|': 'TOK_BITOR',
        '^': 'TOK_XOR',
        '~': 'TOK_TILDE',
        '(': 'TOK_LPAREN',
        ')': 'TOK_RPAREN',
        '{': 'TOK_LBRACE',
        '}': 'TOK_RBRACE',
        '[': 'TOK_LBRACKET',
        ']': 'TOK_RBRACKET',
        ';': 'TOK_SEMICOLON',
        ',': 'TOK_COMMA',
        '.': 'TOK_DOT',
        ':': 'TOK_COLON',
        '==': 'TOK_EQ',
        '!=': 'TOK_NE',
        '<=': 'TOK_LE',
        '>=': 'TOK_GE',
        '&&': 'TOK_AND',
        '||': 'TOK_OR',
        '++': 'TOK_INC',
        '--': 'TOK_DEC',
                }
    
                token_type = op_map.get(op, 'TOK_OPERATOR')
                self.add_token(token_type, op)
                continue
        
            self.advance()
    
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

    def read_string(self, quote='"'):
        string = ''
        self.advance()  # Skip opening quote
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '\\' and self.peek_char() == quote:
                string += quote
                self.advance()
                self.advance()
            else:
                string += self.current_char()
                self.advance()
        if self.current_char() == quote:
            self.advance()  # Skip closing quote
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
    
    # Two-char operators
        two_char = char + next_char
        if two_char in ['++', '--', '==', '!=', '<=', '>=', '&&', '||', '<<', '>>']:
            self.advance()
            self.advance()
            return two_char

        # Single-char operator
        self.advance()
        return char

    def add_token(self, type, value):
        self.token.append(Token(type, value, self.line, self.col))

class PyLexer(object):
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
            if char == '#':
                self.skipcomment()
                continue
        
        # Strings
            if char == '"' or char == "'" or (char == 'f' and self.peek_char() in ['"', "'"]):
                if char == 'f':
                    self.advance()  # skip 'f'
                    quote = self.current_char()  # get quote after f
                    value = self.read_fstring(quote)
                    self.add_token('TOK_FSTRING', value)
                else:
                    quote = char
                    value = self.read_string(quote)
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
                token_type = get_token_type(value, 'Python')  # from keywords.py
                self.add_token(token_type, value)
                continue
        
        # Operators & delimiters
            if char in '+-*/%=<>!&|^~()[];:,.':
                op = self.read_operator()
    
    # Map operator to token type
                op_map = {
        '+': 'TOK_PLUS',
        '-': 'TOK_MINUS',
        '*': 'TOK_STAR',
        '/': 'TOK_SLASH',
        '%': 'TOK_PERCENT',
        '=': 'TOK_ASSIGN',
        '<': 'TOK_LT',
        '>': 'TOK_GT',
        '!': 'TOK_NOT',
        '&': 'TOK_BITAND',
        '|': 'TOK_BITOR',
        '^': 'TOK_XOR',
        '~': 'TOK_TILDE',
        '(': 'TOK_LPAREN',
        ')': 'TOK_RPAREN',
        '{': 'TOK_LBRACE',
        '}': 'TOK_RBRACE',
        '[': 'TOK_LBRACKET',
        ']': 'TOK_RBRACKET',
        ';': 'TOK_SEMICOLON',
        ',': 'TOK_COMMA',
        '.': 'TOK_DOT',
        ':': 'TOK_COLON',
        '==': 'TOK_EQ',
        '!=': 'TOK_NE',
        '<=': 'TOK_LE',
        '>=': 'TOK_GE',
        '&&': 'TOK_AND',
        '||': 'TOK_OR',
        '++': 'TOK_INC',
        '--': 'TOK_DEC',
        }
        
                token_type = op_map.get(op, 'TOK_OPERATOR')
                self.add_token(token_type, op)
                continue
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
        if self.current_char() == '#':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            self.advance()  # Skip the newline
            return
    
    def read_string(self, quote='"'):
        string = ''
        self.advance()  # Skip opening quote
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '\\' and self.peek_char() == quote:
                string += quote
                self.advance()
                self.advance()
            else:
                string += self.current_char()
                self.advance()
        if self.current_char() == quote:
            self.advance()  # Skip closing quote
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

        # Two-char operators
        two_char = char + next_char
        if two_char in ['++', '--', '==', '!=', '<=', '>=', '&&', '||', '<<', '>>']:
            self.advance()
            self.advance()
            return two_char

        # Single-char operator
        self.advance()
        return char
    
    def read_fstring(self, quote='"'):
        f_string = ''
        self.advance()  # Skip the opening quote
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '{':
                f_string += '{'
                self.advance()
                while self.current_char() and self.current_char() != '}':
                    f_string += self.current_char()
                    self.advance()
                if self.current_char() == '}':
                    f_string += '}'
                    self.advance()
            else:
                f_string += self.current_char()
                self.advance()
        if self.current_char() == quote:
            self.advance()  # Skip the closing quote
        return f_string

    def add_token(self, type, value):
        self.token.append(Token(type, value, self.line, self.col))
        