import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import eval
from src import object


def eval_helper(source: str) -> object.Object:
    l: Lexer = Lexer.new(source)
    p: Parser = Parser.new(l)

    program = p.parse_program()
    return eval(program)


@pytest.mark.parametrize(
    "source, expected",
    [
        ("5", 5),
        ("10", 10),
        ("1214315", 1214315),
        ("!!5", True),
        ("true", True),
        ("false", False),
        ("!false", True),
        ("!true", False),
        ("!5", False),
        ("!!true", True),
        ("!!false", False),
        ("!!5", True),
    ],
)
def test_integer_expression(source, expected):
    evaluated = eval_helper(source)
    assert evaluated.value == expected
