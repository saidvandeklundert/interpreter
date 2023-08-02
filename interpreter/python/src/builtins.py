from __future__ import annotations
from src import ast
from src import lexer
from src import token
from src import object
from src import evaluator

from typing import Any


def new_error(format: str, *arg: Any) -> object.Error:
    error_message = ""
    error_message += format
    for item in arg:
        error_message += f" {item}"
    return object.Error(message=f"{error_message}")
