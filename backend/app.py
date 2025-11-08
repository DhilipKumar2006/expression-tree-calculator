from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import math

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def tokenize(expression):
    """Convert expression string into tokens"""
    # Remove spaces
    expression = expression.replace(' ', '')
    # Tokenize using regex - now including single letters
    tokens = re.findall(r'\d+\.?\d*|[a-zA-Z]|[+\-*/^()]', expression)
    return tokens

def precedence(op):
    """Return precedence of operators"""
    if op in ['+', '-']:
        return 1
    if op in ['*', '/']:
        return 2
    if op in ['^']:
        return 3
    return 0

def infix_to_postfix(tokens):
    """Convert infix notation to postfix using Shunting Yard algorithm"""
    output = []
    operator_stack = []
    
    for token in tokens:
        # Check if token is a number or single letter variable
        if re.match(r'\d+\.?\d*', token) or re.match(r'[a-zA-Z]', token):
            output.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # Remove '('
        elif token in ['+', '-', '*', '/', '^']:
            while (operator_stack and 
                   operator_stack[-1] != '(' and
                   precedence(operator_stack[-1]) >= precedence(token)):
                output.append(operator_stack.pop())
            operator_stack.append(token)
    
    while operator_stack:
        output.append(operator_stack.pop())
    
    return output

def build_expression_tree(postfix):
    """Build expression tree from postfix notation"""
    stack = []
    
    for token in postfix:
        # Check if token is a number or single letter variable
        if re.match(r'\d+\.?\d*', token) or re.match(r'[a-zA-Z]', token):
            # Try to convert to float if it's a number, otherwise keep as string
            try:
                value = float(token)
                node = TreeNode(value)
            except ValueError:
                # It's a variable (letter)
                node = TreeNode(token)
            stack.append(node)
        else:  # Operator
            node = TreeNode(token)
            # Pop two operands
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
    
    return stack[0] if stack else None

def evaluate_tree(root):
    """Evaluate expression tree"""
    if root is None:
        return 0
    
    # Leaf node (operand) - could be number or variable
    if root.left is None and root.right is None:
        # If it's a number, return it; if it's a variable, return as string
        if isinstance(root.value, (int, float)):
            return root.value
        else:
            # For variables, we can't evaluate numerically, so return as string
            return root.value
    
    # Internal node (operator)
    left_val = evaluate_tree(root.left)
    right_val = evaluate_tree(root.right)
    
    # If either value is a string (variable), return expression as string
    if isinstance(left_val, str) or isinstance(right_val, str):
        return f"({left_val} {root.value} {right_val})"
    
    # Both values are numbers, perform calculation
    if root.value == '+':
        return left_val + right_val
    elif root.value == '-':
        return left_val - right_val
    elif root.value == '*':
        return left_val * right_val
    elif root.value == '/':
        if right_val == 0:
            raise ValueError("Division by zero")
        return left_val / right_val
    elif root.value == '^':
        return left_val ** right_val
    
    return 0

def postfix_to_infix(postfix):
    """Convert postfix notation back to infix notation"""
    stack = []
    
    for token in postfix:
        # Check if token is a number or single letter variable
        if re.match(r'\d+\.?\d*', token) or re.match(r'[a-zA-Z]', token):
            stack.append(token)
        else:  # Operator
            # Pop two operands
            right = stack.pop()
            left = stack.pop()
            
            # Add parentheses to maintain order of operations
            if len(stack) > 0 or len(postfix) > 1:
                infix = f"({left} {token} {right})"
            else:
                infix = f"{left} {token} {right}"
            stack.append(infix)
    
    return stack[0] if stack else ""

@app.route('/')
def home():
    return jsonify({"message": "Expression Tree Calculator API"})

@app.route('/evaluate', methods=['POST'])
def evaluate_expression():
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        
        if not expression:
            return jsonify({"error": "No expression provided"}), 400
        
        # Tokenize the expression
        tokens = tokenize(expression)
        
        # Convert to postfix
        postfix = infix_to_postfix(tokens)
        
        # Build expression tree
        tree_root = build_expression_tree(postfix)
        
        # Evaluate the tree
        result = evaluate_tree(tree_root)
        
        # Convert postfix back to infix for display
        infix_from_postfix = postfix_to_infix(postfix)
        
        return jsonify({
            "expression": expression,
            "result": result,
            "postfix": postfix,
            "infix_from_postfix": infix_from_postfix
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)