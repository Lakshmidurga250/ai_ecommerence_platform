"""
Comprehensive Catalog Expansion Seeder.
Expands the product catalog to 216 unique products across 9 categories,
15 multi-vendor marketplace sellers, 25 brands, 3 fulfillment warehouses,
customer reviews with sentiment scoring, product questions/answers, and product bundles.
"""

import os
import sys
import random
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.core.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.models.user import User, Role, UserRole, UserProfile, Address
from app.models.seller import Seller, SellerProfile
from app.models.product import Category, Brand, Product, ProductImage, ProductVariant
from app.models.inventory import Warehouse, Inventory, InventoryMovement
from app.models.cart import Cart, Wishlist
from app.models.review import Review, ReviewSentiment
from app.models.catalog_expansion import (
    ProductBundle, ProductQuestion, ProductAnswer, ReviewHelpfulnessVote, PriceAlert
)
from ai.sentiment.analyzer import SentimentAnalyzer
from app.services.search_service import SearchService

# Import the modular product datasets
from database.seeds.products_data import PRODUCTS_CATALOG
from database.seeds.products_audio_footwear import PRODUCTS_AUDIO_FOOTWEAR
from database.seeds.products_apparel_home import PRODUCTS_APPAREL_HOME
from database.seeds.products_lifestyle import PRODUCTS_LIFESTYLE

# =============================================================================
# 1. CATEGORIES DEFINITION (9 Categories)
# =============================================================================
CATEGORIES_DATA = [
    ("Laptops & Computing", "laptops-computing", "High-performance laptops, ultrabooks, monitors, and computing accessories"),
    ("Smartphones & Tablets", "smartphones-tablets", "Latest flagship smartphones, tablets, chargers, and mobile accessories"),
    ("Audio & Wearables", "audio-wearables", "Noise-cancelling headphones, true wireless earbuds, smartwatches, and speakers"),
    ("Footwear & Running", "footwear-running", "Running shoes, sports sneakers, training, trail, and gym footwear"),
    ("Athletic Apparel", "athletic-apparel", "Gym activewear, moisture-wicking t-shirts, jackets, shorts, and track pants"),
    ("Home & Kitchen", "home-kitchen", "Modern kitchen appliances, cookware, espresso machines, and smart home essentials"),
    ("Gaming & Accessories", "gaming-accessories", "Consoles, mechanical gaming keyboards, high-DPI mice, and gaming headsets"),
    ("Personal Care & Grooming", "personal-care", "Hair dryers, electric shavers, beard trimmers, and sonic electric toothbrushes"),
    ("Books & Stationery", "books-stationery", "Bestselling non-fiction, engineering classics, notebooks, and fine writing pens")
]

# =============================================================================
# 2. BRANDS DEFINITION (25 Brands)
# =============================================================================
BRANDS_DATA = [
    ("Apple", "apple", "https://apple.com"),
    ("Samsung", "samsung", "https://samsung.com"),
    ("Sony", "sony", "https://sony.com"),
    ("Dell", "dell", "https://dell.com"),
    ("Nike", "nike", "https://nike.com"),
    ("Adidas", "adidas", "https://adidas.com"),
    ("Puma", "puma", "https://puma.com"),
    ("boAt", "boat", "https://boat-lifestyle.com"),
    ("HP", "hp", "https://hp.com"),
    ("Lenovo", "lenovo", "https://lenovo.com"),
    ("ASUS", "asus", "https://asus.com"),
    ("Acer", "acer", "https://acer.com"),
    ("OnePlus", "oneplus", "https://oneplus.in"),
    ("Xiaomi", "xiaomi", "https://mi.com/in"),
    ("Realme", "realme", "https://realme.com/in"),
    ("JBL", "jbl", "https://jbl.com"),
    ("Noise", "noise", "https://gonoise.com"),
    ("Philips", "philips", "https://philips.co.in"),
    ("Prestige", "prestige", "https://ttkprestige.com"),
    ("Havells", "havells", "https://havells.com"),
    ("Asics", "asics", "https://asics.com/in"),
    ("Under Armour", "under-armour", "https://underarmour.in"),
    ("Logitech", "logitech", "https://logitech.com"),
    ("SanDisk", "sandisk", "https://westerndigital.com"),
    ("Dyson", "dyson", "https://dyson.in"),
    ("Penguin Random House", "penguin", "https://penguin.com"),
    ("O'Reilly Media", "oreilly", "https://oreilly.com"),
    ("Parker Pen", "parker", "https://parkerpen.com"),
    ("Moleskine", "moleskine", "https://moleskine.com")
]

