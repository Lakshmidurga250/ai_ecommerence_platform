"""
Rename files with dashes to underscores and fix imports in tests.
"""

import re
from pathlib import Path
import subprocess

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"
AI_DIR = BASE_DIR / "ai"
DB_DIR = BASE_DIR / "database"

def rename_and_fix():
    print("Fixing module names and imports from dashes to underscores...")
    
    # 1. Rename files in backend/app/domain
    domain_dir = BACKEND_DIR / "app" / "domain"
    for f in list(domain_dir.glob("*.py")):
        if "-" in f.name:
            new_name = f.name.replace("-", "_")
            new_path = f.with_name(new_name)
            if new_path.exists():
                new_path.unlink()
            f.rename(new_path)
            print(f"  Renamed domain: {f.name} -> {new_name}")

    # 2. Rename files in ai/
    for f in list(AI_DIR.glob("**/*.py")):
        if "-" in f.name:
            new_name = f.name.replace("-", "_")
            new_path = f.with_name(new_name)
            if new_path.exists():
                new_path.unlink()
            f.rename(new_path)
            print(f"  Renamed AI: {f.name} -> {new_name}")

    # 3. Rename files in database/seeds
    seed_dir = DB_DIR / "seeds"
    for f in list(seed_dir.glob("*.py")):
        if "-" in f.name:
            new_name = f.name.replace("-", "_")
            new_path = f.with_name(new_name)
            if new_path.exists():
                new_path.unlink()
            f.rename(new_path)
            print(f"  Renamed seed: {f.name} -> {new_name}")

    # 4. Fix imports in backend/tests/test_pr_*.py
    tests_dir = BACKEND_DIR / "tests"
    for f in list(tests_dir.glob("test_pr_*.py")):
        content = f.read_text(encoding="utf-8")
        # Replace dashes in imports
        new_content = re.sub(
            r'from backend\.app\.domain\.([a-zA-Z0-9_\-]+) import',
            lambda m: f"from backend.app.domain.{m.group(1).replace('-', '_')} import",
            content
        )
        new_content = re.sub(
            r'from ai\.([a-zA-Z0-9_\-]+)\.([a-zA-Z0-9_\-]+) import',
            lambda m: f"from ai.{m.group(1).replace('-', '_')}.{m.group(2).replace('-', '_')} import",
            new_content
        )
        new_content = re.sub(
            r'from database\.seeds\.([a-zA-Z0-9_\-]+) import',
            lambda m: f"from database.seeds.{m.group(1).replace('-', '_')} import",
            new_content
        )
        if new_content != content:
            f.write_text(new_content, encoding="utf-8")
            print(f"  Fixed test imports: {f.name}")

    # 5. Git add and commit changes to master
    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
    subprocess.run(["git", "commit", "-m", "fix(core): sanitize Python module identifiers with underscores for PEP 8 compliance"], cwd=BASE_DIR)
    print("Done renaming and fixing imports.")

if __name__ == "__main__":
    rename_and_fix()
