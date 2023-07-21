from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from src import ast

ObjectType = str


class Type(Enum):
    INTEGER_OBJ = "INTEGER"
    BOOLEAN_OBJ = "BOOLEAN"
    NULL_OBJ = "NULL"
    RETURN_VALUE_OBJ = "RETURN_VALUE"
    ERROR_OBJ = "ERROR"
    FUNCTION_OBJ = "FUNCTION"


class Object(ABC):
    @abstractmethod
    def object_type() -> Type:
        ...

    @abstractmethod
    def inspect() -> str:
        ...


@dataclass
class Integer(Object):
    value: int

    @staticmethod
    def object_type() -> Type:
        return Type.INTEGER_OBJ

    def inspect(self) -> str:
        return str(self.value)


@dataclass
class Boolean(Object):
    value: bool

    @staticmethod
    def object_type() -> Type:
        return Type.BOOLEAN_OBJ

    def inspect(self) -> str:
        return str(self.value)


@dataclass
class Null(Object):
    @staticmethod
    def object_type() -> Type:
        return Type.NULL_OBJ

    def inspect(self) -> str:
        return "null"


@dataclass
class ReturnValue(Object):
    value: Object

    @staticmethod
    def object_type() -> Type:
        return Type.RETURN_VALUE_OBJ

    def inspect(self) -> str:
        return self.value.inspect()


@dataclass
class Error(Object):
    message: str

    @staticmethod
    def object_type() -> Type:
        return Type.ERROR_OBJ

    def inspect(self) -> str:
        return f"ERROR: {self.message}"


@dataclass
class Environment:
    store: dict[str, Object] = field(default_factory=dict)
    outer: Environment | None = None

    def get(self, name: str) -> None | Object:
        object = self.store.get(name)
        if object is None and self.outer is not None:
            object = self.outer.get(name)
        return object

    def set(self, name: str, val: Object) -> Object:
        self.store[name] = val
        return val


def new_environment() -> Environment:
    return Environment()


def new_enclosed_environment(outer: Environment) -> Environment:
    env = new_environment()
    env.outer = outer
    return env


@dataclass
class Function(Object):
    """
    Representation of a function.

    Functions are first class citizens. They are objects
    and can be passed around as such.
    """

    body: ast.BlockStatement
    env: Environment
    parameters: list[ast.Identifier] = field(default_factory=list)

    @staticmethod
    def object_type() -> Type:
        return Type.FUNCTION_OBJ

    def inspect(self) -> str:
        result = ""
        result += "fn("
        for parameter in self.parameters:
            result += str(parameter)
            result += ","
        if result.endswith(","):
            result = result[:-1]
        result += ") {{\n"
        result += str(self.body)
        result += "\n}"

        return result
