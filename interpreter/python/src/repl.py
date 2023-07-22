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
>> let add = fn(a, b, c, d) { return a + b + c + d };
>> add(1, 2, 3, 4);
10
>> let addThree = fn(x) { return x + 3 };
>> addThree(3);
6
>> let max = fn(x, y) { if (x > y) { x } else { y } };
>> max(5, 10)
10
>> let factorial = fn(n) { if (n == 0) { 1 } else { n * factorial(n - 1) } };
>> factorial(5)
120
>> let callTwoTimes = fn(x, func) { func(func(x)) };
>> callTwoTimes(3, addThree);
9
>> callTwoTimes(3, fn(x) { x + 1 });
5
>> let newAdder = fn(x) { fn(n) { x + n } };
>> let addTwo = newAdder(2);
>> addTwo(2);
4
>> let add = fn(x, y) { x + y; }; add(5, 5);
10
>> fn(x) { x == 10 }(10)
True
>> let firstName = "Thorsten";
>> let lastName = "Ball";
>> let fullName = fn(first, last) { first + " " + last };
>> fullName(firstName, lastName);
"""
if __name__ == "__main__":
    main()
