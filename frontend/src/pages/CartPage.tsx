import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Trash2, ArrowRight, ShoppingBag, Tag, ShieldCheck, Check } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';

export const CartPage: React.FC = () => {
  const { cart, updateQuantity, removeItem, applyCoupon, loading } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [couponInput, setCouponInput] = useState('');
  const [couponMsg, setCouponMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleApplyCoupon = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!couponInput.trim()) return;
    try {
      await applyCoupon(couponInput.trim().toUpperCase());
      setCouponMsg({ type: 'success', text: `Coupon ${couponInput.toUpperCase()} applied successfully!` });
    } catch (err: any) {
      setCouponMsg({ type: 'error', text: err.message || 'Invalid coupon code' });
    }
  };

  const handleProceedToCheckout = () => {
    if (!user) {
      navigate('/login?redirect=/checkout');
    } else {
      navigate('/checkout');
    }
  };

  if (!cart || cart.items.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center">
        <div className="w-20 h-20 mx-auto rounded-3xl bg-indigo-50 dark:bg-indigo-950/50 flex items-center justify-center text-indigo-600 dark:text-indigo-400 mb-6">
          <ShoppingBag className="w-10 h-10" />
        </div>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
          Your Shopping Cart is Empty
        </h2>
        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400 max-w-md mx-auto">
          Explore our AI-curated catalog to find top-rated audio gear, performance shoes, and intelligent gadgets.
        </p>
        <Link
          to="/products"
          className="mt-8 inline-flex items-center gap-2 px-6 py-3.5 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm shadow-xl shadow-indigo-600/30 transition-all"
        >
          <span>Start Shopping</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full">
      <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white mb-8">
        Your Shopping Cart ({cart.items.reduce((acc, i) => acc + i.quantity, 0)} items)
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
        {/* Cart Items List */}
        <div className="lg:col-span-2 space-y-4">
          {cart.items.map((item) => {
            const product = item.product;
            const image =
              product?.images && product.images.length > 0
                ? product.images[0].image_url
                : 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400';

            return (
              <div
                key={item.id}
                className="bg-white dark:bg-slate-900 p-4 sm:p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col sm:flex-row items-center gap-4 sm:gap-6"
              >
                <div className="w-24 h-24 rounded-xl bg-slate-100 dark:bg-slate-800 overflow-hidden flex-shrink-0">
                  <img src={image} alt={product?.name || 'Product'} className="w-full h-full object-cover" />
                </div>

                <div className="flex-1 w-full sm:w-auto">
                  <Link
                    to={`/product/${product?.slug || ''}`}
                    className="text-sm sm:text-base font-bold text-slate-800 dark:text-slate-100 hover:text-indigo-600 line-clamp-2"
                  >
                    {product?.name || `Product #${item.product_id}`}
                  </Link>
                  <p className="text-xs text-slate-400 mt-1">
                    Unit Price: ${Number(item.price_at_addition).toFixed(2)}
                  </p>
                </div>

                {/* Quantity Controls */}
                <div className="flex items-center gap-3">
                  <div className="flex items-center border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-800 p-1">
                    <button
                      onClick={() => updateQuantity(item.id, Math.max(1, item.quantity - 1))}
                      disabled={loading || item.quantity <= 1}
                      className="px-2.5 py-1 text-slate-600 dark:text-slate-300 hover:bg-white dark:hover:bg-slate-700 rounded-lg text-xs font-bold disabled:opacity-30"
                    >
                      -
                    </button>
                    <span className="px-3 text-xs font-bold text-slate-900 dark:text-white">
                      {item.quantity}
                    </span>
                    <button
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                      disabled={loading}
                      className="px-2.5 py-1 text-slate-600 dark:text-slate-300 hover:bg-white dark:hover:bg-slate-700 rounded-lg text-xs font-bold"
                    >
                      +
                    </button>
                  </div>

                  <span className="text-base font-extrabold text-slate-900 dark:text-white w-20 text-right">
                    ${(Number(item.price_at_addition) * item.quantity).toFixed(2)}
                  </span>

                  <button
                    onClick={() => removeItem(item.id)}
                    className="p-2 text-slate-400 hover:text-rose-500 rounded-xl hover:bg-rose-50 dark:hover:bg-rose-950/30 transition-colors"
                    title="Remove item"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        {/* Order Summary Card */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-5">
            <h3 className="text-base font-bold text-slate-900 dark:text-white">Order Summary</h3>

            {/* Price Line Items */}
            <div className="space-y-3 text-xs">
              <div className="flex justify-between text-slate-600 dark:text-slate-400">
                <span>Subtotal</span>
                <span className="font-semibold text-slate-800 dark:text-slate-200">
                  ${Number(cart.subtotal).toFixed(2)}
                </span>
              </div>
              <div className="flex justify-between text-slate-600 dark:text-slate-400">
                <span>Estimated Tax</span>
                <span className="font-semibold text-slate-800 dark:text-slate-200">
                  ${Number(cart.tax_amount).toFixed(2)}
                </span>
              </div>
              <div className="flex justify-between text-slate-600 dark:text-slate-400">
                <span>Shipping Fee</span>
                <span className="font-semibold text-slate-800 dark:text-slate-200">
                  {cart.shipping_fee > 0 ? `$${Number(cart.shipping_fee).toFixed(2)}` : 'FREE'}
                </span>
              </div>

              {cart.discount_amount > 0 && (
                <div className="flex justify-between text-emerald-600 dark:text-emerald-400 font-semibold pt-1 border-t border-dashed border-emerald-200">
                  <span>Coupon Discount ({cart.coupon_code})</span>
                  <span>-${Number(cart.discount_amount).toFixed(2)}</span>
                </div>
              )}

              <div className="pt-3 border-t border-slate-200 dark:border-slate-800 flex justify-between text-base font-black text-slate-900 dark:text-white">
                <span>Total Due</span>
                <span className="text-indigo-600 dark:text-indigo-400">
                  ${Number(cart.total_amount).toFixed(2)}
                </span>
              </div>
            </div>

            {/* Coupon Code Entry */}
            <form onSubmit={handleApplyCoupon} className="pt-2">
              <label className="block text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1.5 flex items-center gap-1">
                <Tag className="w-3.5 h-3.5 text-indigo-500" /> Have a Promo Code?
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="e.g. WELCOME10"
                  value={couponInput}
                  onChange={(e) => setCouponInput(e.target.value)}
                  className="flex-1 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs uppercase px-3 py-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="px-4 py-2 bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 rounded-xl text-xs font-bold hover:opacity-90 transition-opacity"
                >
                  Apply
                </button>
              </div>
              {couponMsg && (
                <p
                  className={`mt-2 text-[11px] font-medium ${
                    couponMsg.type === 'success' ? 'text-emerald-600' : 'text-rose-500'
                  }`}
                >
                  {couponMsg.text}
                </p>
              )}
            </form>

            {/* Checkout CTA */}
            <button
              onClick={handleProceedToCheckout}
              disabled={loading}
              className="w-full py-4 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-xl shadow-indigo-600/30 flex items-center justify-center gap-2 transition-all"
            >
              <span>Proceed to Secure Checkout</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <div className="flex items-center justify-center gap-2 text-xs text-slate-400 pt-2">
              <ShieldCheck className="w-4 h-4 text-emerald-500" />
              <span>256-bit Encrypted Transaction</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
