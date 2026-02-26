import re


class Lexer:
    def __init__(self, code, keywords):
        self.code = code
        self.keywords = keywords

        self.tokens = []
        self.indent_stack = [0]  # Track indentation levels

    def tokenize(self):
        lines = self.code.split("\n")

        for raw_line in lines:
            # Skip completely empty lines
            if not raw_line.strip():
                continue

            # Count leading spaces
            indent = len(raw_line) - len(raw_line.lstrip(" "))

            # STRICT: must be multiples of 4
            if indent % 4 != 0:
                raise Exception("Indentation must be multiples of 4 spaces.")

            self.handle_indentation(indent)

            line = raw_line.strip()

            # Add spacing around important symbols
            line = line.replace("==", " == ")
            line = line.replace("!=", " != ")
            line = line.replace(">=", " >= ")
            line = line.replace("<=", " <= ")
            line = line.replace(">", " > ")
            line = line.replace("<", " < ")
            line = line.replace("(", " ( ")
            line = line.replace(")", " ) ")
            line = line.replace(":", " : ")
            line = line.replace("->", " -> ")

            parts = re.split(r"\s+", line)

            for part in parts:
                if not part:
                    continue

                # NEWLINE handling
                if part == "\n":
                    continue

                # Keywords
                if part in self.keywords:
                    self.tokens.append((self.keywords[part], None))
                else:
                    self.tokens.append(("IDENTIFIER_OR_LITERAL", part))

            # End of line
            self.tokens.append(("NEWLINE", None))

        # Close remaining blocks
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(("DEDENT", None))

        return self.tokens

    def handle_indentation(self, indent):
        current = self.indent_stack[-1]

        if indent > current:
            self.indent_stack.append(indent)
            self.tokens.append(("INDENT", None))

        while indent < current:
            self.indent_stack.pop()
            current = self.indent_stack[-1]
            self.tokens.append(("DEDENT", None))