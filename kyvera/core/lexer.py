import re


class Lexer:
    def __init__(self, code, keywords):
        self.code = code
        self.keywords = keywords
        self.tokens = []
        self.indent_stack = [0]  # Track indentation levels

    def tokenize(self):
        lines = self.code.split("\n")

        for line_number, raw_line in enumerate(lines, start=1):
            # Skip empty lines
            if not raw_line.strip():
                continue

            # Count leading spaces
            indent = len(raw_line) - len(raw_line.lstrip(" "))

            # Enforce 4-space indentation
            if indent % 4 != 0:
                raise Exception(
                    f"Indentation error on line {line_number}: must use multiples of 4 spaces."
                )

            self.handle_indentation(indent)

            line = raw_line.strip()

            # Token pattern that correctly captures strings
            token_pattern = (
                r'"[^"]*"|\d+|==|!=|>=|<=|->|\+|\-|\*|\/|>|<|\(|\)|:|,|[A-Za-z_]\w*'
            )

            parts = re.findall(token_pattern, line)

            for part in parts:
                # Keywords (language packs)
                if part in self.keywords:
                    self.tokens.append((self.keywords[part], None))

                # Numbers
                elif part.isdigit():
                    self.tokens.append(("NUMBER", int(part)))

                # Strings
                elif part.startswith('"') and part.endswith('"'):
                    value = part[1:-1]
                    self.tokens.append(("STRING", value))

                # Identifiers
                else:
                    self.tokens.append(("IDENTIFIER", part))

            # End of line
            self.tokens.append(("NEWLINE", None))

        # Close remaining indentation blocks
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(("DEDENT", None))

        return self.tokens

    def handle_indentation(self, indent):
        current = self.indent_stack[-1]

        if indent > current:
            self.indent_stack.append(indent)
            self.tokens.append(("INDENT", None))
            current = indent

        while indent < current:
            self.indent_stack.pop()
            current = self.indent_stack[-1]
            self.tokens.append(("DEDENT", None))

        if indent != current:
            raise Exception("Invalid dedent level.")
