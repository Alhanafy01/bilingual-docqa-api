# bilingual-docqa-api

A question-answering API over Arabic and English documents: upload documents, ask questions in either language, get answers grounded in cited sources.

> **Status: work in progress (Phase 1: foundations).** The service skeleton, configuration, tests and code-quality tooling are in place. Document ingestion, retrieval (RAG) and evaluation come next; see the [roadmap](#roadmap).

## Why

Most document Q&A demos assume English-only, clean text. Real documents in the Gulf and Egypt are often Arabic, English, or both in the same file. This project aims to handle that properly, and to prove it with an evaluation report rather than a demo.

## Tech stack

| Area | Choice |
|---|---|
| Language | Python 3.12 |
| API | FastAPI (async) |
| Configuration | pydantic-settings (typed settings from environment / `.env`) |
| Packaging | uv, `src/` layout, hatchling |
| Testing | pytest, FastAPI `TestClient` |
| Code quality | ruff (lint + format, incl. security rules), mypy (strict), pre-commit |
| Planned | PostgreSQL + pgvector, SQLAlchemy + Alembic, Docker Compose, GitHub Actions CI, LLM APIs, Ragas evaluation |

## Getting started

Prerequisites: [uv](https://docs.astral.sh/uv/) and Git. uv installs the right Python version for you.

```bash
git clone git@github.com:Alhanafy01/bilingual-docqa-api.git
cd bilingual-docqa-api

uv sync                          # create .venv and install dependencies from uv.lock
cp .env.example .env             # local settings (never commit .env)
uv run pre-commit install        # enable the git hooks

uv run fastapi dev src/app/main.py
```

Then open:

- http://127.0.0.1:8000/health returns `{"status": "ok", "environment": "local"}`
- http://127.0.0.1:8000/docs for the interactive API docs

## Development

```bash
uv run pytest                    # tests
uv run ruff check .              # lint
uv run ruff format .             # format
uv run mypy src tests            # type check (strict)
uv run pre-commit run --all-files  # everything the git hook runs
```

Every commit is checked by pre-commit hooks: formatting, lint, strict typing, trailing whitespace, large files (> 500 KB) and private keys.

## Configuration

Settings are read from environment variables or a local `.env` file (see `.env.example`):

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `Bilingual DocQA API` | Title shown in the API docs |
| `ENVIRONMENT` | `local` | Deployment environment name |
| `DEBUG` | `false` | FastAPI debug mode |

## Project structure

```
src/app/
├── main.py          # FastAPI app and routes
└── core/
    └── config.py    # typed settings
tests/
├── conftest.py      # shared fixtures (test client)
└── test_health.py
```

## Roadmap

- [x] Project skeleton: uv, FastAPI, typed settings, health endpoint
- [x] Tests with pytest
- [x] ruff, strict mypy and pre-commit hooks
- [ ] GitHub Actions CI
- [ ] Docker Compose with PostgreSQL + pgvector
- [ ] Document upload, Arabic/English text extraction and chunking
- [ ] Hybrid retrieval (full-text + vector) with reranking
- [ ] `/ask` endpoint with cited, streamed answers
- [ ] Evaluation on a bilingual golden question set (retrieval recall, faithfulness)
- [ ] Security hardening: prompt-injection tests, rate limiting, access control

## Author

Mahmoud Elhanafy, [GitHub @Alhanafy01](https://github.com/Alhanafy01)
