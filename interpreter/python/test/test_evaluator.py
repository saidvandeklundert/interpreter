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
        ("-5", -5),
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
        ("-10", -10),
        ("5 + 5 + 5 + 5 - 10", 10),
        ("2 * 2 * 2 * 2 * 2", 32),
        ("-50 + 100 + -50", 0),
        ("5 * 2 + 10", 20),
        ("5 + 2 * 10", 25),
        ("20 + 2 * -10", 0),
        ("50 / 2 * 2 + 10", 60),
        ("2 * (5 + 10)", 30),
        ("3 * 3 * 3 + 10", 37),
        ("3 * (3 * 3) + 10", 37),
        ("(5 + 10 * 2 + 15 / 3) * 2 + -10", 50),
        ("true", True),
        ("false", False),
        ("1 < 2", True),
        ("1 > 2", False),
        ("1 < 1", False),
        ("1 > 1", False),
        ("1 == 1", True),
        ("1 != 1", False),
        ("1 == 2", False),
        ("1 != 2", True),
        ("true == true", True),
        ("false == false", True),
        ("true == false", False),
        ("true != false", True),
        ("false != true", True),
        ("(1 < 2) == true", True),
        ("(1 < 2) == false", False),
        ("(1 > 2) == true", False),
        ("(1 > 2) == false", True),
        ("if (1 < 2) { 10} else { 20}", 10),
        ("if (false) { 10}", None),
        ("if (1) { 10}", 10),
        ("if (1 < 2) { 10 }", 10),
        ("if (1 > 2) { 10 }", None),
        ("if (1 > 2) { 10 } else { 20}", 20),
        ("if (1 < 2) { 10 } else { 20}", 10),
        ("return 10;", 10),
        ("return 10; 9;", 10),
        ("return 2 * 5; 9;", 10),
        ("9; return 2 * 5; 9;", 10),
    ],
)
def test_evaluations(source, expected):
    evaluated = eval_helper(source)
    import pdb

    # pdb.set_trace()
    if evaluated is None:
        assert evaluated is expected
    else:
        assert evaluated.value == expected
