from lexer import CLexer
from parser import CParser
from py_generator import PythonGenerator

code = """
int x = 5;
x = x + 1;
"""

lexer = CLexer(code)
tokens = lexer.tokenize()

parser = CParser(tokens)
ast = parser.parse()

generator = PythonGenerator(ast)

print(generator.generate())