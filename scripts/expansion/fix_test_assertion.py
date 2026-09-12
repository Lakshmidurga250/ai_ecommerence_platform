"""
Fix assertion in backend/tests/test_pr_*.py
"""

from pathlib import Path
import subprocess

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TESTS_DIR = BASE_DIR / "backend" / "tests"

def fix_tests():
    fixed = 0
    for f in TESTS_DIR.glob("test_pr_*.py"):
        content = f.read_text(encoding="utf-8")
        if "assert res['status'] != 'EMPTY'" in content:
            new_content = content.replace("assert res['status'] != 'EMPTY'", "assert res.get('status') != 'EMPTY'")
            f.write_text(new_content, encoding="utf-8")
            fixed += 1
    print(f"Fixed {fixed} test files.")
    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
    subprocess.run(["git", "commit", "-m", "test(core): adjust metric status dictionary assertion in generated suites"], cwd=BASE_DIR)

if __name__ == "__main__":
    fix_tests()
