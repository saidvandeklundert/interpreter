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
    """
    Main eval function to evaluate the ast.Node objects.
    """
    match type(node):
        # statements
        case ast.Program:
            return eval_statements(node.statements)

        # expression
        case ast.ExpressionStatement:
            return eval(node.expression)
        case ast.PrefixExpression:
            right = eval(node.right)
            if is_error(right):
                return right
            return eval_prefix_expression(node.operator, right)
        case ast.InfixExpression:
            left = eval(node.left)

            if is_error(left):
                return left

            right = eval(node.right)

            if is_error(right):
                return right
            return eval_infix_expression(node.operator, left, right)
        case ast.IntegerLiteral:
            return object.Integer(value=node.value)
        case ast.Boolean:
            return native_bool_to_boolean_object(node.value)
        case ast.BlockStatement:
            return eval_statements(node.statements)
        case ast.IfExpression:
            return eval_if_expression(node)
        case ast.ReturnStatement:
            val = eval(node.return_value)
            if is_error(val):
                return val
            return object.ReturnValue(value=val)
    return None


def eval_program(program: ast.Program) -> object.Object:
    result: object.Object
    for statement in program.statements:
        result = eval(statement)
        match type(result):
            case object.ReturnValue:
                return result.value
            case object.Error:
                return result

    return result


def eval_blockstatement(block: ast.BlockStatement) -> object.Object:
    result: object.Object
    for statement in block.statements:
        result = eval(statement)

        if result is not None:
            if (
                type(result) == object.Type.RETURN_VALUE_OBJ
                or type(result) == object.Type.ERROR_OBJ
            ):
                return result


def eval_statements(statements: list[ast.Statement]) -> object.Object:
    result: object.Object
    for statement in statements:
        result = eval(statement)
        if type(result) == object.ReturnValue:
            import pdb

            # pdb.set_trace()
            return result.value

        elif hasattr(result, "Error"):
            # not defined yet??
            return result
    return result


def native_bool_to_boolean_object(input: bool) -> object.Boolean:
    if input:
        return TRUE
    return FALSE


def is_error(obj: object.Object) -> bool:
    if obj is not None:
        return obj.object_type() == object.Type.ERROR_OBJ
    return False


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
    elif operator == "==":
        return native_bool_to_boolean_object(left == right)
    elif operator == "!=":
        return native_bool_to_boolean_object(left != right)

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
        case "<":
            return native_bool_to_boolean_object(left_value < right_value)
        case ">":
            return native_bool_to_boolean_object(left_value > right_value)
        case "==":
            return native_bool_to_boolean_object(left_value == right_value)
        case "!=":
            return native_bool_to_boolean_object(left_value != right_value)
        case _:
            return NULL


def eval_if_expression(if_expression: ast.IfExpression) -> object.Object:
    condition = eval(if_expression.condition)
    if is_error(condition):
        return condition
    if is_truthy(condition):
        return eval(if_expression.consequence)
    elif if_expression.alternative != None:
        return eval(if_expression.alternative)
    else:
        return None


def is_truthy(obj: object.Object) -> bool:
    if obj is NULL:
        return False
    elif obj is TRUE:
        return True
    elif obj is FALSE:
        return False
    else:
        return True
