from .ast import NumberNode, BinOpNode, VarAccessNode

class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, program_node):
        for statement in program_node.statements:
            self.visit(statement)

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"No visit method for {type(node).__name__}")

    def visit_PrintNode(self, node):
        value = self.evaluate(node.expression)
        print(value)
    

    def evaluate(self, node):
        if isinstance(node, NumberNode):
            return node.value
            
        if isinstance(node, VarAccessNode):
            if node.name in self.variables:
                return self.variables[node.name]
            else:
                raise Exception(f"Undefined variable '{node.name}'")

        if isinstance(node, BinOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            if node.operator == "+":
                return left + right
            elif node.operator == "-":
                return left - right
            elif node.operator == "*":
                return left * right
            elif node.operator == "/":
                return left / right
            elif node.operator == ">":
                return left > right
            elif node.operator == "<":
                return left < right
            elif node.operator == "==":
                return left == right
            elif node.operator == "!=":
                return left != right
            elif node.operator == ">=":
                return left >= right
            elif node.operator == "<=":
                return left <= right
            elif node.operator == "and":
                return left and right
            
    def visit_VariableNode(self, node):
        value = self.evaluate(node.value)
        self.variables[node.name] = value
        
    def visit_IfNode(self, node):
        condition = self.evaluate(node.condition)

        if condition:
            for stmt in node.body:
                self.visit(stmt)
        elif node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)
