from __future__ import annotations
from typing import Union
from src.token import Token, TokenTypes, lookup_identifier
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class Lexer:
    """
    The Lexer.

    input: source code that needs lexing
    position: current position in input, pointing to the current char
    read_position: current reading position
    char: current char that is being evaluated
    """

    def __init__(
        self,
        input: str,
        position: int,
        read_position: int,
        char: Union[str, None],
    ):
        self.input = input
        self.position = position
        self.read_position = read_position
        self.char = char

    @staticmethod
    def new(source_code: str) -> Lexer:
        """
        Provide a new lexer that points to the first char
        in the source code.
        """
        lexer = Lexer(
            input=source_code,
            position=0,
            read_position=0,
            char=None,
        )
        lexer.read_char()
        return lexer

    def read_char(self) -> None:
        """
        Read the char that read_position is pointing to and set
        self.char to that value.

        Increment the read_position afterwards.
        """
        if self.read_position >= len(self.input):
            self.char = None
        else:
            self.char = self.input[self.read_position]
            LOGGER.debug(self.char)
        self.position = self.read_position
        self.read_position += 1

    def next_token(self) -> Token:
        """
        Convert the char under evaluation to a token and return it.

        Meanwhile, advance the pointer by calling `read_char` so that the
        char under examination is updated.
        """
        self.skip_whitespace()
        tok = self.char
        LOGGER.debug(f"token assigned: {tok}")

        match tok:
            case "=":
                if self.peek_char() == "=":
                    char = self.char
                    self.read_char()
                    tok = Token(TokenTypes.EQ.value, char + self.char)

                else:
                    tok = Token(TokenTypes.ASSIGN.value, self.char)
            case ";":
                tok = Token(TokenTypes.SEMICOLON.value, self.char)
            case "(":
                tok = Token(TokenTypes.LPAREN.value, self.char)
            case ")":
                tok = Token(TokenTypes.RPAREN.value, self.char)
            case ",":
                tok = Token(TokenTypes.COMMA.value, self.char)
            case "+":
                tok = Token(TokenTypes.PLUS.value, self.char)
            case "-":
                tok = Token(TokenTypes.MINUS.value, self.char)
            case "!":
                if self.peek_char() == "=":
                    char = self.char
                    self.read_char()
                    tok = Token(TokenTypes.NOT_EQ.value, char + self.char)
                else:
                    tok = Token(TokenTypes.BANG.value, self.char)
            case "/":
                tok = Token(TokenTypes.SLASH.value, self.char)
            case "*":
                tok = Token(TokenTypes.ASTERISK.value, self.char)
            case "<":
                tok = Token(TokenTypes.LT.value, self.char)
            case ">":
                tok = Token(TokenTypes.GT, self.char)
            case ",":
                tok = Token(TokenTypes.COMMA.value, self.char)
            case "{":
                tok = Token(TokenTypes.LBRACE.value, self.char)
            case "}":
                tok = Token(TokenTypes.RBRACE.value, self.char)
            case "[":
                tok = Token(TokenTypes.LBRACKET.value, self.char)
            case "]":
                tok = Token(TokenTypes.RBRACKET.value, self.char)
            case None:
                tok = Token(TokenTypes.EOF.value, self.char)
            case '"':
                string = self.read_string()
                tok = Token(Type=TokenTypes.STRING, Literal=string)

            case _:
                if self.is_letter(self.char):
                    token_literal = self.read_identifier()
                    token_type = lookup_identifier(token_literal)
                    return Token(Literal=token_literal, Type=token_type)
                elif self.is_digit(self.char):
                    return Token(Literal=self.read_number(), Type=TokenTypes.INT)
                else:
                    tok = new_token(TokenTypes.ILLEGAL, self.char)

        self.read_char()
        return tok

    def read_identifier(self) -> str:
        position = self.position

        while self.char and self.is_letter(self.char):
            self.read_char()
        return self.input[position : self.position]

    def read_string(self) -> str:
        """
        Read a string literal after triggering the following in the lexer:
         case '"':
        """
        position = self.position + 1

        while self.char:
            self.read_char()
            if self.char == '"' or self.char == 0:
                break
        return self.input[position : self.position]

    @staticmethod
    def is_letter(char: str) -> bool:
        if len(char) != 1:
            raise ValueError(f"char should be 1 character, got {char}")
        return char.isalpha() or char == "_"

    @staticmethod
    def is_digit(char: str | None) -> bool:
        if char is None:
            return False
        return char.isdigit()

    def read_number(self) -> str:
        position = self.position
        LOGGER.info(f"read number self.char {self.char}")
        print("self.char", self.char)
        while self.is_digit(self.char):
            self.read_char()
        return self.input[position : self.position]

    def skip_whitespace(self) -> None:
        while self.char in [" ", "\t", "\n", "\r"]:
            LOGGER.debug("skip white space")
            self.read_char()

    def peek_char(self) -> str:
        """
        Returns the char at the read position.

        Returns an empty string if EOF is reached.
        """
        if self.read_position >= len(self.input):
            return ""
        else:
            return self.input[self.read_position]


def new_token(tokenType: TokenTypes, char: str) -> TokenTypes:
    tok = Token(Type=tokenType, Literal=char)
    return tok
