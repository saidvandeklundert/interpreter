from src.token import Token
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field
from typing import Union


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
    name: Union[Identifier, None] = None
    value: Union[Expression, None] = None

    def statement_node():
        pass

    def token_literal(self) -> str:
        return self.token.Literal

    def expression_node():
        pass
