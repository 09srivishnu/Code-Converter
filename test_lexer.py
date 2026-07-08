from lexer import CLexer, PyLexer
from token import Token

# ============ C LEXER TESTS ============

def test_c_simple_declaration():
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
    print("✅ test_c_simple_declaration passed")

def test_c_number():
    code = "int x = 42;"
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.value == '42' for t in tokens)
    assert any(t.type == 'TOK_NUMBER' for t in tokens)
    print("✅ test_c_number passed")

def test_c_float():
    code = "float pi = 3.14;"
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.value == '3.14' for t in tokens)
    print("✅ test_c_float passed")

def test_c_string_double_quote():
    code = 'printf("hello");'
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.type == 'TOK_STRING' and t.value == 'hello' for t in tokens)
    print("✅ test_c_string_double_quote passed")

def test_c_string_single_quote():
    code = "char c = 'x';"
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.type == 'TOK_STRING' and t.value == 'x' for t in tokens)
    print("✅ test_c_string_single_quote passed")

def test_c_operators():
    code = "x == 5"
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.value == '==' for t in tokens)
    assert any(t.type == 'TOK_EQ' for t in tokens)
    print("✅ test_c_operators passed")

def test_c_line_comment():
    code = "int x; // comment here"
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    # Should not have "comment" in tokens
    assert not any(t.value == 'comment' for t in tokens)
    print("✅ test_c_line_comment passed")

def test_c_block_comment():
    code = "int x; /* comment */ int y;"
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    # Should not have "comment" in tokens
    assert not any(t.value == 'comment' for t in tokens)
    assert tokens[0].value == 'int'
    assert tokens[1].value == 'x'
    print("✅ test_c_block_comment passed")

def test_c_for_loop():
    code = "for (int i = 0; i < 10; i++)"
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.type == 'TOK_FOR' for t in tokens)
    assert any(t.value == '++' for t in tokens)
    print("✅ test_c_for_loop passed")

def test_c_operators_multi_char():
    code = "x++ y-- a&&b c||d"
    lexer = CLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.value == '++' for t in tokens)
    assert any(t.value == '--' for t in tokens)
    assert any(t.value == '&&' for t in tokens)
    assert any(t.value == '||' for t in tokens)
    print("✅ test_c_operators_multi_char passed")

# ============ PYTHON LEXER TESTS ============

def test_py_simple_assignment():
    code = "x = 5"
    lexer = PyLexer(code)
    tokens = lexer.tokenize()
    
    assert len(tokens) == 4  # x, =, 5, EOF
    assert tokens[0].type == 'TOK_IDENTIFIER'
    assert tokens[0].value == 'x'
    assert tokens[1].type == 'TOK_ASSIGN'
    assert tokens[2].type == 'TOK_NUMBER'
    assert tokens[2].value == '5'
    print("✅ test_py_simple_assignment passed")

def test_py_string_double_quote():
    code = 'name = "world"'
    lexer = PyLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.type == 'TOK_STRING' and t.value == 'world' for t in tokens)
    print("✅ test_py_string_double_quote passed")

def test_py_string_single_quote():
    code = "name = 'world'"
    lexer = PyLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.type == 'TOK_STRING' and t.value == 'world' for t in tokens)
    print("✅ test_py_string_single_quote passed")

def test_py_fstring():
    code = 'message = f"hello {name}"'
    lexer = PyLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.type == 'TOK_FSTRING' for t in tokens)
    print("✅ test_py_fstring passed")

def test_py_comment():
    code = "x = 5  # this is a comment"
    lexer = PyLexer(code)
    tokens = lexer.tokenize()
    
    # Should not have "comment" in tokens
    assert not any(t.value == 'comment' for t in tokens)
    print("✅ test_py_comment passed")

def test_py_keywords():
    code = "if x == 5: print('yes')"
    lexer = PyLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.type == 'TOK_IF' for t in tokens)
    assert any(t.type == 'TOK_EQ' for t in tokens)
    print("✅ test_py_keywords passed")

def test_py_for_loop():
    code = "for i in range(10):"
    lexer = PyLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.type == 'TOK_FOR' for t in tokens)
    assert any(t.type == 'TOK_IN' for t in tokens)
    print("✅ test_py_for_loop passed")

def test_py_float():
    code = "pi = 3.14"
    lexer = PyLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.value == '3.14' for t in tokens)
    print("✅ test_py_float passed")

def test_py_def():
    code = "def foo(x, y):"
    lexer = PyLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.type == 'TOK_DEF' for t in tokens)
    print("✅ test_py_def passed")

def test_py_logical_operators():
    code = "if x and y or z:"
    lexer = PyLexer(code)
    tokens = lexer.tokenize()
    
    assert any(t.type == 'TOK_AND' for t in tokens)
    assert any(t.type == 'TOK_OR' for t in tokens)
    print("✅ test_py_logical_operators passed")

if __name__ == '__main__':
    print("=" * 50)
    print("RUNNING C LEXER TESTS")
    print("=" * 50)
    test_c_simple_declaration()
    test_c_number()
    test_c_float()
    test_c_string_double_quote()
    test_c_string_single_quote()
    test_c_operators()
    test_c_line_comment()
    test_c_block_comment()
    test_c_for_loop()
    test_c_operators_multi_char()
    
    print("\n" + "=" * 50)
    print("RUNNING PYTHON LEXER TESTS")
    print("=" * 50)
    test_py_simple_assignment()
    test_py_string_double_quote()
    test_py_string_single_quote()
    test_py_fstring()
    test_py_comment()
    test_py_keywords()
    test_py_for_loop()
    test_py_float()
    test_py_def()
    test_py_logical_operators()
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("=" * 50)