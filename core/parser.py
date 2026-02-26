from .ast import ProgramNode, VariableNode, PrintNode, NumberNode, BinOpNode, VarAccessNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        statements = []

        while self.position < len(self.tokens):
            token_type, args = self.tokens[self.position]

            if token_type == "VAR":
                statements.append(self.parse_variable())

            elif token_type == "PRINT":
                statements.append(self.parse_print())

            self.position += 1

        return ProgramNode(statements)

    def parse_variable(self):
        args = self.tokens[self.position][1]
        name = args[0]

        arrow_index = args.index("->")
        expression_tokens = args[arrow_index + 1:]

        expression = self.parse_expression(expression_tokens)
        return VariableNode(name, expression)

    def parse_print(self):
        self.position += 1  # skip PRINT

        expr_tokens = []

        while (
            self.position < len(self.tokens)
            and self.tokens[self.position][0] != "NEWLINE"
        ):
            token_type, value = self.tokens[self.position]

            if value is not None:
                expr_tokens.append(value)

            self.position += 1

        return PrintNode(self.parse_expression(expr_tokens))
    
    def parse_expression(self, tokens):
        self.expr_tokens = tokens
        self.expr_pos = 0
        return self.parse_comparison()
    
    def parse_term(self):
        node = self.parse_factor()

        while (
            self.expr_pos < len(self.expr_tokens)
            and self.expr_tokens[self.expr_pos] in ("+", "-")
        ):
            op = self.expr_tokens[self.expr_pos]
            self.expr_pos += 1
            right = self.parse_factor()
            node = BinOpNode(node, op, right)

        return node

    def parse_factor(self):
        node = self.parse_atom()

        while (
            self.expr_pos < len(self.expr_tokens)
            and self.expr_tokens[self.expr_pos] in ("*", "/")
        ):
            op = self.expr_tokens[self.expr_pos]
            self.expr_pos += 1
            right = self.parse_atom()
            node = BinOpNode(node, op, right)

        return node

    def parse_atom(self):
        token = self.expr_tokens[self.expr_pos]

        if token == "(":
            self.expr_pos += 1
            node = self.parse_comparison()  # FIXED
            self.expr_pos += 1  # skip ')'
            return node

        if token.isdigit():
            self.expr_pos += 1
            return NumberNode(int(token))

        if token.isidentifier():
            self.expr_pos += 1
            return VarAccessNode(token)

        raise Exception(f"Unexpected token: {token}")
        
    def parse_comparison(self):
        left = self.parse_term()

        comparisons = []

        while (
            self.expr_pos < len(self.expr_tokens)
            and self.expr_tokens[self.expr_pos] in ("==", "!=", ">", "<", ">=", "<=")
        ):
            op = self.expr_tokens[self.expr_pos]
            self.expr_pos += 1
            right = self.parse_term()

            comparisons.append((left, op, right))
            left = right  # important for chaining

        if not comparisons:
            return left

        # Build chained AND comparisons
        node = BinOpNode(
            comparisons[0][0],
            comparisons[0][1],
            comparisons[0][2],
        )

        for comp in comparisons[1:]:
            next_node = BinOpNode(comp[0], comp[1], comp[2])
            node = BinOpNode(node, "and", next_node)

        return node
    