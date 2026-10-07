# Calculator Backend

Flask + SQLite backend for a front-end/back-end separated calculator system.

## Features

- Basic arithmetic
- Compound expressions
- Operator precedence
- Parentheses
- Unary positive/negative signs
- Decimal numbers
- Invalid expression handling
- Division-by-zero handling
- SQLite history persistence
- Query history API
- Delete specified history API
- No `eval()` / `exec()` or equivalent arbitrary-code execution

## Runtime

- Python 3.10+ recommended
- pip

## Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Start backend

Run from the backend repository root:

```bash
python -m src.app
```

Default address:

```text
http://127.0.0.1:5000
```

Health check:

```text
GET /api/health
```

## Database

SQLite is initialized automatically on backend startup.

Default database file:

```text
calculator.db
```

Table:

```text
calculation_history
- id
- expression
- result
- created_at
```

The database path can be changed using:

```text
CALCULATOR_DB_PATH=/path/to/calculator.db
```

## CORS

Development default:

```text
ALLOWED_ORIGINS=*
```

For deployment, set it to your public frontend origin when possible.

## APIs

### Calculate

```text
POST /api/calculate
```

Request:

```json
{
  "expression": "(1+2)*3"
}
```

Success:

```json
{
  "success": true,
  "expression": "(1+2)*3",
  "result": "9"
}
```

### Get history

```text
GET /api/history
```

### Delete one record

```text
DELETE /api/history/{id}
```

## Tests

```bash
pytest
```

## Production example

```bash
gunicorn -w 2 -b 0.0.0.0:5000 src.app:app
```

If you deploy on a server, keep the SQLite file on persistent storage.
