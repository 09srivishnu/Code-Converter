from ast_nodes import *

class PythonGenerator(object):
    def __init__(self, ast):
        self.ast = ast
        self.output = []
        self.indent_level = 0

    def generate(self):
        for node in self.ast:
            self.generate_node(node)
        
        return '\n'.join(self.output)

    def generate_node(self, node):
        if isinstance(node, VarDeclaration):
            self.generate_var_declaration(node)
        elif isinstance(node, Assignment):
            self.generate_assignment(node)
        elif isinstance(node, IfStatement):
            self.generate_if_statement(node)
        elif isinstance(node, ForLoop):
            self.generate_for_loop(node)
        elif isinstance(node, WhileLoop):
            self.generate_while_loop(node)
        elif isinstance(node, DoWhileLoop):
            self.generate_do_while_loop(node)
        elif isinstance(node, FunctionDef):
            self.generate_function_def(node)
        elif isinstance(node, FunctionCall):
            self.generate_function_call(node)
        elif isinstance(node, ReturnStatement):
            self.generate_return_statement(node)
        elif isinstance(node, BreakStatement):
            self.generate_break_statement(node)
        elif isinstance(node, ContinueStatement):
            self.generate_continue_statement(node)
        elif isinstance(node, Block):
            self.generate_block(node)
        elif isinstance(node, UnaryOp):
            self.generate_unary_op(node)
        elif isinstance(node, BinaryOp):
            self.generate_binary_op(node)
        elif isinstance(node, Literal):
            self.generate_literal(node)
        elif isinstance(node, Identifier):
            self.generate_identifier(node)
        else:
            raise ValueError("Unsupported node type: {}".format(type(node)))

    def emit(self, line):
        indent = '      ' * self.indent_level
        self.output.append(indent + line)

    def increase_indent(self):
        self.indent_level += 1

    def decrease_indent(self):
        self.indent_level -= 1
        if self.indent_level < 0:
            self.indent_level = 0

    def generate_var_declaration(self, node):
        if node.value is not None:
            self.emit(f"{node.name} = {self.generate_expression(node.value)}")
        else:
            self.emit(f"{node.name} = 0")

    def generate_assignment(self, node):
        self.emit(f"{node.name} = {self.generate_expression(node.value)}")

    def generate_if_statement(self, node):
        self.emit(f"if {self.generate_expression(node.condition)}:")
        self.increase_indent()
        for stmt in node.body:
            self.generate_node(stmt)
        self.decrease_indent()
        if node.else_body is not None:
            self.emit("else:")
            self.increase_indent()
            for stmt in node.else_body:
                self.generate_node(stmt)
            self.decrease_indent()

    def generate_for_loop(self, node):
        variable = node.init.name
        start = self.generate_expression(node.init.value)
        end = self.generate_expression(node.condition.right)
        self.emit(f"for {variable} in range({start}, {end}):")
        self.increase_indent()
        for stmt in node.body:
            self.generate_node(stmt)
        self.decrease_indent()
    
    def generate_while_loop(self, node):
        self.emit(f"while {self.generate_expression(node.condition)}:")
        self.increase_indent()
        for stmt in node.body:
            self.generate_node(stmt)
        self.decrease_indent()

    def generate_do_while_loop(self, node):
        self.emit("while True:")
        self.increase_indent()
        for stmt in node.body:
            self.generate_node(stmt)
        self.emit(f"if not {self.generate_expression(node.condition)}:")
        self.increase_indent()
        self.emit("break")
        self.decrease_indent()
        self.decrease_indent()

    def generate_function_def(self, node):
        params = ', '.join(param.name for param in node.params)
        self.emit(f"def {node.name}({params}):")
        self.increase_indent()
        for stmt in node.body:
            self.generate_node(stmt)
        self.decrease_indent()

    def generate_function_call(self, node):
        py_name = self.map_c_function_to_python(node.name)
    
        if py_name == 'print':
            if len(node.args) > 0 and isinstance(node.args[0], Literal):
                fmt_str = node.args[0].value
                format_args = node.args[1:]
            
                converted_fmt = fmt_str
                converted_fmt = converted_fmt.replace('%d', '{}')
                converted_fmt = converted_fmt.replace('%s', '{}')
                converted_fmt = converted_fmt.replace('%f', '{}')
            
                args_str = ', '.join(self.generate_expression(arg) for arg in format_args)
                self.emit(f"print(f\"{converted_fmt}\".format({args_str}))")
            else:
                args = ', '.join(self.generate_expression(arg) for arg in node.args)
                self.emit(f"{py_name}({args})")
        else:
            args = ', '.join(self.generate_expression(arg) for arg in node.args)
            self.emit(f"{py_name}({args})")

    def generate_return_statement(self, node):
        if node.value is not None:
            self.emit(f"return {self.generate_expression(node.value)}")
        else:
            self.emit("return")

    def generate_break_statement(self, node):
        self.emit("break")

    def generate_continue_statement(self, node):
        self.emit("continue")

    def generate_block(self, node):
        for stmt in node.statements:
            self.generate_node(stmt)

    def generate_unary_op(self, node):
        operand = self.generate_expression(node.operand)
        if node.op == "++" or node.op == "--":
            return f"{operand} += 1" if node.op == "++" else f"{operand} -= 1"
        return f"{node.op}{operand}"

    def generate_binary_op(self, node):
        left = self.generate_expression(node.left)
        right = self.generate_expression(node.right)
        return f"{left} {node.op} {right}"

    def generate_literal(self, node):
        return str(node.value)

    def generate_identifier(self, node):
        return node.name

    def generate_expression(self, node):
        if isinstance(node, BinaryOp):
            return self.generate_binary_op(node)
        elif isinstance(node, UnaryOp):
            return self.generate_unary_op(node)
        elif isinstance(node, Literal):
            return self.generate_literal(node)
        elif isinstance(node, Identifier):
            return self.generate_identifier(node)
        else:
            raise ValueError("Unsupported expression node type: {}".format(type(node)))

    def map_c_function_to_python(self, name):
        mapping = {
        'printf': 'print',
        'scanf': 'input',
        'strlen': 'len',
        'malloc': 'list',
        }
        return mapping.get(name, name)

    def infer_python_type(self, value):
        if isinstance(value, Literal):
            if isinstance(value.value, int):
                return 0
            elif isinstance(value.value, float):
                return 0.0
            elif isinstance(value.value, str):
                return ""
        return None