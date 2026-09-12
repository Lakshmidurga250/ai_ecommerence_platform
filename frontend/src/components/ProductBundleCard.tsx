import React, { useState } from 'react';
import { Plus, Check, ShoppingBag, Sparkles, ArrowRight } from 'lucide-react';
import { useCart } from '../context/CartContext';

interface ProductBundleCardProps {
  bundle: {
    bundle_id: number;
    bundle_name: string;
    discount_percent: number;
    bundle_price: number;
    regular_price: number;
    savings: number;
    primary_product: {
      id: number;
      name: string;
      price: number;
      image?: string;
    };
    bundled_product: {
      id: number;
      name: string;
      price: number;
      image?: string;
    };
  };
}

export const ProductBundleCard: React.FC<ProductBundleCardProps> = ({ bundle }) => {
  const { addToCart } = useCart();
  const [added, setAdded] = useState(false);

  const handleAddBundle = () => {
    // Add primary product
    addToCart({
      id: bundle.primary_product.id,
      name: bundle.primary_product.name,
      price: bundle.primary_product.price,
      image_url: bundle.primary_product.image,
      stock_quantity: 10
    } as any, 1);

    // Add bundled product with applied discount
    const discountedPrice = round(bundle.bundled_product.price * (1 - bundle.discount_percent / 100), 2);
    addToCart({
      id: bundle.bundled_product.id,
      name: `${bundle.bundled_product.name} (Bundle Savings)`,
      price: discountedPrice,
      image_url: bundle.bundled_product.image,
      stock_quantity: 10
    } as any, 1);

    setAdded(true);
    setTimeout(() => setAdded(false), 2500);
  };

  const round = (val: number, decimals: number) => {
    return Number(Math.round(Number(val + 'e' + decimals)) + 'e-' + decimals);
  };

  return (
    <div className="bg-gradient-to-br from-indigo-50/70 via-white to-blue-50/70 dark:from-slate-900 dark:to-slate-800 rounded-2xl p-6 border border-indigo-100/80 dark:border-slate-700 shadow-sm hover:shadow-md transition-all">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="p-1.5 bg-indigo-600 text-white rounded-lg shadow-sm">
            <Sparkles className="w-4 h-4" />
          </span>
          <h3 className="font-bold text-slate-900 dark:text-white text-base">
            Frequently Bought Together
          </h3>
        </div>
        <span className="bg-emerald-100 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 font-bold text-xs px-2.5 py-1 rounded-full border border-emerald-200/60">
          Save {bundle.discount_percent}% on Bundle
        </span>
      </div>

      <div className="flex flex-col md:flex-row items-center gap-4 my-4">
        {/* Primary Item */}
        <div className="flex items-center gap-3 flex-1 bg-white dark:bg-slate-800/80 p-3.5 rounded-xl border border-slate-200/80 dark:border-slate-700 w-full">
          <div className="w-16 h-16 rounded-lg bg-slate-100 dark:bg-slate-700 overflow-hidden flex-shrink-0 flex items-center justify-center">
            {bundle.primary_product.image ? (
              <img src={bundle.primary_product.image} alt={bundle.primary_product.name} className="w-full h-full object-cover" />
            ) : (
              <ShoppingBag className="w-6 h-6 text-slate-400" />
            )}
          </div>
          <div className="min-w-0 flex-1">
            <p className="text-xs font-semibold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">This Item</p>
            <h4 className="text-sm font-semibold text-slate-800 dark:text-slate-200 truncate">{bundle.primary_product.name}</h4>
            <p className="text-sm font-bold text-slate-900 dark:text-white">${bundle.primary_product.price.toFixed(2)}</p>
          </div>
        </div>

        {/* Plus Sign */}
        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-300 font-black shadow-inner">
          <Plus className="w-4 h-4" />
        </div>

        {/* Bundled Item */}
        <div className="flex items-center gap-3 flex-1 bg-white dark:bg-slate-800/80 p-3.5 rounded-xl border border-slate-200/80 dark:border-slate-700 w-full">
          <div className="w-16 h-16 rounded-lg bg-slate-100 dark:bg-slate-700 overflow-hidden flex-shrink-0 flex items-center justify-center">
            {bundle.bundled_product.image ? (
              <img src={bundle.bundled_product.image} alt={bundle.bundled_product.name} className="w-full h-full object-cover" />
            ) : (
              <ShoppingBag className="w-6 h-6 text-slate-400" />
            )}
          </div>
          <div className="min-w-0 flex-1">
            <p className="text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">Recommended Pairing</p>
            <h4 className="text-sm font-semibold text-slate-800 dark:text-slate-200 truncate">{bundle.bundled_product.name}</h4>
            <div className="flex items-center gap-1.5">
              <span className="text-sm font-bold text-slate-900 dark:text-white">
                ${(bundle.bundled_product.price * (1 - bundle.discount_percent / 100)).toFixed(2)}
              </span>
              <span className="text-xs text-slate-400 line-through">
                ${bundle.bundled_product.price.toFixed(2)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Pricing and Action Footer */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-3 border-t border-slate-100 dark:border-slate-700/60 mt-3">
        <div>
          <div className="flex items-baseline gap-2">
            <span className="text-xs text-slate-500">Total Bundle Price:</span>
            <span className="text-xl font-black text-indigo-600 dark:text-indigo-400">
              ${bundle.bundle_price.toFixed(2)}
            </span>
            <span className="text-sm text-slate-400 line-through">
              ${bundle.regular_price.toFixed(2)}
            </span>
          </div>
          <p className="text-xs font-medium text-emerald-600 dark:text-emerald-400">
            Instant savings of ${bundle.savings.toFixed(2)} when bought together
          </p>
        </div>

        <button
          onClick={handleAddBundle}
          disabled={added}
          className={`flex items-center gap-2 px-5 py-2.5 rounded-xl font-bold text-sm shadow-md transition-all ${
            added
              ? 'bg-emerald-600 text-white shadow-emerald-500/30'
              : 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-indigo-500/25 hover:scale-[1.02]'
          }`}
        >
          {added ? (
            <>
              <Check className="w-4 h-4" />
              Bundle Added to Cart!
            </>
          ) : (
            <>
              <ShoppingBag className="w-4 h-4" />
              Add Both to Cart
            </>
          )}
        </button>
      </div>
    </div>
  );
};
