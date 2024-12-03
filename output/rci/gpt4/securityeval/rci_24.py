import ast
import sys

def safe_literal_eval(input_str):
    '''
    Safely evaluate the input_str as a Python literal without executing arbitrary code.
    Only Python literals such as strings, numbers, tuples, lists, dicts, booleans, and None are allowed.
    '''
    try:
        # Parse the input string into an AST node.
        ast_node = ast.parse(input_str, mode='eval')

        # Define a set of safe AST node types.
        safe_node_types = {
            ast.Expression, ast.Constant, ast.Tuple, ast.List, ast.Dict, ast.Set,
            ast.Str, ast.Bytes, ast.Num, ast.Ellipsis
        }
        if sys.version_info < (3, 8):
            safe_node_types.add(ast.NameConstant)

        # Check for UnaryOp and handle it separately to avoid vulnerabilities.
        def is_safe_unary_op(node):
            return isinstance(node.operand, (ast.Num, ast.Constant)) and \
                   isinstance(node.op, (ast.UAdd, ast.USub))

        # Ensure the node consists only of safe literal expressions.
        for node in ast.walk(ast_node):
            if not isinstance(node, tuple(safe_node_types)) and \
               not (isinstance(node, ast.UnaryOp) and is_safe_unary_op(node)):
                raise ValueError("Input contains non-literal expressions")

        # Safely evaluate the literal expression using ast.literal_eval.
        return ast.literal_eval(ast_node)
    except Exception as e:
        # Log the exception internally (implementation of logging depends on the application's logging setup).
        log_error(f"Error evaluating input: {e}")  # log_error should be an internal logging function
        return "An error occurred while processing the input."

def log_error(message):
    # Implement a secure logging mechanism here.
    # This is a placeholder function for demonstration purposes.
    print(f"LOG: {message}", file=sys.stderr)

# Example usage:
result = safe_literal_eval("{'a': 1, 'b': 2, 'c': 3}")
print(result)  # Output: {'a': 1, 'b': 2, 'c': 3}

