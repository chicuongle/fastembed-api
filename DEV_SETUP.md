Development setup for fastembed-api

This document describes how to set up a local development environment for this project which uses a TOML-based Python project configuration (Poetry / pyproject.toml).

Relevant files

- [`pyproject.toml`](pyproject.toml:1) — project metadata and dependencies
- [`README.md`](README.md:1) — project overview and Docker build notes

Prerequisites

1. Install Python 3.10 or later (but <4.0). Verify with:

   python --version

2. Install Git (if you need to clone or work with branches).

Recommended tool: Poetry

This project is configured with Poetry via [`pyproject.toml`](pyproject.toml:1). Poetry manages virtual environments and dependencies and is the recommended way to install and run the project.

Install Poetry (one of these options):

- Recommended (install script):

  curl -sSL https://install.python-poetry.org | python3 -

- Using pipx (if you use pipx):

  pipx install poetry

Confirm Poetry works:

  poetry --version

Create / use the virtual environment and install dependencies

From the repository root (where [`pyproject.toml`](pyproject.toml:1) lives):

1. Install dependencies (this creates and uses a Poetry-managed venv):

   poetry install

2. To activate the virtual environment for an interactive shell (optional):

   poetry shell

3. To run commands inside the virtualenv without activating it:

   poetry run <command>

Run the development server

The project includes FastAPI and uvicorn per [`pyproject.toml`](pyproject.toml:1). Start the server in reload mode for development:

  poetry run uvicorn app:app --reload --host 0.0.0.0 --port 8000

Then visit http://localhost:8000 and the interactive docs at http://localhost:8000/docs

Environment variables

If your app requires environment variables, create a local `.env` file in the repo root and add variables there. You can load them in development using packages like python-dotenv or configure uvicorn / the app to read them.

VS Code setup (optional but recommended)

1. Select the Poetry virtualenv interpreter:
   - Open Command Palette (Ctrl+Shift+P) → Python: Select Interpreter → choose the Poetry venv for this project.
2. Install recommended extensions: Python, Pylance, EditorConfig, and optionally Black and Ruff plugins.
3. Add workspace settings (example) to .vscode/settings.json:

{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.testing.pytestEnabled": true
}

Formatting, linting, and testing

- Formatter: black (recommended). Run with:

  poetry run black .

- Linter: ruff (recommended). Run with:

  poetry run ruff .

- Tests: pytest (if tests are added). Run with:

  poetry run pytest

Docker development (quick test)

The repository contains a [`Dockerfile`](Dockerfile:1). To build and run:

  docker build -t fastembed-api .
  docker run -p 8000:8000 fastembed-api

This is useful to reproduce the runtime environment quickly but not necessary for local iterative development.

Pre-commit and CI (recommended)

Add pre-commit hooks (black, ruff, isort, pytest) and a CI pipeline that runs linting/tests on push/PRs.

Common troubleshooting

- If Poetry complains about the Python version, ensure your system Python version matches the constraint in [`pyproject.toml`](pyproject.toml:1).
- To see the full venv path that Poetry uses:

  poetry env info --path

- To remove and recreate the venv:

  poetry env remove $(poetry env list --full-path | awk '{print $1}')
  poetry install

Summary (quick commands)

- Install dependencies: poetry install
- Run server: poetry run uvicorn app:app --reload --host 0.0.0.0 --port 8000
- Format: poetry run black .
- Lint: poetry run ruff .
- Tests: poetry run pytest

Reference files: [`pyproject.toml`](pyproject.toml:1), [`README.md`](README.md:1)
