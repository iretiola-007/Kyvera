import sys
from novascript.languages.loader import load_language
from novascript.core.lexer import Lexer
from novascript.core.parser import Parser
from novascript.core.interpreter import Interpreter


def extract_language(code):
    lines = [line.strip() for line in code.split("\n") if line.strip()]

    if not lines[0].startswith("use "):
        raise Exception("NovaScript requires 'use <language>' at the top.")

    _, lang_name = lines[0].split()

    return lang_name.lower(), "\n".join(lines[1:])
        


def main():
    file = sys.argv[1]

    with open(file, "r", encoding="utf-8") as f:
        code = f.read()

    lang_name, code_without_directive = extract_language(code)

    language_pack = load_language(lang_name)

    lexer = Lexer(code_without_directive, language_pack.KEYWORDS)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(ast)
    
    DEBUG = False

    tokens = lexer.tokenize()

    if DEBUG:
        print(tokens)
    


if __name__ == "__main__":
    main()