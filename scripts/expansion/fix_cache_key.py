"""
Fix self._cache key in backend/app/domain/*.py
"""

from pathlib import Path
import subprocess

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOMAIN_DIR = BASE_DIR / "backend" / "app" / "domain"

def fix_cache():
    fixed = 0
    for f in DOMAIN_DIR.glob("*.py"):
        content = f.read_text(encoding="utf-8")
        if "{method_idx}" in content:
            new_content = content.replace("{method_idx}", "val")
            f.write_text(new_content, encoding="utf-8")
            fixed += 1
    print(f"Fixed {fixed} domain files.")
    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
    subprocess.run(["git", "commit", "-m", "fix(domain): resolve cache key variable identifier in domain services"], cwd=BASE_DIR)

if __name__ == "__main__":
    fix_cache()
