from src.token import Token
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field
from typing import Union
from pydantic import BaseModel


@dataclass
class Node(ABC):
    """
    A single node in the AST
    """

    token: Token

    @abstractmethod
    def token_literal(self) -> str:
        return self.token.Literal


@dataclass
class Statement(Node):
    @abstractmethod
    def statement_node() -> None:
        ...


@dataclass
class Expression(Node):
    @abstractmethod
    def expression_node(self) -> None:
        ...


@dataclass
class Program:
    statements: list[Statement] = field(default_factory=list)

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0]
        else:
            return ""

    def __iter__(self) -> Statement:
        return iter(self.statements)

    def __str__(self) -> str:
        return_str = ""
        for statement in self.statements:
            return_str += str(statement) + "\n"
        return return_str


@dataclass
class Identifier(Expression):
    value: str

    def statement_node():
        pass

    def token_literal(self) -> str:
        return self.token.Literal

    def expression_node():
        pass


@dataclass
class LetStatement(Statement):
    """
    Representation of the Let statement in a program.
    """

    # token: Token  inherited from 'Statemen' -> 'Node'
    name: Union[Identifier, None] = None
    value: Union[Expression, None] = None

    def statement_node():
        pass

    def token_literal(self) -> str:
        return self.token.Literal

    def expression_node():
        pass


@dataclass
class ReturnStatement(Statement):
    """
    ReturnStatement structure with a field for the initial token
    and a field for the value of the expression that is to be returned,
    """

    # token: Token  inherited from 'Statemen' -> 'Node'
    return_value: Union[Expression, None] = None

    def statement_node():
        pass

    def token_literal(self) -> str:
        return self.token.Literal


@dataclass
class ExpressionStatement(Statement):
    """
    When we hit the Parser.parse_statement() default case,
    the Parser.parse_expression_statement() runs.

    This method constructs an 'ast.ExpressionStatement',
    can calls `Parser.parse_expression' to fill the content
    of that class by running a function that is registered
    in the 'Parser.prefix_parse_function' registry of functions.
    """

    # token: Token  inherited from 'Statemen' -> 'Node'
    expression: Union[Expression, None] = None

    def statement_node():
        pass

    def token_literal(self) -> str:
        return self.token.Literal


@dataclass
class IntegerLiteral(Expression):
    """
    The IntegerLiteral in the Monkey programming language is
    an expression and thus we inherit from Expression.
    """

    # token: Token  inherited from 'Expression' -> 'Node'
    value: int = 0

    def statement_node():
        pass

    def token_literal(self) -> str:
        return self.token.Literal

    def expression_node(self) -> None:
        pass
