# Product Catalog Baseline Audit & Root Cause Analysis

**Date:** 2026-09-12  
**Environment:** Python 3.14 / FastAPI / SQLite (`ecommerce.db`) / React 18 + Vite / TypeScript  

---

## 1. Executive Summary

An audit of the storefront at `http://localhost:5173/products` revealed that only two product items were rendering on the product listing page:
1. **Nike Dri-FIT Men's Moisture-Wicking Training T-Shirt (Black)** — Price: ₹1,795.00
2. **boAt Airdopes 141 ANC True Wireless Earbuds (Gunmetal Black)** — Price: ₹1,799.00

This audit documents the underlying data layer, backend APIs, frontend filtering logic, and the root causes that led to this severe under-population of the storefront.

---

## 2. Baseline Database Metrics

| Metric | Measured Value | Notes |
| :--- | :--- | :--- |
| **Total Products in Database** | **11** | Seeded from `database/seeds/seed_data.py` |
| **Active Products (`is_active=1`)** | 11 | All 11 products active |
| **Featured Products (`is_featured=1`)** | 8 | Rendered on Home page featured section |
| **Categories Count** | 6 | Laptops, Smartphones, Audio, Footwear, Apparel, Kitchen |
| **Sellers Count** | 3 | TechVault, UrbanFit, PureLiving |
| **Brands Count** | 8 | Apple, Samsung, Sony, Dell, Nike, Adidas, Puma, boAt |
| **Total Inventory Records** | 11 | Linked to Central Fulfillment Hub |
| **Total Product Images** | 11 | 1 primary Unsplash image per product |
| **Total Product Reviews** | 4 | Low statistical sample for recommendation engine |
| **Total Product Questions** | 5 | Community Q&A seeded for testing |
| **Total Product Bundles** | 3 | Bundles seeded for testing |

### Products Breakdown by Category in Baseline Database:
- **Laptops & Computing (Category ID 1):** 2 products (Apple MacBook Pro 14 M3 @ ₹199,900, Dell XPS 15 @ ₹174,900)
- **Smartphones & Tablets (Category ID 2):** 2 products (Apple iPhone 15 Pro @ ₹134,900, Samsung Galaxy S24 Ultra @ ₹139,999)
- **Audio & Wearables (Category ID 3):** 2 products (Sony WH-1000XM5 @ ₹28,990, boAt Airdopes 141 ANC @ ₹1,799)
- **Footwear & Running (Category ID 4):** 3 products (Nike Air Zoom Pegasus 40 @ ₹8,995, Adidas Ultraboost Light @ ₹14,999, Puma Velocity Nitro 2 @ ₹4,999)
- **Athletic Apparel (Category ID 5):** 1 product (Nike Dri-FIT Men's Training T-Shirt @ ₹1,795)
- **Home & Kitchen (Category ID 6):** 1 product (PureLiving Barista Pro Espresso Machine @ ₹12,499)

---

## 3. Root Cause Analysis: Why Only Two Products Were Displayed

The root cause was determined to be a **compound multi-layer constraint**:

### Root Cause 1: Client-Side Price Slider Hardcoding (`ProductListPage.tsx`)
In `frontend/src/pages/ProductListPage.tsx`:
```tsx
const [minPrice, setMinPrice] = useState<number>(0);
const [maxPrice, setMaxPrice] = useState<number>(2000); // <-- Hardcoded to 2,000!
...
const filteredProducts = products.filter((p) => {
  if (p.price < minPrice || p.price > maxPrice) return false;
  if (inStockOnly && p.stock <= 0) return false;
  return true;
});
...
<input
  type="range"
  min="0"
  max="2000" // <-- Slider capped at 2,000
  step="50"
  value={maxPrice}
  onChange={(e) => setMaxPrice(Number(e.target.value))}
/>
```
Every product in the catalog with a price $> 2,000$ was immediately discarded by the client-side filter upon component mount!

### Root Cause 2: Price Distribution in the Initial 11-Product Seed
Examining the exact prices of all 11 products in `ecommerce.db`:
- Apple MacBook Pro 14 M3: ₹199,900.00 ($> 2000$ $\rightarrow$ **Filtered Out**)
- Dell XPS 15: ₹174,900.00 ($> 2000$ $\rightarrow$ **Filtered Out**)
- Apple iPhone 15 Pro: ₹134,900.00 ($> 2000$ $\rightarrow$ **Filtered Out**)
- Samsung Galaxy S24 Ultra: ₹139,999.00 ($> 2000$ $\rightarrow$ **Filtered Out**)
- Sony WH-1000XM5: ₹28,990.00 ($> 2000$ $\rightarrow$ **Filtered Out**)
- **boAt Airdopes 141 ANC: ₹1,799.00 ($\le 2000$ $\rightarrow$ RETAINED)**
- Nike Air Zoom Pegasus 40: ₹8,995.00 ($> 2000$ $\rightarrow$ **Filtered Out**)
- Adidas Ultraboost Light: ₹14,999.00 ($> 2000$ $\rightarrow$ **Filtered Out**)
- Puma Velocity Nitro 2: ₹4,999.00 ($> 2000$ $\rightarrow$ **Filtered Out**)
- **Nike Dri-FIT Training T-Shirt: ₹1,795.00 ($\le 2000$ $\rightarrow$ RETAINED)**
- PureLiving Barista Pro: ₹12,499.00 ($> 2000$ $\rightarrow$ **Filtered Out**)

**Result:** Exactly and only the Nike Dri-FIT T-shirt and the boAt Airdopes survived the initial render filter!

### Root Cause 3: Category Slug vs ID Parameter Mismatch
In `ProductListPage.tsx`:
```tsx
const params: Record<string, any> = {};
if (selectedCategory) params['category'] = selectedCategory; // sends "laptops-computing"
const res = await api.getProducts(params);
```
In `backend/app/api/v1/products.py`:
```python
def list_products(
    category_id: Optional[int] = Query(None), # Only accepted integer category_id!
    ...
```
Passing `?category=laptops-computing` was ignored by the backend because the endpoint parameter was named `category_id` and typed as integer, leaving filtering to fall back to unconstrained catalog queries.

### Root Cause 4: Overall Database Catalog Scarcity
Even with price filtering relaxed, 11 products across 6 major departments provided less than 2 products per department on average, causing large empty grid spaces and preventing recommendation engines from finding statistical neighbors.

---

## 4. Remediation Strategy

1. **Backend Layer**:
   - Update `list_products` to accept `category` (slug/name) and `brand` (slug/name) in addition to `category_id` and `brand_id`.
   - Support higher limit query parameters (up to 250).
   - Re-index BM25 and TF-IDF models over the expanded catalog.

2. **Data & Seeding Layer**:
   - Seed **200+ distinct, non-duplicate products** spanning all major departments.
   - Expand to 15 sellers, 25 brands, 3 warehouses, 100+ reviews, Q&A, and bundles.
   - Use realistic Indian e-commerce pricing (INR ₹299 to ₹199,900) across budget, mid-range, and premium tiers.

3. **Frontend Layer**:
   - Dynamic price range slider with upper ceiling adapted to catalog (₹200,000 INR).
   - Multi-faceted sidebar with Department, Brand, Rating (4★, 3★, 2★), and In-Stock filters.
   - Interactive pagination (20 items per page) with page navigation and item counter ("Showing 1-20 of 200+").
   - Uniform INR currency formatting (`₹`).
   - Skeletons, empty states, and error handling.
