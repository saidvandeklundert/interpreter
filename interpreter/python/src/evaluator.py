from __future__ import annotations
from src import ast
from src import lexer
from src import token
from src import object
from typing import Any
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


TRUE = object.Boolean(value=True)
FALSE = object.Boolean(value=False)
NULL = object.Null()


def eval(node: ast.Node, env: object.Environment) -> Any:
    """
    Main eval function to evaluate the ast.Node objects.
    """
    match type(node):
        # statements
        case ast.Program:
            return eval_statements(node.statements, env)
        case ast.LetStatement:
            val = eval(node.value, env)
            if is_error(val):
                return val
            env.set(name=node.name.value, val=val)

        # expression
        case ast.ExpressionStatement:
            return eval(node.expression, env)
        case ast.PrefixExpression:
            right = eval(node.right, env)
            if is_error(right):
                return right
            return eval_prefix_expression(node.operator, right)
        case ast.InfixExpression:
            left = eval(node.left, env)

            if is_error(left):
                return left

            right = eval(node.right, env)

            if is_error(right):
                return right
            return eval_infix_expression(node.operator, left, right)
        case ast.IntegerLiteral:
            return object.Integer(value=node.value)
        case ast.StringLiteral:
            return object.String(value=node.value)
        case ast.Boolean:
            return native_bool_to_boolean_object(node.value)
        case ast.BlockStatement:
            return eval_statements(node.statements, env)
        case ast.IfExpression:
            return eval_if_expression(node, env)
        case ast.ReturnStatement:
            val = eval(node.return_value, env)
            if is_error(val):
                return val
            return object.ReturnValue(value=val)
        case ast.Identifier:
            return eval_identifier(node, env)
        case ast.CallExpression:
            import pdb

            # pdb.set_trace()
            func = eval(node.function, env)
            if is_error(func):
                # pdb.set_trace()
                return func

            eval_expr_result = eval_expressions(node.arguments, env)
            # pdb.set_trace()
            if len(eval_expr_result) == 1 and is_error(eval_expr_result[0]):
                return eval_expr_result[0]

            return apply_function(func, eval_expr_result)
        case ast.FunctionLiteral:
            parameters = node.parameters
            body = node.body
            return object.Function(parameters=parameters, env=env, body=body)

    return None


def eval_program(program: ast.Program, env: object.Environment) -> object.Object:
    """
    Main function to evaluate a program.

    Takes in the ast.Program and then feeds all the statements to the 'eval'
    function, one at a time.
    """
    result: object.Object
    for statement in program.statements:
        result = eval(statement, env)
        result_type = type(result)
        LOGGER.info(f"result_type: {result_type}")
        LOGGER.info(f"result: {result}")
        # print(f"result_type: {result_type}")
        if result_type == object.ReturnValue:
            return result.value
        elif result_type == object.Error:
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

    return result


def eval_statements(
    statements: list[ast.Statement], env: object.Environment
) -> object.Object:
    result: object.Object
    for statement in statements:
        result = eval(statement, env)
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
            return new_error(f"unkown operator: {operator}{right.object_type()}")


def eval_minus_prefix_operator_expression(right: object.Object) -> object.Object:
    LOGGER.debug(right)
    if right.object_type() != object.Type.INTEGER_OBJ:
        return new_error(f"unknown operator: -{right.object_type()}")
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
    elif (
        left.object_type() == object.Type.STRING_OBJ
        and right.object_type() == object.Type.STRING_OBJ
    ):
        return eval_string_infix_expression(operator, left, right)
    elif left.object_type() != right.object_type():
        return new_error(
            f"type mismatch: {left.object_type()} {operator} {right.object_type()}"
        )

    elif operator == "==":
        return native_bool_to_boolean_object(left == right)
    elif operator == "!=":
        return native_bool_to_boolean_object(left != right)

    else:
        return new_error(
            f"unknown operator: {left.object_type()} {operator} {right.object_type()}"
        )


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
            return new_error(
                f"unkown operator: {left.object_type()} {operator} {right.object_type()}"
            )


def eval_if_expression(
    if_expression: ast.IfExpression, env: object.Environment
) -> object.Object:
    condition = eval(if_expression.condition, env)
    if is_error(condition):
        return condition
    if is_truthy(condition):
        return eval(if_expression.consequence, env)
    elif if_expression.alternative is not None:
        return eval(if_expression.alternative, env)
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


def new_error(format: str, *arg: Any) -> object.Error:
    error_message = ""
    error_message += format
    for item in arg:
        error_message += f" {item}"
    return object.Error(message=f"{error_message}")


def eval_identifier(node: ast.Identifier, env: object.Environment) -> object.Object:
    val = env.get(name=node.value)
    if not val:
        return new_error(f"identifier not found: {node.value}")
    return val


def eval_expressions(
    exps: list[ast.Expression], env: object.Environment
) -> list[object.Object]:
    result: list[object.Object] = []
    import pdb

    # pdb.set_trace()
    for e in exps:
        evaluated = eval(e, env)
        if is_error(evaluated):
            return [object.Object(evaluated)]
        result.append(evaluated)
    return result


def apply_function(fn: object.Object, args: list[object.Object]) -> object.Object:
    LOGGER.info("execuring apply_function")
    print("execuring apply_function")
    import pdb

    # pdb.set_trace()
    func = fn
    extended_env = extended_function_env(func, args)
    evaluated = eval(func.body, extended_env)
    return unwrap_return_value(evaluated)


def extended_function_env(
    func: object.Function, args: list[object.Object]
) -> object.Environment:
    import pdb

    # pdb.set_trace()
    env = object.new_enclosed_environment(func.env)
    for idx, param in enumerate(func.parameters):
        env.set(param.value, args[idx])

    return env


def unwrap_return_value(obj: object.Object) -> object.Object:
    import pdb

    # pdb.set_trace()
    try:
        return_value = obj.ReturnValue
        return return_value.value
    except Exception as err:
        LOGGER.info(err)
        return obj


def eval_string_infix_expression(
    operator: str, left: object.Object, right: object.Object
):
    if operator != "+":
        return new_error(
            f"unknown operator: {left.object_type()} {operator} {right.object_type()}"
        )
    return object.String(value=left.value + right.value)
