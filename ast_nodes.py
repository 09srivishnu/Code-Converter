class ASTNode:
    class Literal(ASTNode):
        def __init__(self, value):
            self.value = value