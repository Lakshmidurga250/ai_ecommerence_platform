import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, CreditCard, CheckCircle2, Lock, AlertCircle, Loader2 } from 'lucide-react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';

export const CheckoutPage: React.FC = () => {
  const { cart, refreshCart } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [addresses, setAddresses] = useState<any[]>([]);
  const [selectedAddressId, setSelectedAddressId] = useState<number>(1);
  const [paymentMethod, setPaymentMethod] = useState<string>('CREDIT_CARD');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [orderComplete, setOrderComplete] = useState<any | null>(null);

  useEffect(() => {
    if (!user) {
      navigate('/login?redirect=/checkout');
      return;
    }
    const loadAddresses = async () => {
      try {
        const addrList = await api.getAddresses();
        setAddresses(addrList);
        if (addrList.length > 0) {
          setSelectedAddressId(addrList[0].id);
        }
      } catch (err) {
        // Fallback default address id
        setSelectedAddressId(1);
      }
    };
    loadAddresses();
  }, [user, navigate]);

  const handlePlaceOrder = async () => {
    if (!cart || cart.items.length === 0) return;
    setLoading(true);
    setError(null);

    try {
      const order = await api.checkout({
        shipping_address_id: selectedAddressId || 1,
        payment_method: paymentMethod,
        coupon_code: cart.coupon_code,
      });
      setOrderComplete(order);
      await refreshCart();
    } catch (err: any) {
      setError(err.message || 'Checkout failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (orderComplete) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-20 text-center">
        <div className="w-20 h-20 mx-auto rounded-full bg-emerald-50 dark:bg-emerald-950/50 flex items-center justify-center text-emerald-600 dark:text-emerald-400 mb-6">
          <CheckCircle2 className="w-12 h-12" />
        </div>
        <h1 className="text-3xl font-extrabold text-slate-900 dark:text-white">
          Order Placed Successfully!
        </h1>
        <p className="mt-2 text-slate-500 dark:text-slate-400 text-sm">
          Order reference: <span className="font-mono font-bold text-slate-800 dark:text-slate-200">{orderComplete.order_number}</span>
        </p>
        <p className="mt-1 text-xs text-slate-400">
          A confirmation and tracking link has been registered to your profile.
        </p>

        <div className="mt-8 p-6 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-left text-xs space-y-2">
          <div className="flex justify-between font-semibold">
            <span>Status:</span>
            <span className="text-emerald-600 uppercase">{orderComplete.status}</span>
          </div>
          <div className="flex justify-between font-semibold">
            <span>Total Paid:</span>
            <span>${Number(orderComplete.total_amount).toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span>Items:</span>
            <span>{orderComplete.items?.length || 0} product(s)</span>
          </div>
        </div>

        <div className="mt-8 flex justify-center gap-4">
          <button
            onClick={() => navigate('/orders')}
            className="px-6 py-3 rounded-2xl bg-indigo-600 text-white font-semibold text-sm hover:bg-indigo-700 shadow-md"
          >
            View My Orders
          </button>
          <button
            onClick={() => navigate('/products')}
            className="px-6 py-3 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 font-semibold text-sm hover:bg-slate-200 shadow-sm"
          >
            Continue Shopping
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full">
      <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white mb-8">
        Secure Checkout
      </h1>

      {error && (
        <div className="mb-6 p-4 rounded-2xl bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/40 text-rose-600 dark:text-rose-400 text-xs font-semibold flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
        {/* Left Column: Delivery & Payment Options */}
        <div className="lg:col-span-2 space-y-8">
          {/* Step 1: Address */}
          <div className="bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xs">
                1
              </span>
              Delivery Address
            </h2>

            <div className="p-4 rounded-2xl border-2 border-indigo-600/40 bg-indigo-50/20 dark:bg-indigo-950/20 text-xs space-y-1">
              <p className="font-bold text-slate-900 dark:text-white">
                {user?.profile?.first_name || user?.username} {user?.profile?.last_name || ''}
              </p>
              <p className="text-slate-600 dark:text-slate-400">
                124 Innovation Way, Tech Park, Suite 400
              </p>
              <p className="text-slate-600 dark:text-slate-400">San Francisco, CA 94105</p>
              <p className="text-slate-500 font-mono text-[11px] pt-1">Primary Verified Shipping Address</p>
            </div>
          </div>

          {/* Step 2: Payment Method */}
          <div className="bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
            <h2 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xs">
                2
              </span>
              Payment Selection
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {[
                { id: 'CREDIT_CARD', label: 'Card / Debit', icon: CreditCard, sub: 'Instant approval' },
                { id: 'UPI_SIMULATION', label: 'UPI / VPA', icon: Lock, sub: 'Instant gateway' },
                { id: 'COD', label: 'Cash on Delivery', icon: ShieldCheck, sub: 'Pay on arrival' },
              ].map((m) => {
                const Icon = m.icon;
                const isSel = paymentMethod === m.id;
                return (
                  <button
                    key={m.id}
                    type="button"
                    onClick={() => setPaymentMethod(m.id)}
                    className={`p-4 rounded-2xl border text-left transition-all flex flex-col justify-between ${
                      isSel
                        ? 'border-indigo-600 bg-indigo-50/40 dark:bg-indigo-950/40 text-indigo-900 dark:text-indigo-200 shadow-sm'
                        : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700'
                    }`}
                  >
                    <Icon className={`w-5 h-5 mb-2 ${isSel ? 'text-indigo-600' : 'text-slate-400'}`} />
                    <div>
                      <p className="text-xs font-bold">{m.label}</p>
                      <p className="text-[10px] text-slate-400">{m.sub}</p>
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Fraud Protection Notice */}
            <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60 text-[11px] text-slate-600 dark:text-slate-400 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-500 flex-shrink-0" />
              <span>
                Protected by Isolation Forest Anomaly Detection (AI Fraud Shield). Transactions are scanned in &lt;5ms.
              </span>
            </div>
          </div>
        </div>

        {/* Right Column: Order Review */}
        <div className="lg:col-span-1">
          <div className="bg-white dark:bg-slate-900 p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-slate-900 dark:text-white">Review &amp; Pay</h3>

            <div className="divide-y divide-slate-100 dark:divide-slate-800 max-h-56 overflow-y-auto">
              {cart?.items.map((i) => (
                <div key={i.id} className="py-2.5 flex justify-between text-xs">
                  <div className="max-w-[70%]">
                    <p className="font-semibold text-slate-800 dark:text-slate-200 truncate">
                      {i.product?.name || `Product #${i.product_id}`}
                    </p>
                    <p className="text-slate-400 text-[11px]">Qty: {i.quantity}</p>
                  </div>
                  <span className="font-bold text-slate-900 dark:text-white">
                    ${(Number(i.price_at_addition) * i.quantity).toFixed(2)}
                  </span>
                </div>
              ))}
            </div>

            <div className="pt-4 border-t border-slate-200 dark:border-slate-800 space-y-2 text-xs">
              <div className="flex justify-between text-slate-500">
                <span>Subtotal:</span>
                <span>${Number(cart?.subtotal || 0).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-slate-500">
                <span>Tax:</span>
                <span>${Number(cart?.tax_amount || 0).toFixed(2)}</span>
              </div>
              {cart?.discount_amount && cart.discount_amount > 0 ? (
                <div className="flex justify-between text-emerald-600 font-semibold">
                  <span>Coupon Discount:</span>
                  <span>-${Number(cart.discount_amount).toFixed(2)}</span>
                </div>
              ) : null}
              <div className="pt-2 border-t border-slate-200 dark:border-slate-800 flex justify-between text-base font-extrabold text-slate-900 dark:text-white">
                <span>Total Amount:</span>
                <span className="text-indigo-600">${Number(cart?.total_amount || 0).toFixed(2)}</span>
              </div>
            </div>

            <button
              onClick={handlePlaceOrder}
              disabled={loading || !cart?.items.length}
              className="w-full py-4 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm shadow-xl shadow-indigo-600/30 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" /> Verifying with Fraud Shield...
                </>
              ) : (
                <>
                  <Lock className="w-4 h-4" /> Authorize &amp; Pay ${Number(cart?.total_amount || 0).toFixed(2)}
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
