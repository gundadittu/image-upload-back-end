## Prereqs:
- Python 3
- Poetry: https://python-poetry.org/docs/#installation

## Start Flask app
```bash
python3 -m poetry install
export FLASK_APP=main.py
flask db init
flask db migrate -m "initial"
flask db upgrade
flask run
```

## Project structure
- main.py (the entry point for the Flask app)
- app/
  - api/
  - database/
- migrations/ (stores database migration info; created when initializating db)
- submissions/ (stores images from user submissions)
  - raw/
  - rotated/
  - faces/
- app.db (stores database tables and rows; created when initializating db)
- config.py
- poetry.lock (needed for dependency management)
- pyproject.toml (needed for dependency management)

## Repl.it
https://replit.com/@gundadittu/image-upload-back-end?v=1
