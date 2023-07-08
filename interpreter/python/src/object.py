from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

ObjectType = str


class Type(Enum):
    INTEGER_OBJ = "INTEGER"
    BOOLEAN_OBJ = "BOOLEAN"
    NULL_OBJ = "NULL"


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
