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
if (10 > 1) {
  if (10 > 1) {
    return true + false;
  }

  return 1;
"""
lexer: Lexer = Lexer.new(source)
parser: Parser = Parser.new(lexer)

program = parser.parse_program()
eval_program(program)
