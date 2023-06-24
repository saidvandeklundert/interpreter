import pytest
from src.token import Token, TokenType, TokenTypes
from src.lexer import Lexer


def test_next_token_simple():
    """
    Ensure the lexer can translate source code into the proper tokens.
    """
    source_code = "=+(){},;"

    expected = [
        (TokenTypes.ASSIGN, "="),
        (TokenTypes.PLUS, "+"),
        (TokenTypes.LPAREN, "("),
        (TokenTypes.RPAREN, ")"),
        (TokenTypes.LBRACE, "{"),
        (TokenTypes.RBRACE, "}"),
        (TokenTypes.COMMA, ","),
        (TokenTypes.SEMICOLON, ";"),
        (TokenTypes.EOF, None),
    ]
    lexer = Lexer.new(source_code)
    for idx, tt in enumerate(expected):
        tok = lexer.next_token()
        assert (
            tok.Type == tt[0]
        ), f"expected idx {idx}: incorrect tokenType.\
              Got {tok.Type}, expected {tt[0]}"
        assert (
            tok.Literal == tt[1]
        ), f"expected idx {idx}:incorrect literal.\
              Got {tok.Literal}, expected {tt[1]}"


def test_next_token():
    """
    Ensure the lexer can translate source code into the proper tokens.
    """
    source_code = """let five = 5;
let ten = 10;
let add = fn(x, y) {
x + y;
};
let result = add(five, ten);
!-/*5;
5 < 10 > 5;

if (5 < 10) {
    return true;
} else {
    return false;
}

10 == 10;
10 != 9;"""

    expected = [
        (TokenTypes.LET, "let"),
        (TokenTypes.IDENT, "five"),
        (TokenTypes.ASSIGN, "="),
        (TokenTypes.INT, "5"),
        (TokenTypes.SEMICOLON, ";"),
        (TokenTypes.LET, "let"),
        (TokenTypes.IDENT, "ten"),
        (TokenTypes.ASSIGN, "="),
        (TokenTypes.INT, "10"),
        (TokenTypes.SEMICOLON, ";"),
        (TokenTypes.LET, "let"),
        (TokenTypes.IDENT, "add"),
        (TokenTypes.ASSIGN, "="),
        (TokenTypes.FUNCTION, "fn"),
        (TokenTypes.LPAREN, "("),
        (TokenTypes.IDENT, "x"),
        (TokenTypes.COMMA, ","),
        (TokenTypes.IDENT, "y"),
        (TokenTypes.RPAREN, ")"),
        (TokenTypes.LBRACE, "{"),
        (TokenTypes.IDENT, "x"),
        (TokenTypes.PLUS, "+"),
        (TokenTypes.IDENT, "y"),
        (TokenTypes.SEMICOLON, ";"),
        (TokenTypes.RBRACE, "}"),
        (TokenTypes.SEMICOLON, ";"),
        (TokenTypes.LET, "let"),
        (TokenTypes.IDENT, "result"),
        (TokenTypes.ASSIGN, "="),
        (TokenTypes.IDENT, "add"),
        (TokenTypes.LPAREN, "("),
        (TokenTypes.IDENT, "five"),
        (TokenTypes.COMMA, ","),
        (TokenTypes.IDENT, "ten"),
        (TokenTypes.RPAREN, ")"),
        (TokenTypes.SEMICOLON, ";"),
        (TokenTypes.BANG, "!"),
        (TokenTypes.MINUS, "-"),
        (TokenTypes.SLASH, "/"),
        (TokenTypes.ASTERISK, "*"),
        (TokenTypes.INT, "5"),
        (TokenTypes.SEMICOLON, ";"),
        (TokenTypes.INT, "5"),
        (TokenTypes.LT, "<"),
        (TokenTypes.INT, "10"),
        (TokenTypes.GT, ">"),
        (TokenTypes.INT, "5"),
        (TokenTypes.SEMICOLON, ";"),
        (TokenTypes.IF, "if"),
        (TokenTypes.LPAREN, "("),
        (TokenTypes.INT, "5"),
        (TokenTypes.LT, "<"),
        (TokenTypes.INT, "10"),
        (TokenTypes.RPAREN, ")"),
        (TokenTypes.LBRACE, "{"),
        (TokenTypes.RETURN, "return"),
        (TokenTypes.TRUE, "true"),
        (TokenTypes.SEMICOLON, ";"),
        (TokenTypes.RBRACE, "}"),
        (TokenTypes.ELSE, "else"),
        (TokenTypes.LBRACE, "{"),
        (TokenTypes.RETURN, "return"),
        (TokenTypes.FALSE, "false"),
        (TokenTypes.SEMICOLON, ";"),
        (TokenTypes.RBRACE, "}"),
        (TokenTypes.INT, "10"),
        (TokenTypes.EQ, "=="),
        (TokenTypes.INT, "10"),
        (TokenTypes.SEMICOLON, ";"),
        (TokenTypes.INT, "10"),
        (TokenTypes.NOT_EQ, "!="),
        (TokenTypes.INT, "9"),
        (TokenTypes.SEMICOLON, ";"),
        (TokenTypes.EOF, None),
    ]
    lexer = Lexer.new(source_code)
    for idx, tt in enumerate(expected):
        tok = lexer.next_token()
        print(f"{tok.Literal}  {tok.Type}")
        assert (
            tok.Type == tt[0]
        ), f"expected idx {idx}: incorrect tokenType.\
              Got {tok.Type}, expected {tt[0]}"
        assert (
            tok.Literal == tt[1]
        ), f"expected idx {idx}:incorrect literal.\
              Got {tok.Literal}, expected {tt[1]}"


@pytest.mark.parametrize(
    "char, result",
    [
        ("1", False),
        ("9", False),
        ("=", False),
        ("-", False),
        ("/", False),
        (">", False),
        ("a", True),
        ("i", True),
        ("w", True),
        ("x", True),
        ("Z", True),
        ("D", True),
        ("b", True),
        ("_", True),
    ],
)
def test_lexer_is_letter(char, result):
    assert Lexer.is_letter(char) == result


def test_lexer_read_identifier():
    lexer = Lexer.new("let another_identifier = 10;")
    result = lexer.read_identifier()
    assert result == "let"
    assert lexer.position == 3
    second_result = result = lexer.read_identifier()
    assert second_result == ""
    assert lexer.position == 3
    lexer.position = 4
    lexer.read_char()
    another_identifier = lexer.read_identifier()
    assert another_identifier == "another_identifier"
