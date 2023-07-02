from __future__ import annotations
from src import ast
from src import lexer
from src import token
import logging
from typing import Callable
from enum import IntEnum

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

PrefixParseFunction = Callable[[], ast.Expression]
InfixParseFunction = Callable[[ast.Expression], ast.Expression]


class Precedence(IntEnum):
    LOWEST = 1
    EQUALS = 2  # ==
    LESSGREATER = 3  # > or <
    SUM = 4  # +
    PRODUCT = 5  # *
    PREFIX = 6  # -X or !X
    CALL = 7  # myFunction(X)


PRECEDENCES: dict[token.TokenTypes, int] = {
    token.TokenTypes.EQ: Precedence.EQUALS,
    token.TokenTypes.NOT_EQ: Precedence.EQUALS,
    token.TokenTypes.LT: Precedence.LESSGREATER,
    token.TokenTypes.GT: Precedence.LESSGREATER,
    token.TokenTypes.PLUS: Precedence.SUM,
    token.TokenTypes.MINUS: Precedence.SUM,
    token.TokenTypes.SLASH: Precedence.PRODUCT,
    token.TokenTypes.ASTERISK: Precedence.PRODUCT,
    token.TokenTypes.LPAREN: Precedence.CALL,
}


class Parser:
    def __init__(self, l: lexer.Lexer):
        self.l: lexer.Lexer = l
        self.cur_token: token.Token | None = None
        self.peek_token: token.Token | None = None
        self.errors: list[str] = []
        self.prefix_parse_function: dict[str, PrefixParseFunction] = {}
        self.register_prefix_function(token.TokenTypes.IDENT, self.parse_identifier)
        self.register_prefix_function(token.TokenTypes.INT, self.parse_integer_literal)
        self.register_prefix_function(
            token.TokenTypes.BANG, self.parse_prefix_expression
        )
        self.register_prefix_function(
            token.TokenTypes.MINUS, self.parse_prefix_expression
        )
        self.register_prefix_function(token.TokenTypes.TRUE, self.parse_boolean)
        self.register_prefix_function(token.TokenTypes.FALSE, self.parse_boolean)
        self.register_prefix_function(
            token.TokenTypes.LPAREN, self.parse_grouped_expression
        )
        self.register_prefix_function(token.TokenTypes.IF, self.parse_if_expression)
        self.register_prefix_function(
            token.TokenTypes.FUNCTION, self.parse_function_literal
        )
        # register infix operators
        self.infix_parse_function: dict[str, InfixParseFunction] = {}
        self.register_infix_function(token.TokenTypes.PLUS, self.parse_infix_expression)
        self.register_infix_function(
            token.TokenTypes.MINUS, self.parse_infix_expression
        )
        self.register_infix_function(
            token.TokenTypes.SLASH, self.parse_infix_expression
        )
        self.register_infix_function(
            token.TokenTypes.ASTERISK, self.parse_infix_expression
        )
        self.register_infix_function(token.TokenTypes.EQ, self.parse_infix_expression)
        self.register_infix_function(
            token.TokenTypes.NOT_EQ, self.parse_infix_expression
        )
        self.register_infix_function(token.TokenTypes.LT, self.parse_infix_expression)
        self.register_infix_function(token.TokenTypes.GT, self.parse_infix_expression)
        self.register_infix_function(
            token.TokenTypes.LPAREN, self.parse_call_expression
        )

    @staticmethod
    def new(l: lexer.Lexer) -> Parser:
        """
        Creates a new instance of the Parser and sets the cur_token and
        peek_token to the proper starting position.

        The __init__ takes care of the setup of the individual attributes of the
         instance of the Parser.
        """
        p = Parser(l=l)

        p.next_token()
        p.next_token()
        return p

    def next_token(self) -> None:
        """
        What this method provides the parser with is that:
        - we have a 'self.cur_token' that we can operate on as the current token
        - we have a 'peek_token' so we understand what token will be next

        How it works:
        - set curtoken to peek_token
        - set peek_token by calling 'next_token' on the Lexer which:
          - converts the char under evaluation to a token, returns it and advances the lexer
        """
        self.cur_token = self.peek_token
        self.peek_token = self.l.next_token()

    def parse_program(self) -> ast.Program:
        """
        Parse the program.:
        - instantiate the ast.Program() (which contains a list of statements)
        - while the token is not EOF:
          - parse the current token using 'parse_statement'
          - append the parsed statement to the program
          - use 'next_token' to have the Lexer parse the next token
        - when EOF is encountered, return the program
        """
        program = ast.Program()
        while self.cur_token.Type != token.TokenTypes.EOF:
            statement = self.parse_statement()
            LOGGER.info(f"parsed {statement}")
            if statement is not None:
                program.statements.append(statement)
            self.next_token()
        return program

    def parse_statement(self) -> ast.Statement:
        """
        Allows for 'self.cur_token' to be parsed as a statement by
        selecting the proper parsing function for the current token Type.

        Returns and executes the matched method, which in turns returns a statement.
        """
        current_token = self.cur_token
        LOGGER.debug(f"current token in parse statement {current_token}")
        match current_token.Type:
            case token.TokenTypes.LET:
                return self.parse_let_statement()
            case token.TokenTypes.RETURN:
                return self.parse_return_statement()
            case _:
                return self.parse_expression_statement()

    def parse_expression_statement(self) -> ast.ExpressionStatement:
        """
        Parse 'self.cur_token' as an ExpressionStatement.

        Creates the Expression statement and parses the expression to set
        the expression attribute of the Expression statement.

        Returns the Expression statement.
        """
        statement = ast.ExpressionStatement(token=self.cur_token)
        statement.expression = self.parse_expression(Precedence.LOWEST)

        if self.peek_token_is(token.TokenTypes.SEMICOLON):
            self.next_token()

        return statement

    def parse_expression(self, precedence: Precedence) -> ast.Expression:
        """
        Parse an expression:
        - use 'self.cur_token.Type' to perform a lookup and determine what
          function to use to parse the expression

        - execute the function that does that actual work of parsing the expression
         and returning an 'ast.Expression'

        - enter while loop that tried to find an infix parse function for the next token
          - if that function is found, it is called passing in the previously found expression
          - this is done again and again untill a token with a higher precedence is encountered

        - return the 'ast.Expression'
        """
        prefix = self.prefix_parse_function.get(self.cur_token.Type)

        LOGGER.info(f"parse_expression prefix {prefix} for {self.cur_token.Type}")
        LOGGER.info(f"{self.prefix_parse_function.keys()}")
        if prefix is None:
            self.no_prefix_parse_function_error(self.cur_token)
            return None
        left_expression = prefix()
        while (
            not self.peek_token_is(token.TokenTypes.SEMICOLON)
            and precedence < self.peek_precedence()
        ):
            infix = self.infix_parse_function.get(self.peek_token.Type)
            if infix is None:
                return left_expression
            self.next_token()
            left_expression = infix(left_expression)

        return left_expression

    def no_prefix_parse_function_error(self, t: token.TokenTypes) -> None:
        message = f"no prefix parse function for {t} found"
        self.errors.append(message)

    def parse_let_statement(self) -> ast.LetStatement:
        """
        Parse 'self.cur_token' and turn it into a LetStatement.

        Returns the LetStatement.
        """
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

    def parse_return_statement(self) -> ast.ReturnStatement:
        """
        Parse 'self.cur_token' and turn it into a ReturnStatement.

        Returns the ReturnStatement.
        """
        LOGGER.info(f"parse return statement {self.cur_token}")
        statement = ast.ReturnStatement(token=self.cur_token)
        self.next_token()

        # skipping expression until we encounter a semicolon
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
            self.peek_error(t)
            return False

    def _errors(self) -> list[str]:
        return self.errors

    def peek_error(self, t: token.TokenTypes) -> None:
        error_message = (
            f"expected next token to be {t}, got {self.peek_token.Type} instead"
        )
        self.errors.append(error_message)

    def register_prefix_function(
        self,
        token_type: token.TokenTypes,
        function: PrefixParseFunction,
    ) -> None:
        """
        Register a PrefixParseFunction to the 'prefix_parse_function'
        register in the Parser.
        """
        self.prefix_parse_function[token_type] = function

    def register_infix_function(
        self,
        token_type: token.TokenTypes,
        function: InfixParseFunction,
    ) -> None:
        """
        Register an InfixParseFunction to the 'infix_parse_function'
        register in the Parser.
        """
        self.infix_parse_function[token_type] = function

    def parse_identifier(self) -> ast.Expression:
        """
        Parsing function for token.IDENT, registered in 'prefix_parse_function'.
        """

        return ast.Identifier(token=self.cur_token, value=self.cur_token.Literal)

    def parse_integer_literal(self) -> ast.Expression:
        literal_expression = ast.IntegerLiteral(token=self.cur_token)
        try:
            value = int(self.cur_token.Literal)
        except Exception as err:
            self.errors.append(f"parse_integer_literal gave {str(err)}")
        LOGGER.info(f"parsed {value} from {self.cur_token}")
        literal_expression.value = value
        return literal_expression

    def parse_prefix_expression(self) -> ast.Expression:
        """
        Builds a PrefixExpression node using the current token.

        In order to set the 'right' attribute, it advances the token and then parses the next token
        using 'parse_expression'. The expression that is returned by this method
        is set as the value for the 'right' attribute.
        """
        expression = ast.PrefixExpression(
            token=self.cur_token, operator=self.cur_token.Literal, right=None
        )
        self.next_token()
        expression.right = self.parse_expression(Precedence.PREFIX)
        return expression

    def peek_precedence(self) -> int:
        """
        Return the precedence of the next token if there is
        a next token.
        """
        if self.peek_token is None:
            return Precedence.LOWEST

        precedence = PRECEDENCES.get(self.peek_token.Type)
        if precedence:
            return precedence
        else:
            return Precedence.LOWEST

    def curr_precedence(self) -> int:
        cur_token = self.cur_token
        if cur_token is None:
            return Precedence.LOWEST

        precedence = PRECEDENCES.get(self.cur_token.Type)
        if precedence:
            return precedence
        else:
            return Precedence.LOWEST

    def parse_infix_expression(self, left_expression: ast.Expression) -> ast.Expression:
        """
        Takes a left expression to build an InifxExpression. The right expression
        is retrieved by moving the token forward one step.
        """
        expression = ast.InfixExpression(
            token=self.cur_token,
            operator=self.cur_token.Literal,
            left=left_expression,
            right=None,
        )
        precedence = self.curr_precedence()
        self.next_token()
        expression.right = self.parse_expression(precedence=precedence)

        return expression

    def parse_boolean(self) -> ast.Expression:
        return ast.Boolean(
            token=self.cur_token, value=self.cur_token_is(token.TokenTypes.TRUE)
        )

    def parse_grouped_expression(self) -> ast.Expression:
        self.next_token()

        expression = self.parse_expression(Precedence.LOWEST)

        if not self.expect_peek(token.TokenTypes.RPAREN):
            return None

        return expression

    def parse_if_expression(self) -> ast.Expression:
        expression = ast.IfExpression(token=self.cur_token)

        if not self.expect_peek(token.TokenTypes.LPAREN):
            return None
        self.next_token()
        expression.condition = self.parse_expression(Precedence.LOWEST)

        if not self.expect_peek(token.TokenTypes.RPAREN):
            return None
        if not self.expect_peek(token.TokenTypes.LBRACE):
            return None
        expression.consequence = self.parse_block_statement()

        if self.peek_token_is(token.TokenTypes.ELSE):
            self.next_token()
            if not self.expect_peek(token.TokenTypes.LBRACE):
                return None
            expression.alternative = self.parse_block_statement()
        return expression

    def parse_block_statement(self) -> ast.BlockStatement:
        block = ast.BlockStatement(token=self.cur_token)
        self.next_token()

        while not self.cur_token_is(token.TokenTypes.RBRACE) and not self.cur_token_is(
            token.TokenTypes.EOF
        ):
            statement = self.parse_statement()
            if statement:
                block.statements.append(statement)
            self.next_token()
        return block

    def parse_function_literal(self) -> ast.Expression:
        literal = ast.FunctionLiteral(token=self.cur_token)

        if not self.expect_peek(token.TokenTypes.LPAREN):
            return None
        literal.parameters = self.parse_function_parameters()

        if not self.expect_peek(token.TokenTypes.LBRACE):
            return None

        literal.body = self.parse_block_statement()

        return literal

    def parse_function_parameters(self) -> list[ast.Identifier]:
        identifiers: list[ast.Identifier] = []

        if self.peek_token_is(token.TokenTypes.RPAREN):
            self.next_token()
            return identifiers

        self.next_token()

        identifier = ast.Identifier(token=self.cur_token, value=self.cur_token.Literal)
        identifiers.append(identifier)
        while self.peek_token_is(token.TokenTypes.COMMA):
            self.next_token()
            self.next_token()
            identifier = ast.Identifier(
                token=self.cur_token, value=self.cur_token.Literal
            )
            identifiers.append(identifier)

        if not self.expect_peek(token.TokenTypes.RPAREN):
            return None

        return identifiers

    def parse_call_expression(self, function: ast.Expression) -> ast.Expression:
        expression = ast.CallExpression(token=self.cur_token, function=function)
        expression.arguments = self.parse_call_arguments()
        return expression

    def parse_call_arguments(self) -> list[ast.Expression]:
        arguments: list[ast.Expression] = []

        if self.peek_token_is(token.TokenTypes.RPAREN):
            self.next_token()
            return arguments

        self.next_token()
        arguments.append(self.parse_expression(Precedence.LOWEST))

        while self.peek_token_is(token.TokenTypes.COMMA):
            self.next_token()
            self.next_token()
            arguments.append(self.parse_expression(Precedence.LOWEST))

        if not self.expect_peek(token.TokenTypes.RPAREN):
            return None

        return arguments
