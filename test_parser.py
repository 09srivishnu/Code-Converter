from lexer import CLexer
from parser import CParser
from ast_nodes import *

# Test 1: Simple variable declaration
code1 = "int x = 5;"
lexer1 = CLexer(code1)
tokens1 = lexer1.tokenize()
parser1 = CParser(tokens1)
ast1 = parser1.parse()

print("Test 1: int x = 5;")
print(ast1)
print(ast1[0])  # VarDeclaration(int, x, Literal(5))
assert isinstance(ast1[0], VarDeclaration)
assert ast1[0].name == "x"
assert ast1[0].data_type == "int"
print("✅ Test 1 passed\n")

# Test 2: Assignment
code2 = "x = 10;"
lexer2 = CLexer(code2)
tokens2 = lexer2.tokenize()
parser2 = CParser(tokens2)
ast2 = parser2.parse()

print("Test 2: x = 10;")
print(ast2[0])  # Assignment(x, Literal(10))
assert isinstance(ast2[0], Assignment)
assert ast2[0].name == "x"
print("✅ Test 2 passed\n")

# Test 3: If statement
code3 = "if (x == 5) { y = 10; }"
lexer3 = CLexer(code3)
tokens3 = lexer3.tokenize()
parser3 = CParser(tokens3)
ast3 = parser3.parse()

print("Test 3: if (x == 5) { y = 10; }")
print(ast3[0])  # IfStatement
assert isinstance(ast3[0], IfStatement)
assert isinstance(ast3[0].condition, BinaryOp)
print("✅ Test 3 passed\n")

# Test 4: For loop
code4 = "for (int i = 0; i < 3; i++) { x++; }"
lexer4 = CLexer(code4)
tokens4 = lexer4.tokenize()
parser4 = CParser(tokens4)
ast4 = parser4.parse()

print("Test 4: for loop")
print(ast4[0])  # ForLoop
assert isinstance(ast4[0], ForLoop)
print("✅ Test 4 passed\n")

# Test 5: While loop
code5 = "while (x < 10) { x++; }"
lexer5 = CLexer(code5)
tokens5 = lexer5.tokenize()
parser5 = CParser(tokens5)
ast5 = parser5.parse()

print("Test 5: while loop")
assert isinstance(ast5[0], WhileLoop)
print("✅ Test 5 passed\n")

# Test 6: Function call
code6 = "printf(\"hello\");"
lexer6 = CLexer(code6)
tokens6 = lexer6.tokenize()
parser6 = CParser(tokens6)
ast6 = parser6.parse()

print("Test 6: printf(\"hello\");")
assert isinstance(ast6[0], FunctionCall)
assert ast6[0].name == "printf"
print("✅ Test 6 passed\n")

# Test 7: Return statement
code7 = "return 5;"
lexer7 = CLexer(code7)
tokens7 = lexer7.tokenize()
parser7 = CParser(tokens7)
ast7 = parser7.parse()

print("Test 7: return 5;")
assert isinstance(ast7[0], ReturnStatement)
print("✅ Test 7 passed\n")

# Test 8: Binary operations
code8 = "x = 5 + 3;"
lexer8 = CLexer(code8)
tokens8 = lexer8.tokenize()
parser8 = CParser(tokens8)
ast8 = parser8.parse()

print("Test 8: x = 5 + 3;")
assert isinstance(ast8[0], Assignment)
assert isinstance(ast8[0].value, BinaryOp)
assert ast8[0].value.op == "+"
print("✅ Test 8 passed\n")

# Test 9: Function definition
code9 = "int foo(int x) { return x; }"
lexer9 = CLexer(code9)
tokens9 = lexer9.tokenize()
parser9 = CParser(tokens9)
ast9 = parser9.parse()

print("Test 9: function definition")
assert isinstance(ast9[0], FunctionDef)
assert ast9[0].name == "foo"
assert ast9[0].return_type == "int"
print("✅ Test 9 passed\n")

# Test 10: Break and continue
code10 = "break; continue;"
lexer10 = CLexer(code10)
tokens10 = lexer10.tokenize()
parser10 = CParser(tokens10)
ast10 = parser10.parse()

print("Test 10: break and continue")
assert isinstance(ast10[0], BreakStatement)
assert isinstance(ast10[1], ContinueStatement)
print("✅ Test 10 passed\n")

print("=" * 50)
print("✅ ALL PARSER TESTS PASSED!")
print("=" * 50)