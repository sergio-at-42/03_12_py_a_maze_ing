# Install activity dependencies using pip, uv, pipx, or any other package manager of your choice.
install :

# Execute the main script of your activity (e.g., via Python interpreter).
run :

# Run the main script in debug mode using Python’s built-in debugger (e.g., pdb).
debug :

# Remove temporary files or caches (e.g., __pycache__, .mypy_cache) to keep the activity environment clean.
clean :

# flake8 . and mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
lint :

# flake8 . and mypy .
lint-strict (optional) :
