"""
python .\src\main_evaluator.py
ipython -i .\src\main_evaluator.py

"""

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import eval
from src import object

source = """
5
-1
"""
lexer: Lexer = Lexer.new(source)
parser: Parser = Parser.new(lexer)

program = parser.parse_program()
eval(program)
