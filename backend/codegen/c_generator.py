from parser.ast_nodes import *
class CGenerator(object):
    def generate(self, ast: ASTNode) -> str:
        raise NotImplementedError