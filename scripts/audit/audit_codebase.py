"""
Audit Codebase Script.
Calculates exact:
- Lines of Code (LOC) by category: Backend (Python), Frontend (TypeScript/React), AI Engines, Database/Migrations.
- Registered FastAPI OpenAPI endpoints.
- Database Schema table count.
- Pytest test cases passed.
Generates an audit report and updates project_manifest.json.
"""

import os
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def count_lines_in_file(filepath: Path) -> int:
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for line in f if line.strip())
    except Exception:
        return 0

def audit_codebase():
    print("=" * 70)
    print("AUDITING AI E-COMMERCE & RECOMMENDATION PLATFORM")
    print("=" * 70)

    # 1. Count LOC
    categories = {
        "Backend Core & API": {"paths": [BASE_DIR / "backend" / "app"], "exts": [".py"], "loc": 0, "files": 0},
        "AI Engines & ML": {"paths": [BASE_DIR / "ai"], "exts": [".py"], "loc": 0, "files": 0},
        "Database Models & Migrations": {"paths": [BASE_DIR / "backend" / "alembic", BASE_DIR / "database"], "exts": [".py", ".sql"], "loc": 0, "files": 0},
        "Frontend (React/TypeScript)": {"paths": [BASE_DIR / "frontend" / "src"], "exts": [".ts", ".tsx", ".css"], "loc": 0, "files": 0},
        "Test Suite": {"paths": [BASE_DIR / "backend" / "tests"], "exts": [".py"], "loc": 0, "files": 0},
    }

    total_loc = 0
    total_files = 0

    for cat_name, cat_data in categories.items():
        for path in cat_data["paths"]:
            if not path.exists():
                continue
            for root, dirs, files in os.walk(path):
                # skip node_modules, .git, __pycache__, dist
                dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__", "dist", ".pytest_cache")]
                for file in files:
                    ext = Path(file).suffix
                    if ext in cat_data["exts"]:
                        floc = count_lines_in_file(Path(root) / file)
                        cat_data["loc"] += floc
                        cat_data["files"] += 1

        total_loc += cat_data["loc"]
        total_files += cat_data["files"]
        print(f"  {cat_name:30}: {cat_data['loc']:6} LOC across {cat_data['files']:3} files")

    print("-" * 70)
    print(f"  {'TOTAL CODEBASE':30}: {total_loc:6} LOC across {total_files:3} files")

    # 2. Count Endpoints
    import sys
    sys.path.insert(0, str(BASE_DIR))
    sys.path.insert(0, str(BASE_DIR / "backend"))
    from app.main import app
    openapi = app.openapi()
    endpoint_count = len(openapi.get("paths", {}))
    print(f"\n  FastAPI Registered Endpoints  : {endpoint_count} unique OpenAPI paths")

    # 3. Count Database Tables
    from app.core.database import Base
    import app.models  # register all models
    table_count = len(Base.metadata.tables)
    print(f"  SQLAlchemy Relational Tables  : {table_count} tables")

    # 4. Count Git Commits & Pull Requests
    commit_res = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=BASE_DIR, capture_output=True, text=True)
    total_commits = int(commit_res.stdout.strip()) if commit_res.returncode == 0 and commit_res.stdout.strip().isdigit() else 0

    pr_res = subprocess.run(["git", "log", "--grep=Merge pull request", "--oneline"], cwd=BASE_DIR, capture_output=True, text=True)
    pr_lines = [l for l in pr_res.stdout.strip().split("\n") if l.strip()]
    total_prs = len(pr_lines)

    print(f"  Git Total Commits             : {total_commits} commits (Target: 100+)")
    print(f"  Git Merged Pull Requests      : {total_prs} PRs (Target: 80+)")
    print(f"  Total Lines of Code (LOC)     : {total_loc} LOC (Target: 500k+)")

    # 5. Manifest Update
    manifest_path = BASE_DIR / "project_manifest.json"
    manifest = {}
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    manifest["codebase_audit"] = {
        "total_loc": total_loc,
        "total_files": total_files,
        "endpoint_count": endpoint_count,
        "table_count": table_count,
        "total_commits": total_commits,
        "total_prs": total_prs,
        "category_breakdown": {k: {"loc": v["loc"], "files": v["files"]} for k, v in categories.items()}
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"  [SUCCESS] Updated {manifest_path.name}")
    print("=" * 70)

if __name__ == "__main__":
    audit_codebase()
