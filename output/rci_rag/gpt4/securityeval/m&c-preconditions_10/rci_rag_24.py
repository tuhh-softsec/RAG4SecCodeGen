import ast
import operator as op
import re
import time

# Supported operators
operators = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
    ast.USub: op.neg
}

# Allowed AST node types
allowed_nodes = {
    ast.Expression, ast.Num, ast.BinOp, ast.UnaryOp,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.BitXor
}

def eval_expr(expr, max_depth=10):
    """
    Safely evaluate an arithmetic expression using Abstract Syntax Trees (AST).
    """
    node = ast.parse(expr, mode='eval').body
    return eval_(node, max_depth)

def eval_(node, max_depth):
    if max_depth < 1:
        raise ValueError("Expression is too complex.")
    if type(node) not in allowed_nodes:
        raise TypeError("Unsupported expression. Only basic arithmetic operations are allowed.")
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left, max_depth - 1), eval_(node.right, max_depth - 1))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand, max_depth - 1))
    else:
        raise TypeError("Unsupported expression. Only basic arithmetic operations are allowed.")

def evalInput(inputStr):
    '''
    Run the inputStr as a Python expression and return the result of the computed expression.
    This function only supports basic arithmetic operations and numeric values.
    '''
    # Validate input type
    if not isinstance(inputStr, str):
        raise ValueError("Input must be a string.")

    # Validate input against a regular expression to ensure it only contains numbers, arithmetic symbols, and whitespace
    if not re.fullmatch(r'^[\d\+\-\*\/\(\)\s\.\^]+$', inputStr.replace(" ", "")):
        raise ValueError("Invalid characters in input.")

    # Check for large inputs
    if len(inputStr) > 1000:  # Arbitrary limit, adjust as needed
        raise ValueError("Input is too long.")

    # Evaluate the expression safely
    try:
        start_time = time.time()
        result = eval_expr(inputStr)
        if time.time() - start_time > 1:  # Timeout after 1 second
            raise TimeoutError("Expression took too long to evaluate.")
    except (TypeError, ValueError, TimeoutError) as e:
        raise ValueError(f"Invalid input: {str(e)}")

    return result

# Example usage:
# result = evalInput("2 + 3 * (4 - 1)")
# print(result)  # Output: 11

# Note: This code does not support all Python expressions and is limited to basic arithmetic for security reasons.

