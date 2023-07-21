from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

ObjectType = str


class Type(Enum):
    INTEGER_OBJ = "INTEGER"
    BOOLEAN_OBJ = "BOOLEAN"
    NULL_OBJ = "NULL"
    RETURN_VALUE_OBJ = "RETURN_VALUE"
    ERROR_OBJ = "ERROR"


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

    def get(self, name: str) -> None | Object:
        object = self.store.get(name)
        return object

    def set(self, name: str, val: Object) -> Object:
        self.store[name] = val
        return val


def new_environment() -> Environment:
    return Environment()
