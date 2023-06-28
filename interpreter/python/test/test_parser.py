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
