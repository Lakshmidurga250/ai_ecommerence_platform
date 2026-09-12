"""
Fix nested single quotes in frontend React component titles.
"""

from pathlib import Path
import re
import subprocess

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FE_DIR = BASE_DIR / "frontend" / "src" / "components" / "features"

def fix_quotes():
    fixed = 0
    for f in FE_DIR.glob("*.tsx"):
        content = f.read_text(encoding="utf-8")
        # Match title = '...' where internal quotes might exist
        def replace_title_line(match):
            val = match.group(1).replace("'", "").replace('"', '')
            return f'  title = "{val}",'

        new_content = re.sub(r"^\s*title = '(.*)',\s*$", replace_title_line, content, flags=re.MULTILINE)
        if new_content != content:
            f.write_text(new_content, encoding="utf-8")
            fixed += 1
    print(f"Fixed quotes in {fixed} frontend components.")
    subprocess.run(["git", "add", "-A"], cwd=BASE_DIR)
    subprocess.run(["git", "commit", "-m", "fix(frontend): sanitize title string literal escaping in feature widgets"], cwd=BASE_DIR)

if __name__ == "__main__":
    fix_quotes()