# =============================================================================
# 3. SELLERS DEFINITION (15 Marketplace Sellers)
# =============================================================================
SELLERS_DATA = [
    {
        "email": "seller1@techvault.com", "username": "techvault", "store": "TechVault Electronics",
        "legal": "TechVault Retail Pvt Ltd", "phone": "+91 9876543210", "rating": 4.9,
        "desc": "Official distributor of high-performance electronics, smartphones, and laptops."
    },
    {
        "email": "seller2@urbanfit.com", "username": "urbanfit", "store": "UrbanFit Sportswear",
        "legal": "UrbanFit Apparel LLP", "phone": "+91 9876543211", "rating": 4.8,
        "desc": "Premium athletic sportswear, running sneakers, and gym accessories."
    },
    {
        "email": "seller3@pureliving.com", "username": "pureliving", "store": "PureLiving Essentials",
        "legal": "PureLiving Home Goods", "phone": "+91 9876543212", "rating": 4.7,
        "desc": "Modern ergonomic home appliances and smart kitchen devices."
    },
    {
        "email": "seller4@digitalhub.in", "username": "digitalhub", "store": "Digital Hub India",
        "legal": "Digital Hub Commerce Pvt Ltd", "phone": "+91 9876543213", "rating": 4.85,
        "desc": "Authorized dealer for enterprise laptops, monitors, storage drives, and peripherals."
    },
    {
        "email": "seller5@primegadgets.in", "username": "primegadgets", "store": "Prime Gadgets Store",
        "legal": "Prime Retail Solutions India", "phone": "+91 9876543214", "rating": 4.75,
        "desc": "Direct retailer of flagship smartphones, power banks, and wireless accessories."
    },
    {
        "email": "seller6@smartbuystore.in", "username": "smartbuystore", "store": "SmartBuy Direct",
        "legal": "SmartBuy Electronics Ltd", "phone": "+91 9876543215", "rating": 4.65,
        "desc": "Budget-friendly tech gadgets, mobile accessories, chargers, and tablets."
    },
    {
        "email": "seller7@fitzone.in", "username": "fitzone", "store": "FitZone Athletics",
        "legal": "FitZone Sports Goods LLP", "phone": "+91 9876543216", "rating": 4.8,
        "desc": "High-performance marathon shoes, trail sneakers, and cross-training apparel."
    },
    {
        "email": "seller8@audioplanet.in", "username": "audioplanet", "store": "Audio Planet Official",
        "legal": "Audio Planet Sound Systems", "phone": "+91 9876543217", "rating": 4.9,
        "desc": "Audiophile studio headphones, high-fidelity wireless speakers, and earbuds."
    },
    {
        "email": "seller9@homeessentials.in", "username": "homeessentials", "store": "Home Essentials Hub",
        "legal": "Home Essentials Retailing Ltd", "phone": "+91 9876543218", "rating": 4.7,
        "desc": "Everyday premium home decor, smart lighting, bedroom comfort, and storage."
    },
    {
        "email": "seller10@kitchenkart.in", "username": "kitchenkart", "store": "KitchenKart MegaStore",
        "legal": "KitchenKart India Pvt Ltd", "phone": "+91 9876543219", "rating": 4.75,
        "desc": "India's favorite destination for mixer grinders, air fryers, and non-stick cookware."
    },
    {
        "email": "seller11@stylemart.in", "username": "stylemart", "store": "StyleMart Fashion",
        "legal": "StyleMart Apparel Ventures", "phone": "+91 9876543220", "rating": 4.6,
        "desc": "Everyday sportswear, moisture-wicking tees, hoodies, and athletic casuals."
    },
    {
        "email": "seller12@apexcomputex.in", "username": "apexcomputex", "store": "Apex Computex Systems",
        "legal": "Apex Computing Technologies", "phone": "+91 9876543221", "rating": 4.9,
        "desc": "Boutique gaming rigs, mechanical keyboards, high-refresh monitors, and workstation SSDs."
    },
    {
        "email": "seller13@mobilegalaxy.in", "username": "mobilegalaxy", "store": "Mobile Galaxy Retail",
        "legal": "Mobile Galaxy Enterprises", "phone": "+91 9876543222", "rating": 4.7,
        "desc": "Wide spectrum of Android & iOS devices, premium cases, and protective gear."
    },
    {
        "email": "seller14@soundwave.in", "username": "soundwave", "store": "SoundWave Pro Audio",
        "legal": "SoundWave Acoustics India", "phone": "+91 9876543223", "rating": 4.8,
        "desc": "Portable Bluetooth party speakers, gaming headsets, and neckband wireless audio."
    },
    {
        "email": "seller15@eliteliving.in", "username": "eliteliving", "store": "Elite Living Goods",
        "legal": "Elite Living Lifestyle Brands", "phone": "+91 9876543224", "rating": 4.85,
        "desc": "Luxury personal grooming gadgets, sonic electric toothbrushes, and designer stationery."
    }
]

