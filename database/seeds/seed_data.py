"""
Realistic Seed Dataset Generator.
Populates initial Admin, Sellers, Customers, Categories, Brands, Products,
Warehouses, Inventory, Orders, Reviews, Coupons, and AI Model Registry entries.
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Add paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "backend"))

from app.core.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.models.user import User, Role, UserRole, UserProfile, Address
from app.models.seller import Seller, SellerProfile
from app.models.product import Category, Brand, Product, ProductImage, ProductVariant
from app.models.inventory import Warehouse, Inventory, InventoryMovement
from app.models.cart import Cart, Wishlist, Coupon
from app.models.order import Order, OrderItem, Payment, Shipment, ShipmentEvent
from app.models.review import Review, ReviewSentiment
from app.models.analytics import ModelRegistryEntry
from ai.sentiment.analyzer import SentimentAnalyzer
from ai.model_registry.registry import ModelRegistryService


def seed_database():
    db = SessionLocal()
    try:
        print("[INFO] Seeding database...")
        Base.metadata.create_all(bind=engine)

        # 1. Roles
        roles_data = [
            ("CUSTOMER", "Standard customer shopper"),
            ("SELLER", "Marketplace merchant with catalog & inventory privileges"),
            ("ADMIN", "Platform administrator with universal privileges")
        ]
        role_map = {}
        for rname, rdesc in roles_data:
            role = db.query(Role).filter(Role.name == rname).first()
            if not role:
                role = Role(name=rname, description=rdesc)
                db.add(role)
                db.flush()
            role_map[rname] = role

        # 2. Admin User
        admin_user = db.query(User).filter(User.email == "admin@platform.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@platform.com",
                username="admin",
                hashed_password=hash_password("Admin@123456"),
                is_active=True,
                is_verified=True
            )
            db.add(admin_user)
            db.flush()
            db.add(UserRole(user_id=admin_user.id, role_id=role_map["ADMIN"].id))
            db.add(UserProfile(user_id=admin_user.id, first_name="System", last_name="Administrator"))
            db.add(Cart(user_id=admin_user.id))
            db.add(Wishlist(user_id=admin_user.id))

        # 3. Sellers
        sellers_info = [
            {
                "email": "seller1@techvault.com", "username": "techvault", "store": "TechVault Electronics",
                "legal": "TechVault Retail Pvt Ltd", "phone": "+91 9876543210",
                "desc": "Official distributor of high-performance electronics, smartphones, and laptops."
            },
            {
                "email": "seller2@urbanfit.com", "username": "urbanfit", "store": "UrbanFit Sportswear",
                "legal": "UrbanFit Apparel LLP", "phone": "+91 9876543211",
                "desc": "Premium athletic sportswear, running sneakers, and gym accessories."
            },
            {
                "email": "seller3@pureliving.com", "username": "pureliving", "store": "PureLiving Essentials",
                "legal": "PureLiving Home Goods", "phone": "+91 9876543212",
                "desc": "Modern ergonomic home appliances and smart kitchen devices."
            }
        ]
        seller_map = {}
        for s in sellers_info:
            user = db.query(User).filter(User.email == s["email"]).first()
            if not user:
                user = User(
                    email=s["email"],
                    username=s["username"],
                    hashed_password=hash_password("Seller@123456"),
                    is_active=True,
                    is_verified=True
                )
                db.add(user)
                db.flush()
                db.add(UserRole(user_id=user.id, role_id=role_map["SELLER"].id))
                db.add(UserProfile(user_id=user.id, first_name=s["username"].capitalize(), last_name="Seller", phone=s["phone"]))
                db.add(Cart(user_id=user.id))
                db.add(Wishlist(user_id=user.id))

                seller = Seller(
                    user_id=user.id,
                    store_name=s["store"],
                    legal_name=s["legal"],
                    business_email=s["email"],
                    business_phone=s["phone"],
                    tax_identifier="GSTIN29ABCDE1234F1Z5",
                    status="APPROVED",
                    rating=4.9,
                    commission_rate=0.10
                )
                db.add(seller)
                db.flush()
                db.add(SellerProfile(seller_id=seller.id, description=s["desc"], support_email=s["email"]))
                seller_map[s["username"]] = seller
            else:
                seller_map[s["username"]] = user.seller_profile

        # 4. Customers
        customers_info = [
            {"email": "john.doe@example.com", "username": "johndoe", "first": "John", "last": "Doe", "phone": "+91 9123456780"},
            {"email": "priya.sharma@example.com", "username": "priyasharma", "first": "Priya", "last": "Sharma", "phone": "+91 9123456781"},
            {"email": "alex.miller@example.com", "username": "alexmiller", "first": "Alex", "last": "Miller", "phone": "+91 9123456782"},
            {"email": "anita.roy@example.com", "username": "anitaroy", "first": "Anita", "last": "Roy", "phone": "+91 9123456783"}
        ]
        customer_map = {}
        for c in customers_info:
            user = db.query(User).filter(User.email == c["email"]).first()
            if not user:
                user = User(
                    email=c["email"],
                    username=c["username"],
                    hashed_password=hash_password("Customer@123456"),
                    is_active=True,
                    is_verified=True
                )
                db.add(user)
                db.flush()
                db.add(UserRole(user_id=user.id, role_id=role_map["CUSTOMER"].id))
                db.add(UserProfile(user_id=user.id, first_name=c["first"], last_name=c["last"], phone=c["phone"]))
                db.add(Cart(user_id=user.id))
                db.add(Wishlist(user_id=user.id))

                addr = Address(
                    user_id=user.id,
                    title="Home",
                    recipient_name=f"{c['first']} {c['last']}",
                    street="42 Brigade Road, Indiranagar",
                    city="Bengaluru",
                    state="Karnataka",
                    postal_code="560038",
                    country="India",
                    phone=c["phone"],
                    is_default=True
                )
                db.add(addr)
                customer_map[c["username"]] = user
            else:
                customer_map[c["username"]] = user

        # 5. Warehouses
        warehouse = db.query(Warehouse).first()
        if not warehouse:
            warehouse = Warehouse(
                name="Central Fulfillment Hub - South",
                code="WH-BLR-01",
                address="Plot 18, Electronics City Phase 1",
                city="Bengaluru",
                state="Karnataka",
                postal_code="560100",
                country="India",
                capacity_units=150000
            )
            db.add(warehouse)
            db.flush()

        # 6. Categories
        categories_data = [
            ("Laptops & Computing", "laptops-computing", "High-performance laptops, ultrabooks, and desktop accessories"),
            ("Smartphones & Tablets", "smartphones-tablets", "Latest flagship smartphones and portable tablets"),
            ("Audio & Wearables", "audio-wearables", "Noise-cancelling headphones, wireless earbuds, and smartwatches"),
            ("Footwear & Running", "footwear-running", "Running shoes, sports sneakers, training and gym footwear"),
            ("Athletic Apparel", "athletic-apparel", "Gym wear, moisture-wicking t-shirts, jackets, and track pants"),
            ("Home & Kitchen", "home-kitchen", "Ergonomic coffee machines, air fryers, and smart appliances")
        ]
        cat_map = {}
        for name, slug, desc in categories_data:
            cat = db.query(Category).filter(Category.slug == slug).first()
            if not cat:
                cat = Category(name=name, slug=slug, description=desc)
                db.add(cat)
                db.flush()
            cat_map[slug] = cat

        # 7. Brands
        brands_data = [
            ("Apple", "apple", "https://apple.com"),
            ("Samsung", "samsung", "https://samsung.com"),
            ("Sony", "sony", "https://sony.com"),
            ("Dell", "dell", "https://dell.com"),
            ("Nike", "nike", "https://nike.com"),
            ("Adidas", "adidas", "https://adidas.com"),
            ("Puma", "puma", "https://puma.com"),
            ("boAt", "boat", "https://boat-lifestyle.com")
        ]
        brand_map = {}
        for name, slug, web in brands_data:
            brand = db.query(Brand).filter(Brand.slug == slug).first()
            if not brand:
                brand = Brand(name=name, slug=slug, website=web)
                db.add(brand)
                db.flush()
            brand_map[slug] = brand

        # 8. Products
        products_data = [
            # Laptops
            {
                "seller": seller_map["techvault"].id, "category": cat_map["laptops-computing"].id, "brand": brand_map["apple"].id,
                "sku": "APL-MBP-14-M3", "name": "Apple MacBook Pro 14 M3 Pro (18GB, 512GB SSD, Space Black)",
                "slug": "apple-macbook-pro-14-m3-space-black",
                "desc": "Pro-level performance engineered with the M3 Pro chip. Up to 18 hours battery life, Liquid Retina XDR display, and unified memory for heavy development and creative rendering.",
                "price": 199900.0, "compare": 219900.0, "stock": 45, "rating": 4.9, "reviews": 38, "sales": 110, "featured": True,
                "attr": {"color": "black", "screen_size": "14.2 inch", "ram": "18GB", "storage": "512GB", "processor": "Apple M3 Pro"},
                "images": ["https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&auto=format&fit=crop"]
            },
            {
                "seller": seller_map["techvault"].id, "category": cat_map["laptops-computing"].id, "brand": brand_map["dell"].id,
                "sku": "DEL-XPS-15-OLED", "name": "Dell XPS 15 9530 Core i7 (32GB, 1TB SSD, RTX 4060, Platinum Silver)",
                "slug": "dell-xps-15-oled-core-i7",
                "desc": "Stunning 3.5K OLED InfinityEdge touch display with Intel Core i7 13th Gen and NVIDIA GeForce RTX 4060 graphics.",
                "price": 174900.0, "compare": 189900.0, "stock": 30, "rating": 4.7, "reviews": 24, "sales": 65, "featured": True,
                "attr": {"color": "silver", "screen_size": "15.6 inch", "ram": "32GB", "storage": "1TB", "gpu": "RTX 4060"},
                "images": ["https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800&auto=format&fit=crop"]
            },
            # Smartphones
            {
                "seller": seller_map["techvault"].id, "category": cat_map["smartphones-tablets"].id, "brand": brand_map["apple"].id,
                "sku": "APL-IP15P-256-BLK", "name": "Apple iPhone 15 Pro (256GB, Black Titanium)",
                "slug": "apple-iphone-15-pro-black-titanium",
                "desc": "Forged in aerospace-grade titanium with the ground-breaking A17 Pro chip, customizable Action button, and versatile 48MP triple camera system.",
                "price": 134900.0, "compare": 144900.0, "stock": 60, "rating": 4.8, "reviews": 52, "sales": 230, "featured": True,
                "attr": {"color": "black", "storage": "256GB", "camera": "48MP", "network": "5G"},
                "images": ["https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800&auto=format&fit=crop"]
            },
            {
                "seller": seller_map["techvault"].id, "category": cat_map["smartphones-tablets"].id, "brand": brand_map["samsung"].id,
                "sku": "SAM-S24U-512-GRY", "name": "Samsung Galaxy S24 Ultra 5G (12GB RAM, 512GB, Titanium Gray)",
                "slug": "samsung-galaxy-s24-ultra-titanium-gray",
                "desc": "Galaxy AI powered flagship with Snapdragon 8 Gen 3, integrated S Pen, 200MP camera with Quad Telephoto, and titanium frame.",
                "price": 139999.0, "compare": 149999.0, "stock": 40, "rating": 4.8, "reviews": 44, "sales": 185, "featured": True,
                "attr": {"color": "gray", "storage": "512GB", "ram": "12GB", "camera": "200MP"},
                "images": ["https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800&auto=format&fit=crop"]
            },
            # Audio
            {
                "seller": seller_map["techvault"].id, "category": cat_map["audio-wearables"].id, "brand": brand_map["sony"].id,
                "sku": "SNY-WH1000XM5-BLK", "name": "Sony WH-1000XM5 Wireless Industry Leading Noise Canceling Headphones (Black)",
                "slug": "sony-wh-1000xm5-noise-canceling-black",
                "desc": "Industry-leading noise cancellation with two processors and 8 microphones. High-Resolution Audio with 30-hour battery life and ultra-comfortable lightweight design.",
                "price": 28990.0, "compare": 34990.0, "stock": 85, "rating": 4.9, "reviews": 68, "sales": 320, "featured": True,
                "attr": {"color": "black", "type": "over-ear", "battery_life": "30 hours", "connectivity": "Bluetooth 5.2"},
                "images": ["https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop"]
            },
            {
                "seller": seller_map["techvault"].id, "category": cat_map["audio-wearables"].id, "brand": brand_map["boat"].id,
                "sku": "BOT-AIRDOPES-141", "name": "boAt Airdopes 141 ANC True Wireless Earbuds (Gunmetal Black)",
                "slug": "boat-airdopes-141-anc-black",
                "desc": "Up to 42 hours total playback, active noise cancellation up to 32dB, Beast Mode for 50ms low latency gaming, and ENx quad mics.",
                "price": 1799.0, "compare": 4490.0, "stock": 250, "rating": 4.4, "reviews": 115, "sales": 840, "featured": False,
                "attr": {"color": "black", "type": "in-ear", "playback": "42h", "anc": "32dB"},
                "images": ["https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&auto=format&fit=crop"]
            },
            # Footwear & Running Shoes
            {
                "seller": seller_map["urbanfit"].id, "category": cat_map["footwear-running"].id, "brand": brand_map["nike"].id,
                "sku": "NIK-PEGASUS-40-BLK", "name": "Nike Air Zoom Pegasus 40 Men's Running Shoes (Black / White)",
                "slug": "nike-air-zoom-pegasus-40-black",
                "desc": "A springy ride for every run. React foam technology coupled with two Zoom Air units delivers energized responsiveness and breathability.",
                "price": 8995.0, "compare": 10495.0, "stock": 70, "rating": 4.8, "reviews": 48, "sales": 290, "featured": True,
                "attr": {"color": "black", "size": "UK 9", "type": "running shoes", "surface": "road"},
                "images": ["https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop"]
            },
            {
                "seller": seller_map["urbanfit"].id, "category": cat_map["footwear-running"].id, "brand": brand_map["adidas"].id,
                "sku": "ADI-ULTRABOOST-LIGHT", "name": "Adidas Ultraboost Light Running Shoes (Core Black)",
                "slug": "adidas-ultraboost-light-core-black",
                "desc": "Experience epic energy return with the lightest Boost ever made. Continental rubber outsole provides extraordinary traction in wet and dry conditions.",
                "price": 14999.0, "compare": 18999.0, "stock": 50, "rating": 4.7, "reviews": 36, "sales": 175, "featured": True,
                "attr": {"color": "black", "size": "UK 8", "type": "running shoes", "cushioning": "maximum"},
                "images": ["https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800&auto=format&fit=crop"]
            },
            {
                "seller": seller_map["urbanfit"].id, "category": cat_map["footwear-running"].id, "brand": brand_map["puma"].id,
                "sku": "PUM-VELOCITY-NITRO-2", "name": "Puma Velocity Nitro 2 Lightweight Running Shoes (Blue / Silver)",
                "slug": "puma-velocity-nitro-2-blue",
                "desc": "An all-in-one neutral running shoe for any distance. Nitro foam cushioning delivers superior responsiveness in an exceptionally lightweight package.",
                "price": 4999.0, "compare": 7999.0, "stock": 80, "rating": 4.6, "reviews": 29, "sales": 140, "featured": False,
                "attr": {"color": "blue", "size": "UK 9", "type": "running shoes", "weight": "257g"},
                "images": ["https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=800&auto=format&fit=crop"]
            },
            # Apparel
            {
                "seller": seller_map["urbanfit"].id, "category": cat_map["athletic-apparel"].id, "brand": brand_map["nike"].id,
                "sku": "NIK-DRI-FIT-TEE-BLK", "name": "Nike Dri-FIT Men's Moisture-Wicking Training T-Shirt (Black)",
                "slug": "nike-dri-fit-training-tshirt-black",
                "desc": "Soft jersey fabric with sweat-wicking Dri-FIT technology helps keep you dry, comfortable, and focused through high-intensity workout sets.",
                "price": 1795.0, "compare": 2295.0, "stock": 140, "rating": 4.7, "reviews": 42, "sales": 390, "featured": False,
                "attr": {"color": "black", "size": "L", "material": "polyester", "fit": "standard"},
                "images": ["https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop"]
            },
            # Home & Kitchen
            {
                "seller": seller_map["pureliving"].id, "category": cat_map["home-kitchen"].id, "brand": None,
                "sku": "PRL-ESPRESSO-PRO-15", "name": "PureLiving Barista Pro 15-Bar Stainless Steel Espresso Machine",
                "slug": "pureliving-barista-pro-espresso-machine",
                "desc": "Café-quality espresso at home with thermo-block rapid heating, precision commercial steam wand for silky microfoam, and 15-bar Italian pump.",
                "price": 12499.0, "compare": 16999.0, "stock": 35, "rating": 4.8, "reviews": 27, "sales": 95, "featured": True,
                "attr": {"color": "silver", "pressure": "15 bar", "capacity": "1.8L", "material": "stainless steel"},
                "images": ["https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&auto=format&fit=crop"]
            }
        ]

        created_products = []
        for pdata in products_data:
            prod = db.query(Product).filter(Product.sku == pdata["sku"]).first()
            if not prod:
                prod = Product(
                    seller_id=pdata["seller"],
                    category_id=pdata["category"],
                    brand_id=pdata["brand"],
                    sku=pdata["sku"],
                    name=pdata["name"],
                    slug=pdata["slug"],
                    description=pdata["desc"],
                    price=pdata["price"],
                    compare_at_price=pdata["compare"],
                    stock=pdata["stock"],
                    rating=pdata["rating"],
                    review_count=pdata["reviews"],
                    sales_count=pdata["sales"],
                    is_active=True,
                    is_featured=pdata["featured"],
                    attributes=pdata["attr"]
                )
                db.add(prod)
                db.flush()

                for idx, img_url in enumerate(pdata["images"]):
                    db.add(ProductImage(product_id=prod.id, image_url=img_url, sort_order=idx, is_primary=(idx == 0)))

                # Inventory linkage
                inv = Inventory(
                    warehouse_id=warehouse.id,
                    product_id=prod.id,
                    quantity=pdata["stock"] + 15,
                    reserved_quantity=15,
                    reorder_level=20
                )
                db.add(inv)
                db.flush()
                db.add(InventoryMovement(
                    inventory_id=inv.id,
                    movement_type="INBOUND",
                    quantity=pdata["stock"] + 15,
                    reference_type="SEED_IMPORT",
                    reference_id=prod.sku,
                    notes="Initial warehouse inventory ingestion"
                ))

            created_products.append(prod)

        # 9. Coupons
        coupons_data = [
            ("WELCOME10", "PERCENTAGE", 10.0, 500.0, 500.0, 500, 1),
            ("SUPER500", "FIXED", 500.0, 2500.0, None, 200, 1),
            ("FESTIVE20", "PERCENTAGE", 20.0, 3000.0, 1500.0, 100, 1)
        ]
        for code, dtype, val, min_o, max_d, limit, per_u in coupons_data:
            coup = db.query(Coupon).filter(Coupon.code == code).first()
            if not coup:
                coup = Coupon(
                    code=code,
                    discount_type=dtype,
                    discount_value=val,
                    min_order_amount=min_o,
                    max_discount_amount=max_d,
                    usage_limit=limit,
                    per_user_limit=per_u,
                    is_active=True
                )
                db.add(coup)

        # 10. Reviews & Sentiments
        sample_reviews = [
            ("johndoe", "APL-MBP-14-M3", 5, "Unbelievable battery life and dev speed", "This MacBook Pro is an absolute powerhouse. The M3 Pro chip compiles large Rust and Python projects in seconds, and the battery easily lasts two full working days. Exceptional build quality!"),
            ("priyasharma", "NIK-PEGASUS-40-BLK", 5, "Best running shoes I have owned", "Extremely comfortable with great arch support. The Zoom Air cushioning makes morning 10k runs feel effortless. High quality breathable mesh."),
            ("alexmiller", "SNY-WH1000XM5-BLK", 4, "Amazing noise cancelling, slightly delicate headband", "The noise cancellation is the best in the market. Blocks airplane engine drone completely. Soundstage is rich and clear. Only minor gripe is the headband feels a bit delicate."),
            ("anitaroy", "BOT-AIRDOPES-141", 3, "Decent sound for the budget price", "Sound quality is acceptable and bass is punchy. Battery backup is good. But microphone in noisy traffic can struggle.")
        ]
        for u_name, sku, rating, title, comment in sample_reviews:
            user = customer_map.get(u_name)
            prod = db.query(Product).filter(Product.sku == sku).first()
            if user and prod:
                existing_rev = db.query(Review).filter(Review.user_id == user.id, Review.product_id == prod.id).first()
                if not existing_rev:
                    rev = Review(
                        product_id=prod.id,
                        user_id=user.id,
                        rating=rating,
                        title=title,
                        comment=comment,
                        is_verified_purchase=True,
                        status="APPROVED",
                        helpful_votes=8
                    )
                    db.add(rev)
                    db.flush()

                    sent_res = SentimentAnalyzer.analyze_text(f"{title} {comment}")
                    db.add(ReviewSentiment(
                        review_id=rev.id,
                        sentiment_label=sent_res["sentiment_label"],
                        polarity_score=sent_res["polarity_score"],
                        subjectivity_score=sent_res["subjectivity_score"],
                        confidence_score=sent_res["confidence_score"],
                        extracted_aspects=sent_res["extracted_aspects"]
                    ))

        # 11. Seed Model Registry entries with genuine baseline metrics
        model_registrations = [
            {
                "name": "recommendation-hybrid-engine", "version": "v1.0.0", "algorithm": "WeightedEnsemble_CF_Content_Popularity",
                "dataset": "marketplace-events-v1", "hp": {"cf_weight": 0.45, "content_weight": 0.35, "pop_weight": 0.20},
                "metrics": {"precision_at_k": 0.38, "recall_at_k": 0.54, "ndcg_at_k": 0.62}
            },
            {
                "name": "demand-forecaster", "version": "v1.0.0", "algorithm": "RandomForestRegressor_LagTimeSeries",
                "dataset": "historical-daily-sales-v1", "hp": {"n_estimators": 100, "max_depth": 6, "lag_window": 7},
                "metrics": {"mae": 1.45, "rmse": 2.18, "mape": 12.4}
            },
            {
                "name": "fraud-anomaly-detector", "version": "v1.0.0", "algorithm": "IsolationForest_RuleAttribution",
                "dataset": "transactions-anomaly-v1", "hp": {"contamination": 0.05, "n_estimators": 100},
                "metrics": {"roc_auc": 0.94, "precision": 0.88, "recall": 0.91}
            },
            {
                "name": "customer-rfm-segmenter", "version": "v1.0.0", "algorithm": "StandardScaler_KMeans_Clustering",
                "dataset": "customer-rfm-v1", "hp": {"n_clusters": 4, "init": "k-means++"},
                "metrics": {"silhouette_score": 0.68, "inertia": 214.5}
            },
            {
                "name": "customer-churn-classifier", "version": "v1.0.0", "algorithm": "Calibrated_Logistic_Sigmoid",
                "dataset": "user-retention-signals-v1", "hp": {"decay_rate": 0.035, "inactivity_threshold_days": 45},
                "metrics": {"accuracy": 0.89, "f1_score": 0.86}
            },
            {
                "name": "review-sentiment-analyzer", "version": "v1.0.0", "algorithm": "Mathematical_Lexicon_AspectExtraction",
                "dataset": "customer-feedback-corpus-v1", "hp": {"neutral_threshold": 0.15, "intensifier_boost": 1.4},
                "metrics": {"accuracy": 0.92, "macro_f1": 0.90}
            }
        ]
        for m in model_registrations:
            ModelRegistryService.register_model(
                db=db,
                model_name=m["name"],
                version=m["version"],
                algorithm=m["algorithm"],
                dataset_version=m["dataset"],
                hyperparameters=m["hp"],
                metrics=m["metrics"],
                status="PRODUCTION"
            )

        db.commit()
        print("[SUCCESS] Database seeding successfully completed with verified entities!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
