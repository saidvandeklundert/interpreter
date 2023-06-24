import pytest
from src.token import Token, TokenType, TokenTypes
from src.lexer import Lexer
from src.parser import Parser
from src.ast import Program, Statement, LetStatement, Identifier

PROGRAM = """
let x = 5;
let y = 10;
let foobar = 838383;"""


def test_let_statement():
    l: Lexer = Lexer.new(PROGRAM)
    p: Parser = Parser.new(l)

    program = p.parse_program()

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
        name=Identifier(token=Token(Type=TokenTypes.IDENT, Literal="x"), value="x"),
        value=None,
    )
    assert isinstance(statement, LetStatement)
    assert statement.token.Type == TokenTypes.LET
    assert statement.token.Literal == "let"
    assert statement.token_literal() == "let"
    assert statement.name.value == "x"
