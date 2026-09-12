"""
AI Intelligence Engines and Machine Learning Pipelines.
"""

import sys
from pathlib import Path

# Ensure root and backend directories are in sys.path
_root_dir = Path(__file__).resolve().parent.parent
_backend_dir = _root_dir / "backend"

for _p in (str(_root_dir), str(_backend_dir)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
