from __future__ import annotations
from src import ast
from src import lexer
from src import token
from src import object
from typing import Any
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


TRUE = object.Boolean(value=True)
FALSE = object.Boolean(value=False)
NULL = object.Null()


def eval(node: ast.Node) -> Any:
    match type(node):
        # statements
        case ast.Program:
            return eval_statements(node.statements)

        # expression
        case ast.ExpressionStatement:
            return eval(node.expression)
        case ast.PrefixExpression:
            right = eval(node.right)
            return eval_prefix_expression(node.operator, right)

        case ast.IntegerLiteral:
            return object.Integer(value=node.value)
        case ast.Boolean:
            return native_bool_to_boolean_object(node.value)
    return None


def eval_statements(statements: list[ast.Statement]) -> object.Object:
    result: object.Object
    for statement in statements:
        result = eval(statement)
    return result


def native_bool_to_boolean_object(input: bool) -> object.Boolean:
    if input:
        return TRUE
    return FALSE


def eval_prefix_expression(operator: str, right: object.Object) -> object.Object:
    match operator:
        case "!":
            return eval_bang_operator_expression(right)
        case _:
            return NULL


def eval_bang_operator_expression(right: object.Object) -> object.Object:
    LOGGER.debug(f"eval_bang right {right}")

    LOGGER.debug(f"eval_bang {right.value == TRUE.value}")
    # import pdb

    # pdb.set_trace()
    match bool(right.value) == TRUE.value:
        case True:
            return FALSE
        case False:
            return TRUE
