import ast
import os

# Get all constants defined in core/constants.py
constants_defined = set()
with open('core/constants.py', 'r') as f:
    tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    constants_defined.add(target.id)

print(f"Defined constants: {sorted(constants_defined)}")

# Check all Python files for imports from core.constants
missing_constants = {}

for root, dirs, files in os.walk('api/apps'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                try:
                    tree = ast.parse(f.read())
                except SyntaxError:
                    continue
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        if node.module == 'core.constants':
                            for alias in node.names:
                                const_name = alias.name
                                if const_name not in constants_defined:
                                    if filepath not in missing_constants:
                                        missing_constants[filepath] = []
                                    missing_constants[filepath].append(const_name)

if missing_constants:
    print("\nMissing constants:")
    for filepath, consts in missing_constants.items():
        print(f"\n{filepath}:")
        for const in consts:
            print(f"  - {const}")
else:
    print("\nAll imports are valid!")
