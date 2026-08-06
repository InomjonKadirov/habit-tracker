# Habit Tracker

## Project Overview

A habit tracker app: a FastAPI service for creating habits, recording daily check-ins, and viewing streak/completion statistics. Habits are persisted in a database (SQLite by default), each habit records daily check-ins (one per date), and the service exposes endpoints to create and list habits, record and review check-ins, and view per-habit streak and completion statistics. The habits list endpoint returns habits ordered by their creation timestamp, oldest first.

## Main features

- **Habits**: create, list (optionally active-only), retrieve, update, and archive habits (`app/main.py`, `app/crud.py`).
- **Check-ins**: record a daily check-in per habit (one per date, enforced by a unique constraint), list check-ins, and delete a check-in.
- **Stats**: per-habit current streak, longest streak, total check-ins, and 30-day completion rate (`app/stats.py`).
- **Data models**: `Habit` and `Checkin` SQLAlchemy models backed by SQLite by default (`app/models.py`, `app/database.py`).
- **Pydantic schemas** for request/response validation (`app/schemas.py`).
- **Test suite** using `pytest` + `httpx` against an in-memory SQLite database (`tests/`).

## Requirements

Minimum Python version: >=3.12

## Installation

The repository uses [uv](https://github.com/astral-sh/uv) (a `uv.lock` is committed and CI runs `uv sync`). From the repository root, the recommended command is:

```bash
uv sync
```

This installs the project and its dependencies declared in `pyproject.toml` (FastAPI, uvicorn, SQLAlchemy, python-multipart) plus the dev group (pytest, httpx).

Alternatively, since the project is a standard `pyproject.toml` package (hatchling backend, no `requirements.txt`/Poetry), you can install it with pip in editable mode:

```bash
pip install -e .
```

Use `uv sync` to get the exact pinned dependency set from `uv.lock`; use `pip install -e .` when you prefer a plain pip workflow without uv.

## Running Locally

Start the FastAPI app with uvicorn (declared as a dependency):

```bash
uv run uvicorn app.main:app --reload
```

The API is then served at `http://127.0.0.1:8000` (interactive docs at `/docs`). By default it uses a local SQLite file (`./habits.db`); override the database with the `DATABASE_URL` environment variable.

## Running the tests

```bash
uv run pytest -q
```

## Project structure

- `app/` — application package:
  - `main.py` — FastAPI app and REST endpoints (habits, check-ins, stats).
  - `models.py` — SQLAlchemy `Habit` and `Checkin` models.
  - `schemas.py` — Pydantic request/response schemas.
  - `crud.py` — database operations for habits and check-ins.
  - `stats.py` — streak and completion-rate calculations.
  - `database.py` — SQLAlchemy engine, session, and table creation.
- `tests/` — pytest tests and fixtures (`conftest.py`, `test_habits.py`, `test_checkins.py`).
- `pyproject.toml` — project metadata, dependencies, and dev dependency group.
- `uv.lock` — locked dependency versions for reproducible installs.
- `.github/workflows/ci.yml` — CI workflow that runs `uv sync` then `uv run pytest -q` on every push.

## Notes

This README was composed strictly from repository contents (source files, `pyproject.toml`, `uv.lock`, and the CI workflow). No run scripts beyond the `uv` commands above were found in the repo; the `uvicorn` invocation is the standard way to run the FastAPI app defined in `app/main.py`.