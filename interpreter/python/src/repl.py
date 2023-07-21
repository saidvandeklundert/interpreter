"""
ipython -i .\src\repl.py
ipython .\src\repl.py
"""
from src.token import Token, TokenType, TokenTypes
from src import lexer
from src import parser
from src import evaluator
from src import object

PROMPT = ">> "


def main():
    print(
        "Hello, welcome to the REPL for the Monkey \
          programming language."
    )
    env = object.new_environment()
    while True:
        parse_line(env)


def parse_line(env: object.Environment):
    """
    Parse and evaluate a single line
    """
    line = input(PROMPT)

    l: lexer.Lexer = lexer.Lexer.new(line)
    p: parser.Parser = parser.Parser.new(l)

    program = p.parse_program()

    result = evaluator.eval(program, env)
    if result is not None:
        print(result.inspect())

"""

>> let a = 5;
>> let b = a > 3;
>> let c = a * 99;
>> if (b) { 10 } else { 1 };
10
>> let d = if (c > a) { 99 } else { 100 };
>> d
99
>> d * c * a;
245025
"""
if __name__ == "__main__":
    main()

