from ast_nodes import *
class CParser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            return Token('TOK_EOF', '', -1, -1)

    def peek_token(self, offset=1):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        else:
            return Token('TOK_EOF', '', -1, -1)

    def advance(self):
        self.pos += 1

    def is_at_end(self):
        return self.current_token().type == 'TOK_EOF'

    def expect(self, token_type):
        if self.current_token().type == token_type:
            token = self.current_token()
            self.advance()
            return token
        else:
            raise SyntaxError("Expected token type {}, but got {} at line {}, col {}".format(
                token_type, self.current_token().type, self.current_token().line, self.current_token().col))
    
    def match(self, *token_types):
        if self.current_token().type in token_types:
            self.advance()
            return True
        return False

    def consume(self, token_type, message):
        if self.current_token().type == token_type:
            token = self.current_token()
            self.advance()
            return token
        else:
            raise SyntaxError(message + " at line {}, col {}".format(
                self.current_token().line, self.current_token().col))
    def parse(self):
        ast = []
        while not self.is_at_end():
            stmt = self.parse_statement()
            if stmt is not None:
                ast.append(stmt)
        return ast

    def parse_statement(self):
        token_type = self.current_token().type
        if token_type in ['TOK_INT', 'TOK_CHAR', 'TOK_FLOAT', 'TOK_DOUBLE', 'TOK_VOID'] and self.peek_token(1).type == 'TOK_IDENTIFIER' and self.peek_token(2).type == 'TOK_LPAREN':
            return self.parse_function_def()

        elif token_type in ['TOK_INT', 'TOK_CHAR', 'TOK_FLOAT', 'TOK_DOUBLE', 'TOK_VOID']:
            return self.parse_var_declaration()

        elif token_type == 'TOK_IDENTIFIER' and self.peek_token(1).type == 'TOK_ASSIGN':
            return self.parse_assignment()
        
        elif token_type == 'TOK_IF':
            return self.parse_if_statement()

        elif token_type == 'TOK_WHILE':
            return self.parse_while_loop()

        elif token_type ==  'TOK_FOR':
            return self.parse_for_loop()

        elif token_type == 'TOK_DO':
            return self.parse_do_while_loop()
        
        elif token_type == "TOK_LBRACE":
            return self.parse_block()

        elif token_type == 'TOK_IDENTIFIER' and self.peek_token(1).type == 'TOK_LPAREN':
            return self.parse_function_call()

        elif token_type == 'TOK_RETURN':
            return self.parse_return() 

        elif token_type == 'TOK_CONTINUE':
            return self.parse_continue()   

        elif token_type == 'TOK_BREAK':
            return self.parse_break()
        
        else:
            expr = self.parse_expression()
            self.expect('TOK_SEMICOLON')
            return expr

    def parse_block(self):
        self.expect('TOK_LBRACE')
        ast = []
        while not self.match('TOK_RBRACE'):
            stmt = self.parse_statement()
            if stmt is not None:
                ast.append(stmt)
        return ast
    
    def parse_expression(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        left = self.parse_logical_and()
        while self.match('TOK_OR'):
            op = '||'
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right)
        return left

    def parse_logical_and(self):
        left = self.parse_equality()
        while self.match('TOK_AND'):
            op = '&&'
            right = self.parse_equality()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_equality(self):
        left = self.parse_comparison()
        while self.match('TOK_EQ', 'TOK_NE'):
            op = self.tokens[self.pos - 1].value
            right = self.parse_comparison()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_comparison(self):
        left = self.parse_additive()
        while self.match('TOK_LT', 'TOK_LE', 'TOK_GT', 'TOK_GE'):
            op = self.tokens[self.pos - 1].value
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        return left

    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.match('TOK_PLUS', 'TOK_MINUS'):
            op = self.tokens[self.pos - 1].value
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        return left
        
    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.match('TOK_STAR', 'TOK_SLASH', 'TOK_PERCENT'):
            op = self.tokens[self.pos - 1].value
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        return left

    def parse_unary(self):
        if self.match('TOK_NOT', 'TOK_MINUS', 'TOK_INC', 'TOK_DEC'):
            op = self.tokens[self.pos - 1].value
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        else:
            return self.parse_primary()
        
    def parse_primary(self):
        token_type = self.current_token().type
        if token_type == 'TOK_IDENTIFIER':
            name = self.parse_variable()
            # Handle postfix operators: i++, i--
            if self.current_token().type in ['TOK_INC', 'TOK_DEC']:
                op = self.current_token().value
                self.advance()
                return UnaryOp(op, Identifier(name))
            return Identifier(name)
        elif token_type == 'TOK_NUMBER':
            value = int(self.parse_number())
            return Literal(value)
        elif token_type == 'TOK_STRING':
            value = self.parse_string()
            return Literal(value)
        elif token_type == 'TOK_LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.expect('TOK_RPAREN')
            return expr

    def parse_variable(self):
        name = self.expect('TOK_IDENTIFIER').value
        return name

    def parse_number(self):
        value = self.expect('TOK_NUMBER').value
        return value

    def parse_string(self):
        value = self.expect('TOK_STRING').value
        return value

    def parse_assignment(self):
        name = self.expect('TOK_IDENTIFIER').value
        self.expect('TOK_ASSIGN')
        value = self.parse_expression()
        self.expect('TOK_SEMICOLON')
        return Assignment(name, value)

    def parse_var_declaration(self):
        token = self.current_token()
        if token.type not in ['TOK_INT', 'TOK_CHAR', 'TOK_FLOAT', 'TOK_DOUBLE', 'TOK_VOID']:
            raise SyntaxError('Expected type keyword')
        data_type = token.value
        self.advance()
        name = self.expect('TOK_IDENTIFIER').value
        value = None
        if self.match('TOK_ASSIGN'):
            value = self.parse_expression()
        self.expect('TOK_SEMICOLON')
        return VarDeclaration(data_type, name, value)

    def parse_function_def(self):
        token = self.current_token()
        if token.type not in ['TOK_INT', 'TOK_CHAR', 'TOK_FLOAT', 'TOK_DOUBLE', 'TOK_VOID']:
            raise SyntaxError("Expected type keyword")
        return_type = token.value
        self.advance()
        name = self.expect('TOK_IDENTIFIER').value
        self.expect('TOK_LPAREN')
        params = []
        if not self.match('TOK_RPAREN'):
            while True:
                token = self.current_token()
                if token.type not in ['TOK_INT', 'TOK_CHAR', 'TOK_FLOAT', 'TOK_DOUBLE', 'TOK_VOID']:
                    raise SyntaxError("Expected type keyword")
                param_type = token.value
                self.advance()
                param_name = self.expect('TOK_IDENTIFIER').value
                params.append((param_type, param_name))
                if self.match('TOK_COMMA'):
                    continue
                else:
                    self.expect('TOK_RPAREN')
                    break
        body = self.parse_block()
        return FunctionDef(return_type, name, params, body)

    def parse_if_statement(self):
        self.expect('TOK_IF')
        self.expect('TOK_LPAREN')
        condition = self.parse_expression()
        self.expect('TOK_RPAREN')
        body = self.parse_block()
        else_body = None
        if self.match('TOK_ELSE'):
            else_body = self.parse_block()
        return IfStatement(condition, body, else_body)
    
    def parse_while_loop(self):
        self.expect('TOK_WHILE')
        self.expect('TOK_LPAREN')
        condition = self.parse_expression()
        self.expect('TOK_RPAREN')
        body = self.parse_block()
        return WhileLoop(condition, body)

    def parse_for_loop(self):
        self.expect('TOK_FOR')
        self.expect('TOK_LPAREN')
        init = None
        if self.current_token().type in ['TOK_INT', 'TOK_CHAR', 'TOK_FLOAT', 'TOK_DOUBLE', 'TOK_VOID']:
            token = self.current_token()
            data_type = token.value
            self.advance()
            name = self.expect('TOK_IDENTIFIER').value
            init_value = None
            if self.match('TOK_ASSIGN'):
                init_value = self.parse_expression()
            self.expect('TOK_SEMICOLON')
            init = VarDeclaration(data_type, name, init_value)
        else:
            init = self.parse_expression()
            self.expect('TOK_SEMICOLON')
        condition = self.parse_expression()
        self.expect('TOK_SEMICOLON')
        increment = self.parse_expression()
        self.expect('TOK_RPAREN')
        body = self.parse_block()
        return ForLoop(init, condition, increment, body)     

    def parse_do_while_loop(self):
        self.expect('TOK_DO')
        body = self.parse_block()
        self.expect('TOK_WHILE')
        self.expect('TOK_LPAREN')
        condition = self.parse_expression()
        self.expect('TOK_RPAREN')
        self.expect('TOK_SEMICOLON')
        return DoWhileLoop(body, condition)

    def parse_function_call(self):
        name = self.expect('TOK_IDENTIFIER').value
        self.expect('TOK_LPAREN')
        args = []
        if not self.match('TOK_RPAREN'):
            while True:
                args.append(self.parse_expression())
                if self.match('TOK_COMMA'):
                    continue
                else:
                    self.expect('TOK_RPAREN')
                    break
        self.expect('TOK_SEMICOLON')
        return FunctionCall(name, args)

    def parse_break(self):
        self.expect('TOK_BREAK')
        self.expect('TOK_SEMICOLON')
        return BreakStatement()

    def parse_continue(self):
        self.expect('TOK_CONTINUE')
        self.expect('TOK_SEMICOLON')
        return ContinueStatement()

    def parse_return(self):
        self.expect('TOK_RETURN')
        value = None
        if not self.match('TOK_SEMICOLON'):
            value = self.parse_expression()
            self.expect('TOK_SEMICOLON')
        return ReturnStatement(value)

class PyParser(object):
    #YET TO BE DONE BY SURYA
    pass