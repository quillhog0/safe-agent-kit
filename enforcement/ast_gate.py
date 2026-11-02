#!/usr/bin/env python3
"""ast_gate.py — compare two Python files with comments/docstrings stripped.
Usage: python3 ast_gate.py original.py modified.py
Exit 0 if syntax trees match, 1 otherwise.
"""
import ast
import sys

def strip(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], 'value', None), ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body = node.body[1:]
    return tree

def main():
    if len(sys.argv) != 3:
        print("Usage: ast_gate.py original.py modified.py", file=sys.stderr)
        sys.exit(2)
    try:
        with open(sys.argv[1]) as f:
            t1 = strip(ast.parse(f.read()))
        with open(sys.argv[2]) as f:
            t2 = strip(ast.parse(f.read()))
    except SyntaxError as e:
        print(f"Syntax error: {e}", file=sys.stderr)
        sys.exit(1)
    if ast.dump(t1) == ast.dump(t2):
        print("AST gate: pass")
        sys.exit(0)
    else:
        print("AST gate: trees differ", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
