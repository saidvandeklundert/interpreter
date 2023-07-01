"""
python .\src\main_parser.py
ipython -i .\src\main_parser.py

"""
from src.lexer import *
from src.token import *
from src.parser import *
from src import token
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


source = """
let x = 5;
let y = 10;
let foobar = 838383;
return 5;
5;
1 + 2 + 3;
false;
true == true;
(!(true == true));
"""

if __name__ == "__main__":
    l = Lexer.new(source)
    p = Parser.new(l)
    # print(p.parse_statement())
    # print(p.parse_let_statement())

    program = p.parse_program()
    print("\n\nProgram\n\n", program)
