INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type, value})'.format(type = self.type, value = self.value)

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.curr_token = None
        self.pos = 0
        self.currentchar = self.text[self.pos]

    def error(self):
        raise Exception('Syntax Error')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.currentchar = None
        else:
            self.currentchar = self.text[self.pos]

    def integer(self):
        res = ''
        while self.currentchar is not None and self.currentchar.isdigit():
            res += self.currentchar
            self.advance()
        return int(res)

    def space(self):
        while self.currentchar.isspace() and self.currentchar is not None:
            self.advance()

    def get_new_token(self):
        while self.currentchar is not None:
            if self.currentchar.isspace():
                self.space()
                continue
            if self.currentchar.isdigit():
                return Token(INTEGER, self.integer())
            if self.currentchar == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.currentchar == '-':
                self.advance()
                return Token(MINUS, '-')
            self.error()

        return Token(EOF, None)

    def eat(self, tokentype):
        if self.curr_token.type == tokentype:
            self.curr_token = self.get_new_token()
        else:
            self.error()
    def term(self):
        token = self.curr_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        self.curr_token = self.get_new_token()
        res = self.term()
        while self.curr_token.type in (PLUS, MINUS):
            token = self.curr_token
            if token.type == PLUS:
                self.eat(PLUS)
                res += self.term()
            if token.type == MINUS:
                self.eat(MINUS)
                res -= self.term()
        return res

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()