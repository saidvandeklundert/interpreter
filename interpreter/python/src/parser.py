from __future__ import annotations
from src import ast
from src import lexer
from src import token
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class Parser:
    def __init__(self, l: lexer.Lexer):
        self.l: lexer.Lexer = l
        self.cur_token: token.Token | None = None
        self.peek_token: token.Token | None = None

    @staticmethod
    def new(l: lexer.Lexer) -> Parser:
        p = Parser(l=l)

        p.next_token()
        p.next_token()
        return p

    def next_token(self) -> None:
        self.cur_token = self.peek_token
        self.peek_token = self.l.next_token()

    def parse_program(self) -> ast.Program:
        program = ast.Program()
        while self.cur_token.Type != token.TokenTypes.EOF:
            statement = self.parse_statement()
            LOGGER.info(f"parsed {statement}")
            if statement is not None:
                program.statements.append(statement)
            self.next_token()
        return program

    def parse_statement(self) -> ast.Statement:
        current_token = self.cur_token
        LOGGER.debug(f"current token in parse statement {current_token}")
        match current_token.Type:
            case token.TokenTypes.LET:
                return self.parse_let_statement()

            case _:
                None

    def parse_let_statement(self) -> ast.LetStatement:
        statement = ast.LetStatement(token=self.cur_token)

        if self.expect_peek(token.TokenTypes.IDENT) is False:
            return None

        statement.name = ast.Identifier(
            token=self.cur_token, value=self.cur_token.Literal
        )

        if self.expect_peek(token.TokenTypes.ASSIGN) is False:
            return None
        # skipping expressiong until we encounter a semicolon
        while self.cur_token.Type != token.TokenTypes.SEMICOLON:
            self.next_token()

        return statement

    def cur_token_is(self, t: token.TokenTypes) -> bool:
        return self.cur_token.Type == t

    def peek_token_is(self, t: token.TokenTypes) -> bool:
        return self.peek_token.Type == t

    def expect_peek(self, t: token.TokenTypes) -> bool:
        if self.peek_token_is(t):
            self.next_token()
            return True
        else:
            return False