# =============================================================================
# 4. WAREHOUSES DEFINITION (3 Regional Centers)
# =============================================================================
WAREHOUSES_DATA = [
    {
        "name": "Central Fulfillment Hub - South", "code": "WH-BLR-01",
        "address": "Plot 18, Electronics City Phase 1", "city": "Bengaluru",
        "state": "Karnataka", "postal_code": "560100", "capacity": 150000
    },
    {
        "name": "Western Distribution Center", "code": "WH-MUM-02",
        "address": "Survey No 45, Bhiwandi Logistics Zone", "city": "Mumbai",
        "state": "Maharashtra", "postal_code": "421302", "capacity": 120000
    },
    {
        "name": "Northern Logistics Hub", "code": "WH-DEL-03",
        "address": "Sector 88, IMT Manesar Industrial Estate", "city": "Gurugram",
        "state": "Haryana", "postal_code": "122051", "capacity": 140000
    }
]

# =============================================================================
# 5. ADDITIONAL CUSTOMERS (For Rich Reviews & Feedback)
# =============================================================================
CUSTOMERS_DATA = [
    {"email": "john.doe@example.com", "username": "johndoe", "first": "John", "last": "Doe"},
    {"email": "priya.sharma@example.com", "username": "priyasharma", "first": "Priya", "last": "Sharma"},
    {"email": "alex.miller@example.com", "username": "alexmiller", "first": "Alex", "last": "Miller"},
    {"email": "anita.roy@example.com", "username": "anitaroy", "first": "Anita", "last": "Roy"},
    {"email": "vikram.aditya@example.com", "username": "vikramaditya", "first": "Vikram", "last": "Aditya"},
    {"email": "sneha.patel@example.com", "username": "snehapatel", "first": "Sneha", "last": "Patel"},
    {"email": "rahul.nair@example.com", "username": "rahulnair", "first": "Rahul", "last": "Nair"},
    {"email": "kavita.menon@example.com", "username": "kavitamenon", "first": "Kavita", "last": "Menon"},
    {"email": "arjun.reddy@example.com", "username": "arjunreddy", "first": "Arjun", "last": "Reddy"},
    {"email": "meera.kapoor@example.com", "username": "meerakapoor", "first": "Meera", "last": "Kapoor"}
]


