"""
ipython -i .\src\repl.py
"""
from src.token import Token, TokenType, TokenTypes
from src import lexer

PROMPT = ">> "


def main():
    print(
        "Hello, welcome to the REPL for the Monkey \
          programming language."
    )

    while True:
        line_to_tokens()


def line_to_tokens():
    """
    Converts a single line of text into Tokens and prints
    the Tokens to screen.
    """
    line = input(PROMPT)
    l: lexer.Lexer = lexer.Lexer.new(line)
    tok = Token(Type="", Literal=None)
    while tok.Type != TokenTypes.EOF:
        tok = l.next_token()
        if tok != TokenTypes.EOF:
            print(tok)


if __name__ == "__main__":
    main()
