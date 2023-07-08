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
        case ast.InfixExpression:
            left = eval(node.left)
            right = eval(node.right)
            return eval_infix_expression(node.operator, left, right)
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
        case "-":
            return eval_minus_prefix_operator_expression(right)
        case _:
            return NULL


def eval_minus_prefix_operator_expression(right: object.Object) -> object.Object:
    LOGGER.debug(right)
    if right.object_type() != object.Type.INTEGER_OBJ:
        return NULL
    value = right.value
    return object.Integer(value=-value)


def eval_bang_operator_expression(right: object.Object) -> object.Object:
    LOGGER.debug(f"eval_bang right {right}")

    LOGGER.debug(f"eval_bang {right.value == TRUE.value}")
    # import pdb

    # pdb.set_trace()
    if isinstance(right, object.Null):
        return TRUE
    match bool(right.value) == TRUE.value:
        case True:
            return FALSE
        case False:
            return TRUE


def eval_infix_expression(
    operator: str, left: object.Object, right: object.Object
) -> object.Object:
    if (
        left.object_type() == object.Type.INTEGER_OBJ
        and right.object_type() == object.Type.INTEGER_OBJ
    ):
        return eval_integer_infix_expression(operator, left, right)
    else:
        return NULL


def eval_integer_infix_expression(
    operator: str, left: object.Object, right: object.Object
) -> object.Object:
    left_value = left.value
    right_value = right.value
    match operator:
        case "+":
            return object.Integer(value=left_value + right_value)
        case "-":
            return object.Integer(value=left_value - right_value)
        case "*":
            return object.Integer(value=left_value * right_value)
        case "/":
            return object.Integer(value=left_value / right_value)
        case _:
            return NULL
