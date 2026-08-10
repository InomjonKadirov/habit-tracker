# Contributing

Thanks for your interest in contributing to `habit-tracker`! This guide covers how to set up the project locally and run the tests.

## Local setup

This repository uses [uv](https://docs.astral.sh/uv/) as its dependency manager.

To install dependencies, run the exact command used by CI:

```sh
uv sync
```

## Running the tests

To run the test suite, use the exact command the repository's CI uses:

```sh
uv run pytest -q
```