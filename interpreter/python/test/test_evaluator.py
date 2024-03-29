import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import eval_program
from src import object
import pdb


def eval_helper(source: str) -> object.Object:
    l: Lexer = Lexer.new(source)
    p: Parser = Parser.new(l)

    program = p.parse_program()
    env = object.new_environment()
    return eval_program(program, env)


@pytest.mark.parametrize(
    "source, expected",
    [
        # array
        ("[1, 2, 3][0]", 1),
        ("[1, 2, 3][1]", 2),
        ("[1, 2, 3][2]", 3),
        ("let myArray = [1, 2, 3]; myArray[2];", 3),
        # builtins
        ('len("one", "two")', "wrong number of arguments. got = 2, want = 1"),
        ("len(1)", "argument to 'len' not supported, got <class 'src.object.Integer'>"),
        ('len("")', 0),
        ('len("four")', 4),
        ('len("hello world")', 11),
        # function application
        ("let identity = fn(x) { x; }; identity(5);", 5),
        ("let identity = fn(x) { return x; }; identity(5);", 5),
        ("let double = fn(x) { x * 2; }; double(5);", 10),
        ("let add = fn(x, y) { x + y; }; add(5, 5);", 10),
        ("let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", 20),
        ("fn(x) { x; }(5)", 5),
        # end function application tests
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
        # binding
        ("let a = 5; a;", 5),
        ("let a = 5 * 5; a;", 25),
        ("let a = 5; let b = a; b;", 5),
        ("let a = 5; let b = a; let c = a + b + 5; c;", 15),
    ],
)
def test_evaluations(source, expected):
    evaluated = eval_helper(source)
    import pdb

    # pdb.set_trace()
    if evaluated is None:
        assert evaluated is expected
    else:
        # pdb.set_trace()
        if type(evaluated) == object.Error:
            assert evaluated.message == expected
        else:
            assert evaluated.value == expected


@pytest.mark.parametrize(
    "source, expected_message",
    [
        (
            '"Hello" - "World"',
            "unknown operator: Type.STRING_OBJ - Type.STRING_OBJ",
        ),
        (
            "foobar",
            "identifier not found: foobar",
        ),
        (
            """
if (10 > 1) {
  if (10 > 1) {
    return true + false;
  }
}

  return 1;""",
            "unknown operator: Type.BOOLEAN_OBJ + Type.BOOLEAN_OBJ",
        ),
        (
            "if (10 > 1) { true + false; }",
            "unknown operator: Type.BOOLEAN_OBJ + Type.BOOLEAN_OBJ",
        ),
        (
            "5; true + false; 5",
            "unknown operator: Type.BOOLEAN_OBJ + Type.BOOLEAN_OBJ",
        ),
        ("5 + true;", "type mismatch: Type.INTEGER_OBJ + Type.BOOLEAN_OBJ"),
        ("5 + true;", "type mismatch: Type.INTEGER_OBJ + Type.BOOLEAN_OBJ"),
        ("5 + true; 5;", "type mismatch: Type.INTEGER_OBJ + Type.BOOLEAN_OBJ"),
        (
            "-true",
            "unknown operator: -Type.BOOLEAN_OBJ",
        ),
        (
            "true + false;",
            "unknown operator: Type.BOOLEAN_OBJ + Type.BOOLEAN_OBJ",
        ),
        (
            "true + false + true + false;",
            "unknown operator: Type.BOOLEAN_OBJ + Type.BOOLEAN_OBJ",
        ),
    ],
)
def test_error_handling(source, expected_message):
    evaluated = eval_helper(source)
    import pdb

    # pdb.set_trace()
    assert evaluated.message == expected_message


def test_function():
    source = "fn(x) { x + 2; };"
    evaluated = eval_helper(source)
    import pdb

    # pdb.set_trace()
    assert isinstance(evaluated, object.Function)
    assert evaluated.parameters[0].value == "x", "function parameter not found"
    assert len(evaluated.parameters) == 1, "incorrect number of parameters found"
    assert len(evaluated.body.statements) == 1
    assert evaluated.body.statements[0].expression.operator == "+"


def test_closures():
    source = """
    let newAdder = fn(x) {
    fn(y) { x + y };
    };
    let addTwo = newAdder(2);
    addTwo(2);
    """
    evaluated = eval_helper(source)
    assert evaluated.value == 4


def test_string_literal():
    source = """
    "Hello World!";
    """
    evaluated = eval_helper(source)
    assert evaluated.value == "Hello World!"


def test_string_concatenation():
    source = """
    "Hello" + " " + "World!";
    """
    evaluated = eval_helper(source)
    assert evaluated.value == "Hello World!"


def test_array():
    source = """
    [1, 2 * 2, 3 + 3]
    """
    evaluated = eval_helper(source)
    # pdb.set_trace()
    assert evaluated.elements[0].value == 1
    assert evaluated.elements[1].value == 4
    assert evaluated.elements[2].value == 6
