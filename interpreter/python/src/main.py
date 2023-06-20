"""
python .\src\main.py
ipython -i .\src\main.py

"""
from src.lexer import *
from src.token import *


if __name__ == "__main__":
    source_code = """let five = 5;
let ten = 10;
let add = fn(x, y) {
x + y;
};
let result = add(five, ten);"""
    lexer = Lexer.new(source_code)
    max_iterations = len(source_code)
    literal = ""
    while max_iterations and literal is not None:
        tok = lexer.next_token()
        # print(f"tok.Literal: {tok.Literal}  tok.Type: {tok.Type} tok: {tok}")
        print(f"{tok.Literal}  {tok.Type} ")
        max_iterations -= 1
        literal = tok.Literal
