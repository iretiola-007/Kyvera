class ProgramNode:
    def __init__(self, statements):
        self.statements = statements


class VariableNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class PrintNode:
    def __init__(self, expression):
        self.expression = expression


class NumberNode:
    def __init__(self, value):
        self.value = value


class BinOpNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class VarAccessNode:
    def __init__(self, name):
        self.name = name

class IfNode:
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
