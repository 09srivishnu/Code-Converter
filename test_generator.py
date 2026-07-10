from lexer import CLexer
from parser import CParser
from py_generator import PythonGenerator

code = """
int main() {
    int n = 29;
    int cnt = 0;
    if (n <= 1) {
        printf("%d is NOT prime", n);
    }
    return 0;
}
"""

lexer = CLexer(code)
tokens = lexer.tokenize()

parser = CParser(tokens)
ast = parser.parse()

generator = PythonGenerator(ast)

print(generator.generate())