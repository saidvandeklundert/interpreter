"""
ipython -i .\src\repl.py
ipython .\src\repl.py
"""
from src.token import Token, TokenType, TokenTypes
from src import lexer
from src import parser
from src import evaluator

PROMPT = ">> "


def main():
    print(
        "Hello, welcome to the REPL for the Monkey \
          programming language."
    )

    while True:
        parse_line()


def parse_line():
    """
    Parse and evaluate a single line
    """
    line = input(PROMPT)

    l: lexer.Lexer = lexer.Lexer.new(line)
    p: parser.Parser = parser.Parser.new(l)

    program = p.parse_program()
    result = evaluator.eval(program)
    if result is not None:
        print(result.inspect())


if __name__ == "__main__":
    main()
