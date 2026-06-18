from .ast import (
    ProgramNode,
    VariableNode,
    PrintNode,
    NumberNode,
    StringNode,
    BinOpNode,
    VarAccessNode,
    IfNode,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def not_eof(self):
        """
        Returns whether we are still in the range of the token list
        """

        return self.position < len(self.tokens)

    def parse(self):
        statements = []

        while self.position < len(self.tokens):
            token_type, token_value = self.tokens[self.position]

            if token_type == "VAR":
                statements.append(self.parse_variable())

            elif token_type == "PRINT":
                statements.append(self.parse_print())

            elif token_type == "IF":
                statements.append(self.parse_if())

            else:
                self.position += 1

        return ProgramNode(statements)

    def parse_variable(self):
        self.position += 1  # skip VAR
        token_type, name = self.tokens[self.position]

        if token_type != "IDENTIFIER":
            raise Exception("Expected variable name")

        self.position += 1
        token_type, arrow = self.tokens[self.position]

        if arrow != "->":
            raise Exception("Expected '->' in variable declaration")

        self.position += 1
        expr_tokens = []

        while (
            self.position < len(self.tokens)
            and self.tokens[self.position][0] != "NEWLINE"
        ):
            expr_tokens.append(self.tokens[self.position])
            self.position += 1

        expression = self.parse_expression(expr_tokens)
        return VariableNode(name, expression)

    def parse_print(self):
        self.position += 1  # skip PRINT
        expr_tokens = []

        while (
            self.position < len(self.tokens)
            and self.tokens[self.position][0] != "NEWLINE"
        ):
            expr_tokens.append(self.tokens[self.position])
            self.position += 1

        return PrintNode(self.parse_expression(expr_tokens))

    def parse_if(self):
        self.position += 1  # skip IF
        expr_tokens = []

        while (
            self.position < len(self.tokens)
            and self.tokens[self.position][0] != "NEWLINE"
        ):
            expr_tokens.append(self.tokens[self.position])
            self.position += 1

        self.position += 1  # advance past the NEWLINE token.

        condition = self.parse_expression(expr_tokens)

        body = []
        else_body = []

        # Handle indentation (basic version)
        if (
            self.position < len(self.tokens)
            and self.tokens[self.position][0] == "INDENT"
        ):
            self.position += 1
            while self.tokens[self.position][0] != "DEDENT":
                token_type, token_value = self.tokens[self.position]
                if token_type == "VAR":
                    body.append(self.parse_variable())
                elif token_type == "PRINT":
                    body.append(self.parse_print())
                else:
                    self.position += 1
            self.position += 1  # skip DEDENT

        if self.tokens[self.position][0] == "ELSE":
            self.position += 1

            while self.tokens[self.position][0] != "DEDENT":
                tok_type, value = self.tokens[self.position]
                if tok_type == "VAR":
                    else_body.append(self.parse_variable())
                elif tok_type == "PRINT":
                    else_body.append(self.parse_print())
                elif tok_type == "IF":
                    else_body.append(self.parse_if())
                else:
                    self.position += 1

            self.position += 1  # skip DEDENT
        return IfNode(condition, body, else_body)

    # -----------------------
    # Expression parsing
    # -----------------------
    def parse_expression(self, tokens):
        self.expr_tokens = tokens
        self.expr_pos = 0
        return self.parse_logic()

    # Handles 'and' / 'or'
    def parse_logic(self):
        node = self.parse_comparison()

        while self.expr_pos < len(self.expr_tokens):
            token_type, token_value = self.expr_tokens[self.expr_pos]

            if token_value == "or":
                self.expr_pos += 1
                right = self.parse_comparison()
                node = BinOpNode(node, "or", right)

            elif token_value == "and":
                self.expr_pos += 1
                right = self.parse_comparison()
                node = BinOpNode(node, "and", right)

            else:
                break

        return node

    def parse_comparison(self):
        left = self.parse_term()
        comparisons = []

        while self.expr_pos < len(self.expr_tokens) and self.expr_tokens[self.expr_pos][
            1
        ] in ("==", "!=", ">", "<", ">=", "<="):
            op = self.expr_tokens[self.expr_pos][1]
            self.expr_pos += 1
            right = self.parse_term()
            comparisons.append((left, op, right))
            left = right

        if not comparisons:
            return left

        node = BinOpNode(comparisons[0][0], comparisons[0][1], comparisons[0][2])
        for comp in comparisons[1:]:
            next_node = BinOpNode(comp[0], comp[1], comp[2])
            node = BinOpNode(node, "and", next_node)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.expr_pos < len(self.expr_tokens) and self.expr_tokens[self.expr_pos][
            1
        ] in ("+", "-"):
            op = self.expr_tokens[self.expr_pos][1]
            self.expr_pos += 1
            right = self.parse_factor()
            node = BinOpNode(node, op, right)
        return node

    def parse_factor(self):
        token_type, token_value = self.expr_tokens[self.expr_pos]

        if token_type == "NOT":
            self.expr_pos += 1
            node = self.parse_factor()
            return BinOpNode(None, "not", node)

        node = self.parse_atom()

        while self.expr_pos < len(self.expr_tokens) and self.expr_tokens[self.expr_pos][
            1
        ] in ("*", "/"):
            op = self.expr_tokens[self.expr_pos][1]
            self.expr_pos += 1
            right = self.parse_atom()
            node = BinOpNode(node, op, right)

        return node

    def parse_atom(self):
        token_type, token_value = self.expr_tokens[self.expr_pos]

        # Parentheses
        if token_value == "(":
            self.expr_pos += 1
            node = self.parse_logic()
            self.expr_pos += 1
            return node

        # Number
        if token_type == "NUMBER":
            self.expr_pos += 1
            return NumberNode(token_value)

        # String
        if token_type == "STRING":
            self.expr_pos += 1
            return StringNode(token_value)

        # Variable
        if token_type == "IDENTIFIER":
            self.expr_pos += 1
            return VarAccessNode(token_value)

        raise Exception(f"Unexpected token: {token_value}")
