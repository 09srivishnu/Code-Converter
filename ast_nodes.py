class ASTNode(object):
    pass

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class VarDeclaration(ASTNode):
    def __init__(self, data_type, name, init_value):
        self.data_type = data_type
        self.name = name
        self.init_value = None if init_value is None else init_value

class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class IfStatement(ASTNode):
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = None if else_body is None else else_body

class ForLoop(ASTNode):
    def __init__(self, init, condition, increment, body):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body

class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class DoWhileLoop(ASTNode):
    def __init__(self, body, condition):
        self.body = body
        self.condition = condition

class FunctionDef(ASTNode):
    def __init__(self, return_type, name, params, body):
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body

class ClassDef(ASTNode):
    def __init__(self, name, base_class, body):
        self.name = name
        self.base_class = base_class
        self.body = body

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class ReturnStatement(ASTNode):
    def __init__(self, value):
        self.value = value

class BreakStatement(ASTNode):
    pass

class ContinueStatement(ASTNode):
    pass

class ArrayAccess(ASTNode):
    def __init__(self, array, index):
        self.array = array
        self.index = index

class StructAccess(ASTNode):
    def __init__(self, object, field):
        self.object = object
        self.field = field

