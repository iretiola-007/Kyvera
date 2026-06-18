class ProgramNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self) -> str:
        """
        Returns a string representation of the object
        when printing to the terminal
        """

        return f"ProgramNode(statements={self.statements})"


class VariableNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        """
        Returns a string representation of the object
        when printing to the terminal
        """

        return f"VariableNode(name={self.name}, value={self.value})"


class PrintNode:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self) -> str:
        """
        Returns a string representation of the object
        when printing to the terminal
        """

        return f"PrintNode(expression={self.expression})"


class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        """
        Returns a string representation of the object
        when printing to the terminal
        """

        return f"NumberNode(value={self.value})"


class StringNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        """
        Returns a string representation of the object
        when printing to the terminal
        """

        return f"StringNode(value={self.value})"


class BinOpNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self) -> str:
        """
        Returns a string representation of the object
        when printing to the terminal
        """

        return f"BinOpNode(left={self.left}, operator='{self.operator}', right={self.right})"


class VarAccessNode:
    def __init__(self, name):
        self.name = name

    def __repr__(self) -> str:
        """
        Returns a string representation of the object
        when printing to the terminal
        """

        return f"VarAccessNode(name={self.name})"


class IfNode:
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self) -> str:
        """
        Returns a string representation of the object
        when printing to the terminal
        """

        return f"IfNode(condition={self.condition}, body={self.body}, else_body={self.else_body})"


class UnaryOpNode:
    def __init__(self, operator, node):
        self.operator = operator
        self.node = node

    def __repr__(self) -> str:
        """
        Returns a string representation of the object
        when printing to the terminal
        """

        return f"UnaryOpNode(operator={self.operator}, node={self.node})"
