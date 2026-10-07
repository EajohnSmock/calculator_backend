# Backend Code Style

## Reference

This project follows Python PEP 8 as the primary code style reference.

Reference:

- https://peps.python.org/pep-0008/

## Project Rules

1. Use four spaces for indentation.
2. Use `snake_case` for variables and functions.
3. Use `CapWords` for class names.
4. Keep functions focused on one responsibility.
5. Separate expression parsing, API routing, and database operations.
6. Use explicit exception classes for calculator errors.
7. Never use `eval()`, `exec()`, or equivalent execution of user input.
8. Use parameterized SQL statements rather than string concatenation.
9. Return consistent JSON responses from APIs.
10. Keep lines reasonably short and use descriptive names.
11. Add tests for important expression and API behavior.
12. Do not commit local virtual environments, cache folders, or database files.
