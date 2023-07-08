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
    def object_type() -> ObjectType:
        ...

    @abstractmethod
    def inspect() -> str:
        ...


@dataclass
class Integer(Object):
    value: int

    def object_type() -> ObjectType:
        return Type.INTEGER_OBJ.value

    def inspect(self) -> str:
        return str(self.value)


@dataclass
class Boolean(Object):
    value: bool

    def object_type() -> ObjectType:
        return Type.BOOLEAN_OBJ.value

    def inspect(self) -> str:
        return str(self.value)


@dataclass
class Null(Object):
    def object_type() -> ObjectType:
        return Type.NULL_OBJ.value

    def inspect(self) -> str:
        return "null"
