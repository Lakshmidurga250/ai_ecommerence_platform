# Contributing Guidelines

## Development Workflow
1. Pull the latest `main` branch.
2. Ensure dependencies are up to date (`pip install -r backend/requirements.txt` and `npm install` in `frontend`).
3. Run automated tests before committing:
   ```bash
   pytest backend/tests/
   ```
4. Follow conventional commit messages:
   - `feat(module): description`
   - `fix(module): description`
   - `test(module): description`
   - `docs(module): description`
5. Keep `PROJECT_PROGRESS.md` and `project_manifest.json` updated with any completed features or new modules.

<!-- Contribution guidelines, PR checklist, and branch conventions -->
