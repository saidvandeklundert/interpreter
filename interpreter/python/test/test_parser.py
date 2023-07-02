import pytest
from src.token import Token, TokenType, TokenTypes
from src.lexer import Lexer
from src.parser import Parser
from src.ast import (
    Program,
    Statement,
    LetStatement,
    Identifier,
    IntegerLiteral,
    ExpressionStatement,
    Expression,
    InfixExpression,
    FunctionLiteral,
)

PROGRAM = """
let x = 5;
let y = 10;
let foobar = 838383;"""


ERR_PROGRAM = """
let x = 5;
let y = 10;
let 838383;"""


def test_error_in_program():
    l: Lexer = Lexer.new(ERR_PROGRAM)
    p: Parser = Parser.new(l)

    p.parse_program()
    with pytest.raises(AssertionError):
        check_parser_error(p)


def check_parser_error(p: Parser) -> str | None:
    assert len(p.errors) == 0, f"program encountered errors{p.errors}"


def test_let_statement():
    l: Lexer = Lexer.new(PROGRAM)
    p: Parser = Parser.new(l)

    program = p.parse_program()

    check_parser_error(p)

    assert isinstance(program, Program)

    expected_identifiers = ["x", "y", "foobar"]

    for idx, statement in enumerate(program):
        statement: LetStatement
        expected = expected_identifiers[idx]
        assert (
            statement.name.value == expected
        ), f"statement expected {expected}, got {statement.name.value }"

        assert statement.token.Type == TokenTypes.LET
        assert statement.token.Literal == "let"


def test_statement_instantiation():
    statement = LetStatement(
        token=Token(Type=TokenTypes.LET, Literal="let"),
        name=Identifier(
            token=Token(Type=TokenTypes.IDENT, Literal="x"),
            value="x",
        ),
        value=None,
    )
    assert isinstance(statement, LetStatement)
    assert statement.token.Type == TokenTypes.LET
    assert statement.token.Literal == "let"
    assert statement.token_literal() == "let"
    assert statement.name.value == "x"


def test_return_statement():
    program_input = """
return 5;
return 10;
return 993322;"""
    l: Lexer = Lexer.new(program_input)
    p: Parser = Parser.new(l)

    program = p.parse_program()
    check_parser_error(p)
    assert len(program.statements) == 3, "program should contain 3 statements"

    for statement in program.statements:
        assert (
            statement.token_literal() == "return"
        ), "expected the token.Literal to be return"


def test_integer_literal():
    """
    Have the parser parse a program with a single statement and:
    - assert the program contains 1 statement
    - asser that statement is an expression
    - assert that expression is an IntegerLiteral
    - assert the value of that IntegerLiteral is 5
    """
    program = "5;"
    l: Lexer = Lexer.new(program)
    p: Parser = Parser.new(l)

    parsed_program = p.parse_program()
    assert len(parsed_program.statements) == 1
    expression_statement = parsed_program.statements[0]
    assert isinstance(expression_statement, ExpressionStatement)

    integer_literal = expression_statement.expression
    assert isinstance(integer_literal, IntegerLiteral)
    assert integer_literal.token.Literal == "5"
    assert integer_literal.value == 5


def test_parse_prefix_expression():
    """
    Verify that the parser can correctly parse prefix expressions.
    """
    program = "!5;\n-15;"
    l: Lexer = Lexer.new(program)
    p: Parser = Parser.new(l)

    parsed_program = p.parse_program()
    assert len(parsed_program.statements) == 2

    expression_1 = parsed_program.statements[0].expression
    assert expression_1.operator == "!"
    assert expression_1.right.value == 5
    assert isinstance(expression_1.right, Expression)

    expression_2 = parsed_program.statements[1].expression
    assert expression_2.operator == "-"
    assert expression_2.right.value == 15
    assert isinstance(expression_2.right, Expression)