def seed_expanded_catalog():
    """Main idempotent seeder for catalog expansion."""
    db = SessionLocal()
    try:
        print("[INFO] Starting Comprehensive Product Catalog Expansion...")
        Base.metadata.create_all(bind=engine)

        # 1. Ensure Roles
        roles_data = [
            ("CUSTOMER", "Standard customer shopper"),
            ("SELLER", "Marketplace merchant"),
            ("ADMIN", "Platform administrator")
        ]
        role_map = {}
        for rname, rdesc in roles_data:
            role = db.query(Role).filter(Role.name == rname).first()
            if not role:
                role = Role(name=rname, description=rdesc)
                db.add(role)
                db.flush()
            role_map[rname] = role

        # 2. Categories
        print("[INFO] Seeding Categories (9 categories)...")
        cat_map: Dict[str, Category] = {}
        for name, slug, desc in CATEGORIES_DATA:
            cat = db.query(Category).filter(Category.slug == slug).first()
            if not cat:
                cat = Category(name=name, slug=slug, description=desc)
                db.add(cat)
                db.flush()
            cat_map[slug] = cat

        # 3. Brands
        print("[INFO] Seeding Brands (25 brands)...")
        brand_map: Dict[str, Brand] = {}
        for name, slug, web in BRANDS_DATA:
            brand = db.query(Brand).filter(Brand.slug == slug).first()
            if not brand:
                brand = Brand(name=name, slug=slug, website=web)
                db.add(brand)
                db.flush()
            brand_map[slug] = brand

        # 4. Warehouses
        print("[INFO] Seeding Warehouses (3 fulfillment centers)...")
        warehouse_list: List[Warehouse] = []
        for wdata in WAREHOUSES_DATA:
            wh = db.query(Warehouse).filter(Warehouse.code == wdata["code"]).first()
            if not wh:
                wh = Warehouse(
                    name=wdata["name"],
                    code=wdata["code"],
                    address=wdata["address"],
                    city=wdata["city"],
                    state=wdata["state"],
                    postal_code=wdata["postal_code"],
                    country="India",
                    capacity_units=wdata["capacity"]
                )
                db.add(wh)
                db.flush()
            warehouse_list.append(wh)

        # 5. Sellers
        print("[INFO] Seeding Marketplace Sellers (15 merchants)...")
        seller_map: Dict[str, Seller] = {}
        for sinfo in SELLERS_DATA:
            user = db.query(User).filter(User.email == sinfo["email"]).first()
            if not user:
                user = User(
                    email=sinfo["email"],
                    username=sinfo["username"],
                    hashed_password=hash_password("Seller@123456"),
                    is_active=True,
                    is_verified=True
                )
                db.add(user)
                db.flush()
                db.add(UserRole(user_id=user.id, role_id=role_map["SELLER"].id))
                db.add(UserProfile(user_id=user.id, first_name=sinfo["store"].split()[0], last_name="Merchant", phone=sinfo["phone"]))
                db.add(Cart(user_id=user.id))
                db.add(Wishlist(user_id=user.id))
                db.flush()

            seller = db.query(Seller).filter(Seller.user_id == user.id).first()
            if not seller:
                seller = Seller(
                    user_id=user.id,
                    store_name=sinfo["store"],
                    legal_name=sinfo["legal"],
                    business_email=sinfo["email"],
                    business_phone=sinfo["phone"],
                    tax_identifier="GSTIN29ABCDE1234F1Z5",
                    status="APPROVED",
                    rating=sinfo["rating"],
                    commission_rate=0.10
                )
                db.add(seller)
                db.flush()
                db.add(SellerProfile(seller_id=seller.id, description=sinfo["desc"], support_email=sinfo["email"]))
                db.flush()
            seller_map[sinfo["username"]] = seller

        # 6. Customers
        print("[INFO] Seeding Customers (10 shoppers)...")
        customer_users: List[User] = []
        for cdata in CUSTOMERS_DATA:
            cuser = db.query(User).filter(User.email == cdata["email"]).first()
            if not cuser:
                cuser = User(
                    email=cdata["email"],
                    username=cdata["username"],
                    hashed_password=hash_password("Customer@123456"),
                    is_active=True,
                    is_verified=True
                )
                db.add(cuser)
                db.flush()
                db.add(UserRole(user_id=cuser.id, role_id=role_map["CUSTOMER"].id))
                db.add(UserProfile(user_id=cuser.id, first_name=cdata["first"], last_name=cdata["last"], phone="+91 9800000000"))
                db.add(Cart(user_id=cuser.id))
                db.add(Wishlist(user_id=cuser.id))
                db.flush()
            customer_users.append(cuser)

        # 7. Products Catalog
        all_catalog = (
            PRODUCTS_CATALOG +
            PRODUCTS_AUDIO_FOOTWEAR +
            PRODUCTS_APPAREL_HOME +
            PRODUCTS_LIFESTYLE
        )
        print(f"[INFO] Seeding {len(all_catalog)} Products across catalog...")

        created_count = 0
        updated_count = 0
        product_records: Dict[str, Product] = {}

        for pdata in all_catalog:
            sku = pdata["sku"]
            cat_slug = pdata["category"]
            brand_slug = pdata["brand"]
            seller_uname = pdata["seller"]

            cat_id = cat_map[cat_slug].id
            brand_id = brand_map[brand_slug].id if brand_slug in brand_map else None
            seller_id = seller_map[seller_uname].id

            discount_pct = 0.0
            if pdata.get("compare") and pdata["compare"] > pdata["price"]:
                discount_pct = round(((pdata["compare"] - pdata["price"]) / pdata["compare"]) * 100.0, 1)

            prod = db.query(Product).filter((Product.sku == sku) | (Product.slug == pdata["slug"])).first()
            if not prod:
                base_slug = pdata["slug"]
                target_slug = base_slug
                s_counter = 1
                while db.query(Product).filter(Product.slug == target_slug).first():
                    target_slug = f"{base_slug}-{s_counter}"
                    s_counter += 1

                prod = Product(
                    seller_id=seller_id,
                    category_id=cat_id,
                    brand_id=brand_id,
                    sku=sku,
                    name=pdata["name"],
                    slug=target_slug,
                    description=pdata["desc"],
                    price=pdata["price"],
                    compare_at_price=pdata.get("compare"),
                    discount_percent=discount_pct,
                    stock=pdata["stock"],
                    rating=pdata["rating"],
                    review_count=pdata["reviews"],
                    sales_count=pdata["sales"],
                    is_active=True,
                    is_featured=pdata.get("featured", False),
                    attributes=pdata.get("attr", {})
                )
                db.add(prod)
                db.flush()
                created_count += 1

                # Images
                for idx, img_url in enumerate(pdata.get("images", [])):
                    db.add(ProductImage(
                        product_id=prod.id,
                        image_url=img_url,
                        sort_order=idx,
                        is_primary=(idx == 0)
                    ))

                # Allocate Inventory across the 3 warehouses
                stock_qty = pdata["stock"]
                wh_allocation = [
                    int(stock_qty * 0.5) + 10,
                    int(stock_qty * 0.3) + 5,
                    int(stock_qty * 0.2) + 5
                ]
                for w_idx, wh_obj in enumerate(warehouse_list):
                    qty = wh_allocation[w_idx]
                    db.add(Inventory(
                        warehouse_id=wh_obj.id,
                        product_id=prod.id,
                        quantity=qty,
                        reserved_quantity=max(0, int(qty * 0.1)),
                        reorder_level=15
                    ))
            else:
                prod.name = pdata["name"]
                prod.category_id = cat_id
                prod.brand_id = brand_id
                prod.price = pdata["price"]
                prod.compare_at_price = pdata.get("compare")
                prod.discount_percent = discount_pct
                prod.stock = pdata["stock"]
                prod.rating = pdata["rating"]
                prod.is_active = True
                prod.is_featured = pdata.get("featured", False)
                prod.attributes = pdata.get("attr", {})
                updated_count += 1

            product_records[sku] = prod
            product_records[prod.sku] = prod


        db.commit()
        print(f"[SUCCESS] Catalog populated: {created_count} new products created, {updated_count} existing verified.")

        # 8. Seed Realistic Reviews with Sentiment Analysis
        print("[INFO] Seeding customer reviews with live ML sentiment analysis...")
        review_templates = [
            ("Outstanding build quality and exceeded all my performance expectations!", 5),
            ("Genuinely good purchase. Build is solid and battery life is very reliable.", 4),
            ("Decent product for the price point, but delivery took an extra day.", 3),
            ("Super fast performance and sleek aesthetics. Totally worth the investment!", 5),
            ("Very satisfied with the ergonomics and lightweight design. Recommended.", 5),
            ("Works well out of the box. Clear documentation and nice packaging.", 4),
            ("Excellent product! Premium feel and top-notch materials.", 5)
        ]

        sentiment_engine = SentimentAnalyzer()
        review_count_created = 0

        # Sample 40 diverse products to receive enriched authentic customer reviews
        sample_skus = list(product_records.keys())[:50]
        for sku_sample in sample_skus:
            target_prod = product_records[sku_sample]
            existing_rev = db.query(Review).filter(Review.product_id == target_prod.id).first()
            if not existing_rev:
                # Assign 2 reviews per sampled product from distinct customers
                selected_custs = random.sample(customer_users, 2)
                for cust in selected_custs:
                    comment_text, star_rating = random.choice(review_templates)
                    rev = Review(
                        user_id=cust.id,
                        product_id=target_prod.id,
                        rating=star_rating,
                        title="Verified Customer Experience",
                        comment=comment_text,
                        is_verified_purchase=True,
                        status="APPROVED",
                        helpful_votes=random.randint(1, 15),
                        created_at=datetime.now(timezone.utc) - timedelta(days=random.randint(1, 45))
                    )
                    db.add(rev)
                    db.flush()

                    # Live sentiment scoring
                    sent_res = sentiment_engine.analyze_text(comment_text)
                    db.add(ReviewSentiment(
                        review_id=rev.id,
                        sentiment_label=sent_res["sentiment_label"],
                        polarity_score=sent_res["polarity_score"],
                        subjectivity_score=sent_res["subjectivity_score"],
                        confidence_score=sent_res["confidence_score"],
                        extracted_aspects=sent_res["extracted_aspects"]
                    ))

                    # Helpful votes
                    db.add(ReviewHelpfulnessVote(
                        review_id=rev.id,
                        user_id=random.choice([c.id for c in customer_users if c.id != cust.id]),
                        is_helpful=True
                    ))
                    review_count_created += 1

        db.commit()
        print(f"[SUCCESS] {review_count_created} enriched customer reviews & sentiments created.")

        # 9. Seed Product Questions & Answers
        print("[INFO] Seeding Product Q&A across top categories...")
        qna_seeds = [
            ("LAP-APL-MBP-14-M3", "Does this MacBook model support multi-monitor external displays?", "Yes, the M3 Pro chip natively supports up to two high-resolution 6K external displays at 60Hz via Thunderbolt.", True),
            ("PHO-SAM-S24U-512-GRY", "Does this unit include the S-Pen inside the phone body?", "Yes, the S-Pen stylus is integrated directly into the bottom chassis of the Galaxy S24 Ultra.", True),
            ("AUD-SNY-WH1000XM5-BLK", "Can these headphones be used while charging via USB-C?", "You get 3 hours of playback from a quick 3-minute charge, but audio streaming is paused during direct plug-in charging.", True),
            ("SHO-NIK-PEGASUS-40", "Are these shoes true to size for wide feet?", "The Pegasus 40 has an accommodating midfoot fit band, but runners with very wide feet often prefer a half size larger.", True),
            ("HOM-PRL-ESPRESSO-15", "What is the recommended coffee grind size for this machine?", "Fine espresso grind is ideal for the 15-bar pressurized portafilter basket to achieve optimum crema extraction.", True),
            ("GAM-SNY-PS5-SLIM-DISC", "Does the console come with the Ultra HD Blu-ray disc drive attached?", "Yes, this is the Disc Edition model which includes the detachable Ultra HD Blu-ray drive pre-installed.", True),
            ("GRO-DYS-SUPERSONIC-DRYER", "Does it include the Flyaway magnetic smoothing attachment?", "Yes, the box includes all 5 original magnetic attachments including the Flyaway smoother and Diffuser.", True)
        ]

        qna_created = 0
        for p_sku, q_text, a_text, seller_reply in qna_seeds:
            if p_sku in product_records:
                p_obj = product_records[p_sku]
                existing_q = db.query(ProductQuestion).filter(
                    ProductQuestion.product_id == p_obj.id,
                    ProductQuestion.question_text == q_text
                ).first()
                if not existing_q:
                    q = ProductQuestion(
                        product_id=p_obj.id,
                        user_id=customer_users[0].id,
                        question_text=q_text,
                        is_answered=True,
                        is_approved=True
                    )
                    db.add(q)
                    db.flush()

                    seller_user = db.query(User).filter(User.id == p_obj.seller.user_id).first()
                    ans_user_id = seller_user.id if seller_user else customer_users[1].id
                    db.add(ProductAnswer(
                        question_id=q.id,
                        user_id=ans_user_id,
                        answer_text=a_text,
                        is_seller_reply=seller_reply,
                        is_approved=True
                    ))
                    qna_created += 1

        db.commit()
        print(f"[SUCCESS] {qna_created} Q&A threads seeded.")

        # 10. Seed Product Bundles
        print("[INFO] Seeding Product Bundles...")
        bundles_seeds = [
            ("Productivity Pro Workstation", "LAP-APL-MBP-14-M3", "ACC-LOGI-MX-MASTER-3S", 204900.0),
            ("Ultimate Flagship Mobile Kit", "PHO-SAM-S24U-512-GRY", "ACC-SAM-45W-CHARGER", 140999.0),
            ("Marathon Runner Performance Pack", "SHO-NIK-PEGASUS-40", "APP-NIK-DRI-FIT-TEE-BLK", 9999.0),
            ("Home Barista Coffee Morning Bundle", "HOM-PRL-ESPRESSO-15", "HOM-MILTON-THERMOSTEEL-1L", 12999.0),
            ("PlayStation Pro Gaming Setup", "GAM-SNY-PS5-SLIM-DISC", "GAM-SNY-DUALSENSE-WHT", 58990.0)
        ]

        bundles_created = 0
        for b_name, main_sku, add_sku, b_price in bundles_seeds:
            if main_sku in product_records and add_sku in product_records:
                m_prod = product_records[main_sku]
                a_prod = product_records[add_sku]
                existing_b = db.query(ProductBundle).filter(
                    ProductBundle.primary_product_id == m_prod.id,
                    ProductBundle.bundle_product_id == a_prod.id
                ).first()
                if not existing_b:
                    db.add(ProductBundle(
                        bundle_name=b_name,
                        primary_product_id=m_prod.id,
                        bundle_product_id=a_prod.id,
                        discount_percent=10.0,
                        is_active=True
                    ))
                    bundles_created += 1

        db.commit()
        print(f"[SUCCESS] {bundles_created} Product Bundles created.")


        # 11. Re-synchronize Search Index
        print("[INFO] Re-synchronizing BM25 Search Engine Index across the entire catalog...")
        SearchService.sync_index(db)
        print("[SUCCESS] Search index fully synchronized with active products!")

        total_prods = db.query(Product).count()
        print(f"[COMPLETED] Comprehensive Catalog Expansion Complete! Total active products in DB: {total_prods}")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Catalog expansion failed: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_expanded_catalog()
