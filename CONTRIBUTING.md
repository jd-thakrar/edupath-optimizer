# Contributing to EduPath Optimizer

Thanks for your interest in contributing.

## Getting Started

1. Fork the repository and create a branch from `main`.
2. Set up the backend:
   - `cd backend`
   - `python -m venv venv`
   - `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
   - `pip install -r ../requirements.txt`
   - `cp .env.example .env`
3. Run local checks:
   - `python -m compileall backend`
   - `python -m unittest discover -s backend -p "test*.py"` (if tests exist)

## Development Guidelines

- Keep changes focused and minimal.
- Never commit secrets, API keys, or private credentials.
- Use `.env` for local secrets and keep `.env.example` as the public template.
- Update documentation when behavior or setup changes.

## Pull Request Process

1. Open an issue for significant changes before implementation.
2. Keep one topic per PR.
3. Ensure CI checks pass.
4. Fill out the pull request template completely.
5. Link the related issue (`Fixes #<issue_number>` when applicable).

## Issue and PR Response Policy

- Maintainers target first response on new issues/PRs within **5 business days**.
- Security reports should follow `SECURITY.md` and not be filed publicly.

## Scope of Contributions

Contributions are welcome for:
- AI model and explainability improvements
- API reliability and security hardening
- Frontend UX improvements
- Test coverage and documentation

Out of scope without prior maintainer agreement:
- Large architecture rewrites
- Breaking API redesigns
- Vendor lock-in specific integrations
