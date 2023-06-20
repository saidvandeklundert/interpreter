from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


TokenType = str  # the type of the token


@dataclass
class Token:
    """
    The way a token is represented by our Lexer.
    """

    Type: TokenType
    Literal: str


class TokenTypes(str, Enum):
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"
    # identifiers
    IDENT = "IDENT"  # add, foobar, x, y, ...
    INT = "INT"  # 1234

    # operators
    ASSIGN = "="
    PLUS = "="

    # delimeters
    COMMA = ","
    SEMICOLON = ";"

    LPAREN = "("
    RPAREN = ")"
    LBRACE = "}"
    RBRACE = "{"

    # keywords
    FUNCTION = "FUNCTION"
    LET = "LET"


KEYWORDS: dict[str, TokenTypes] = {
    "fn": TokenTypes.FUNCTION,
    "let": TokenTypes.LET,
}


def lookup_identifier(identifier: str) -> TokenTypes:
    result = KEYWORDS.get(identifier)
    if result:
        return result
    else:
        return TokenTypes.IDENT
