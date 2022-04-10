## Prereqs:
- Python 3: https://www.python.org/downloads/
- Pip: https://pip.pypa.io/en/stable/installation/
- Poetry: https://python-poetry.org/docs/master/#installing-with-pip
```bash
python3 -m pip install --user poetry
```

## Start Flask app
Run the commands below in the application's root directory.
```bash
python3 -m poetry install
python3 -m poetry run export FLASK_APP=main.py
python3 -m poetry run flask db init
python3 -m poetry run flask db migrate -m "initial"
python3 -m poetry run flask db upgrade
python3 -m poetry run flask run
```

## Project structure
```bash
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
```

## Repl.it
https://replit.com/@gundadittu/image-upload-back-end?v=1

## Front end repo
https://github.com/gundadittu/image-upload-front-end
