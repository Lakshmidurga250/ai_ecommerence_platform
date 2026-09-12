"""
Cart and Wishlist Management Service.
Enforces backend price recalculation and available stock validation.
"""

from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException, InsufficientStockException
from app.models.cart import Cart, CartItem, Wishlist, WishlistItem, Coupon, CouponUsage
from app.models.product import Product, ProductVariant
from app.schemas.cart import CartRead, CartItemRead


class CartService:
    @staticmethod
    def get_or_create_cart(db: Session, user_id: int) -> Cart:
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        return cart

    @staticmethod
    def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int = 1, variant_id: Optional[int] = None) -> Cart:
        cart = CartService.get_or_create_cart(db, user_id)
        product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
        if not product:
            raise NotFoundException("Product", str(product_id))

        price = product.price
        available_stock = product.stock

        if variant_id:
            variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id, ProductVariant.product_id == product_id).first()
            if not variant:
                raise NotFoundException("ProductVariant", str(variant_id))
            price = variant.price
            available_stock = variant.stock

        # Check existing item in cart
        existing_item = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id,
            CartItem.variant_id == variant_id
        ).first()

        new_total_qty = (existing_item.quantity if existing_item else 0) + quantity
        if new_total_qty > available_stock:
            raise InsufficientStockException(product.name, new_total_qty, available_stock)

        if existing_item:
            existing_item.quantity = new_total_qty
            existing_item.price_at_addition = price
        else:
            item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                variant_id=variant_id,
                quantity=quantity,
                price_at_addition=price
            )
            db.add(item)

        db.commit()
        db.refresh(cart)
        return cart

    @staticmethod
    def update_cart_item(db: Session, user_id: int, item_id: int, quantity: int) -> Cart:
        cart = CartService.get_or_create_cart(db, user_id)
        item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
        if not item:
            raise NotFoundException("CartItem", str(item_id))

        if quantity <= 0:
            db.delete(item)
        else:
            product = item.product
            if quantity > product.stock:
                raise InsufficientStockException(product.name, quantity, product.stock)
            item.quantity = quantity

        db.commit()
        db.refresh(cart)
        return cart

    @staticmethod
    def remove_cart_item(db: Session, user_id: int, item_id: int) -> Cart:
        cart = CartService.get_or_create_cart(db, user_id)
        item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
        if item:
            db.delete(item)
            db.commit()
            db.refresh(cart)
        return cart

    @staticmethod
    def clear_cart(db: Session, user_id: int):
        cart = CartService.get_or_create_cart(db, user_id)
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()

    @staticmethod
    def calculate_cart(db: Session, user_id: int, coupon_code: Optional[str] = None) -> Dict[str, Any]:
        """Recalculates cart subtotal, tax, shipping, and discount using verified server data."""
        cart = CartService.get_or_create_cart(db, user_id)
        items = cart.items

        subtotal = 0.0
        tax_amount = 0.0

        for item in items:
            product = item.product
            unit_price = item.variant.price if item.variant else product.price
            item_subtotal = unit_price * item.quantity
            subtotal += item_subtotal
            tax_amount += item_subtotal * (product.tax_rate or 0.18)

        # Shipping rules: Free shipping over ₹1,000, else ₹60
        shipping_fee = 0.0 if (subtotal >= 1000.0 or subtotal == 0.0) else 60.0
        discount_amount = 0.0

        # Validate Coupon
        if coupon_code and subtotal > 0:
            code_clean = coupon_code.strip().upper()
            coupon = db.query(Coupon).filter(Coupon.code == code_clean, Coupon.is_active == True).first()
            if coupon and subtotal >= coupon.min_order_amount:
                if coupon.discount_type == "PERCENTAGE":
                    discount = subtotal * (coupon.discount_value / 100.0)
                    if coupon.max_discount_amount:
                        discount = min(discount, coupon.max_discount_amount)
                    discount_amount = round(discount, 2)
                else:  # FIXED
                    discount_amount = min(subtotal, coupon.discount_value)

        total_amount = max(0.0, round(subtotal + tax_amount + shipping_fee - discount_amount, 2))

        return {
            "id": cart.id,
            "user_id": user_id,
            "items": items,
            "subtotal": round(subtotal, 2),
            "tax_amount": round(tax_amount, 2),
            "discount_amount": round(discount_amount, 2),
            "shipping_fee": round(shipping_fee, 2),
            "total_amount": total_amount,
            "coupon_code": coupon_code
        }

    # Wishlist Methods
    @staticmethod
    def get_or_create_wishlist(db: Session, user_id: int) -> Wishlist:
        wishlist = db.query(Wishlist).filter(Wishlist.user_id == user_id).first()
        if not wishlist:
            wishlist = Wishlist(user_id=user_id)
            db.add(wishlist)
            db.commit()
            db.refresh(wishlist)
        return wishlist

    @staticmethod
    def add_to_wishlist(db: Session, user_id: int, product_id: int) -> Wishlist:
        wishlist = CartService.get_or_create_wishlist(db, user_id)
        existing = db.query(WishlistItem).filter(WishlistItem.wishlist_id == wishlist.id, WishlistItem.product_id == product_id).first()
        if not existing:
            item = WishlistItem(wishlist_id=wishlist.id, product_id=product_id)
            db.add(item)
            db.commit()
            db.refresh(wishlist)
        return wishlist

    @staticmethod
    def remove_from_wishlist(db: Session, user_id: int, product_id: int) -> Wishlist:
        wishlist = CartService.get_or_create_wishlist(db, user_id)
        item = db.query(WishlistItem).filter(WishlistItem.wishlist_id == wishlist.id, WishlistItem.product_id == product_id).first()
        if item:
            db.delete(item)
            db.commit()
            db.refresh(wishlist)
        return wishlist

    @staticmethod
    def move_to_cart(db: Session, user_id: int, product_id: int) -> Cart:
        CartService.remove_from_wishlist(db, user_id, product_id)
        return CartService.add_to_cart(db, user_id, product_id, quantity=1)
