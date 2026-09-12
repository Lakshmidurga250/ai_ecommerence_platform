"""
CLI Script to safely and idempotently seed the expanded product catalog into ecommerce.db.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

from database.seeds.seed_catalog_expansion import seed_expanded_catalog

if __name__ == "__main__":
    print("Executing Product Catalog Seeding Pipeline...")
    seed_expanded_catalog()
    print("Product Catalog Seeding successfully completed!")
