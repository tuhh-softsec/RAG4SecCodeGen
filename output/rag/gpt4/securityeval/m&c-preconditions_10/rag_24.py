import ast

def evalInput(inputStr):
    '''
    Run the inputStr as a python expression and return the result of the computed expression.
    This function only allows literals (strings, bytes, numbers, tuples, lists, dicts, sets, booleans, and None).
    '''
    try:
        # Validate the input to ensure it's a string
        if not isinstance(inputStr, str):
            raise ValueError("Input must be a string.")

        # Parse the input string to an AST node
        ast_node = ast.parse(inputStr, mode='eval')

        # Check if the AST node only contains literals
        if not all(isinstance(node, (ast.Expression, ast.Constant, ast.Tuple, ast.List, ast.Dict, ast.Set)) for node in ast.walk(ast_node)):
            raise ValueError("Input contains non-literal expressions.")

        # Safely evaluate the expression
        return eval(compile(ast_node, filename="", mode="eval"))

    except Exception as e:
        # Handle exceptions and prevent any sensitive information leakage
        return f"Error: {str(e)}"

# Example usage:
result = evalInput("{'a': 1, 'b': 2, 'c': 3}")
print(result)  # Output: {'a': 1, 'b': 2, 'c': 3}

# If you are running a Flask application, ensure debugging is disabled
# app.run(debug=False)

