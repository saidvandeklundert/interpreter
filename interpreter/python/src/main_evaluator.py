"""
ipython .\src\main_evaluator.py
ipython -i .\src\main_evaluator.py

"""

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import eval, eval_program
from src import object
import logging


logging.basicConfig(level=logging.DEBUG)


source = """
let add = fn(x, y) { x + y; };
add(21, 5);
"""
lexer: Lexer = Lexer.new(source)
parser: Parser = Parser.new(lexer)
env = object.new_environment()
program = parser.parse_program()
eval_program(program, env)
