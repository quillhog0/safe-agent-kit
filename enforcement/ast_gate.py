#!/usr/bin/env python3
"""ast_gate.py — compare two Python files with docstrings stripped.

This script supports Python only. Comments are already ignored by the
Python parser; the comparison also drops module, class and function
docstrings. It does not check TypeScript, JavaScript or any other language.

Usage: python3 ast_gate.py original.py modified.py
Exit 0 if the syntax trees match, 1 if they differ or a file is unreadable,
2 if usage is wrong or a non-Python path is given.
"""
import ast
import sys
from pathlib import Path


def strip(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(getattr(node.body[0], "value", None), ast.Constant)
                and isinstance(node.body[0].value.value, str)
            ):
                node.body = node.body[1:]
    return tree


def is_python_path(path: str) -> bool:
    return Path(path).suffix == ".py"


def main():
    if len(sys.argv) != 3:
        print("Usage: ast_gate.py original.py modified.py", file=sys.stderr)
        print("Python files only. Other languages are not checked.", file=sys.stderr)
        sys.exit(2)
    original, modified = sys.argv[1], sys.argv[2]
    if not is_python_path(original) or not is_python_path(modified):
        print(
            "ast_gate.py only supports Python source files (.py).",
            file=sys.stderr,
        )
        print("Other languages are not checked by this script.", file=sys.stderr)
        sys.exit(2)
    try:
        with open(original, encoding="utf-8") as f:
            t1 = strip(ast.parse(f.read(), filename=original))
        with open(modified, encoding="utf-8") as f:
            t2 = strip(ast.parse(f.read(), filename=modified))
    except OSError as e:
        print(f"Cannot read file: {e}", file=sys.stderr)
        sys.exit(1)
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