def test_parsing_infix_expressions():
    test_inputs = [
        ["5 + 5;", 5, "+", 5],
        ["5 - 5;", 5, "-", 5],
        ["5 * 5;", 5, "*", 5],
        ["5 / 5;", 5, "/", 5],
        ["5 > 5;", 5, ">", 5],
        ["5 < 5;", 5, "<", 5],
        ["5 == 5;", 5, "==", 5],
        ["5 != 5;", 5, "!=", 5],
        ["true == true;", True, "==", True],
        ["true != false;", True, "!=", False],
        ["false == false;", False, "==", False],
    ]
    for test_input in test_inputs:
        # import pdb

        # pdb.set_trace()
        l: Lexer = Lexer.new(test_input[0])
        p: Parser = Parser.new(l)

        parsed_program = p.parse_program()
        # pdb.set_trace()
        assert len(parsed_program.statements) == 1
        assert isinstance(parsed_program.statements[0].expression, InfixExpression)
        assert parsed_program.statements[0].expression.left.value == test_input[1]
        assert parsed_program.statements[0].expression.operator == test_input[2]
        assert parsed_program.statements[0].expression.right.value == test_input[3]


def test_if_else():
    l: Lexer = Lexer.new("if (x < y) { x } else { y }")
    p: Parser = Parser.new(l)

    program = p.parse_program()

    check_parser_error(p)

    assert isinstance(program, Program)

    assert len(program.statements) == 1
    assert (
        program.statements[0].expression.consequence.statements[0].expression.value
        == "x"
    )
    assert program.statements[0].expression.alternative is not None
    assert (
        program.statements[0].expression.alternative.statements[0].expression.value
        == "y"
    )


def test_function_literal():
    l: Lexer = Lexer.new("fn(x,y) { x + y }")
    p: Parser = Parser.new(l)

    program = p.parse_program()

    check_parser_error(p)
    assert len(program.statements) == 1
    statement = program.statements[0]

    assert isinstance(statement.expression, FunctionLiteral)

    assert len(statement.expression.body.statements) == 1


@pytest.mark.parametrize(
    "source,expected",
    [
        ("fn(x) {};", ["x"]),
        ("fn(x,y,z) {};", ["x", "y", "z"]),
        ("fn() {};", []),
    ],
)
def test_function_parameter_parsing(source, expected):
    l: Lexer = Lexer.new(source)
    p: Parser = Parser.new(l)

    program = p.parse_program()
    check_parser_error(p)

    statement = program.statements[0]

    import pdb

    # pdb.set_trace()
    parsed_parameters = [x.value for x in statement.expression.parameters]
    assert parsed_parameters == expected


def test_function_parameters():
    l: Lexer = Lexer.new("add(1, 2 * 3, 4 + 5);")
    p: Parser = Parser.new(l)

    program = p.parse_program()
    check_parser_error(p)
    assert len(program.statements) == 1

    statement = program.statements[0]
    expression = statement.expression
    assert len(expression.arguments) == 3

    assert expression.arguments[0].value == 1

    assert expression.arguments[1].left.value == 2
    assert expression.arguments[1].operator == "*"
    assert expression.arguments[1].right.value == 3

    assert expression.arguments[2].left.value == 4
    assert expression.arguments[2].operator == "+"
    assert expression.arguments[2].right.value == 5


@pytest.mark.parametrize(
    "source, identifier, expected",
    [
        ("let x = 5;", "x", 5),
        ("let y = true;", "y", True),
        ("let foobar = y;", "foobar", "y"),
    ],
)
def test_let_statement_values(source, identifier, expected):
    l: Lexer = Lexer.new(source)
    p: Parser = Parser.new(l)
    program = p.parse_program()
    check_parser_error(p)
    assert len(program.statements) == 1
    statement = program.statements[0]
    assert statement.name.value == identifier
    assert statement.value.value == expected
    import pdb

    # pdb.set_trace()
