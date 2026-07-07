# tests/test_lexer.py

from lexer import CLexer
from token import Token

def test_simple_declaration():
    code = "int x;"
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    assert len(tokens) == 4  # int, x, ;, EOF
    assert tokens[0].type == 'TOK_INT'
    assert tokens[0].value == 'int'
    assert tokens[1].type == 'TOK_IDENTIFIER'
    assert tokens[1].value == 'x'
    assert tokens[2].type == 'TOK_SEMICOLON'
    assert tokens[3].type == 'TOK_EOF'
    print("✅ test_simple_declaration passed")

def test_number():
    code = "int x = 42;"
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.value == '42' for t in tokens)
    print("✅ test_number passed")

def test_string():
    code = 'printf("hello");'
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.type == 'TOK_STRING' and t.value == 'hello' for t in tokens)
    print("✅ test_string passed")

def test_operators():
    code = "x == 5"
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.value == '==' for t in tokens)
    print("✅ test_operators passed")

def test_comments():
    code = "int x; // comment"
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    # Should not have comment in tokens
    assert not any(t.value == 'comment' for t in tokens)
    print("✅ test_comments passed")

if __name__ == '__main__':
    test_simple_declaration()
    test_number()
    test_string()
    test_operators()
    test_comments()
    print("\n✅ All tests passed!")