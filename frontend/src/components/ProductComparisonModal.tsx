import React from 'react';
import { X, Check, Minus, ShoppingCart, Star, ShieldCheck } from 'lucide-react';
import { useCart } from '../context/CartContext';

interface ProductComparisonModalProps {
  isOpen: boolean;
  onClose: () => void;
  products: any[];
}

export const ProductComparisonModal: React.FC<ProductComparisonModalProps> = ({
  isOpen,
  onClose,
  products
}) => {
  const { addToCart } = useCart();

  if (!isOpen || !products || products.length === 0) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white dark:bg-slate-900 w-full max-w-4xl rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 dark:border-slate-800">
          <div>
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">Side-by-Side Product Comparison</h3>
            <p className="text-xs text-slate-500">Evaluating specifications, pricing, and buyer reviews</p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Comparison Table */}
        <div className="overflow-auto p-6">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800">
                <th className="p-3 text-xs font-bold text-slate-400 uppercase tracking-wider w-1/4">Specification</th>
                {products.map((p) => (
                  <th key={p.id} className="p-3 w-1/3">
                    <div className="h-32 rounded-xl bg-slate-100 dark:bg-slate-800 overflow-hidden flex items-center justify-center mb-3">
                      {p.images && p.images.length > 0 ? (
                        <img src={p.images[0].image_url} alt={p.name} className="w-full h-full object-cover" />
                      ) : (
                        <div className="text-xs text-slate-400">Product Image</div>
                      )}
                    </div>
                    <h4 className="font-bold text-sm text-slate-900 dark:text-white line-clamp-2">{p.name}</h4>
                    <p className="text-lg font-black text-indigo-600 dark:text-indigo-400 mt-1">${p.price?.toFixed(2)}</p>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-sm">
              <tr>
                <td className="p-3 font-semibold text-slate-500 text-xs">Brand</td>
                {products.map((p) => (
                  <td key={p.id} className="p-3 font-medium text-slate-800 dark:text-slate-200">
                    {p.brand?.name || 'Generic / Independent'}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-3 font-semibold text-slate-500 text-xs">Customer Rating</td>
                {products.map((p) => (
                  <td key={p.id} className="p-3">
                    <div className="flex items-center gap-1 text-amber-500 font-bold text-xs">
                      <Star className="w-4 h-4 fill-amber-400 text-amber-400" />
                      <span>{p.rating?.toFixed(1) || '5.0'} / 5.0</span>
                    </div>
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-3 font-semibold text-slate-500 text-xs">Category</td>
                {products.map((p) => (
                  <td key={p.id} className="p-3 text-slate-700 dark:text-slate-300">
                    {p.category?.name || 'General Catalog'}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-3 font-semibold text-slate-500 text-xs">Stock Status</td>
                {products.map((p) => (
                  <td key={p.id} className="p-3">
                    {p.stock_quantity > 0 ? (
                      <span className="inline-flex items-center gap-1 text-xs font-bold text-emerald-600 bg-emerald-50 dark:bg-emerald-950/60 px-2 py-0.5 rounded-md">
                        <Check className="w-3 h-3" /> In Stock ({p.stock_quantity})
                      </span>
                    ) : (
                      <span className="text-xs font-bold text-rose-600">Out of Stock</span>
                    )}
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-3 font-semibold text-slate-500 text-xs">Warranty Protection</td>
                {products.map((p) => (
                  <td key={p.id} className="p-3 text-slate-700 dark:text-slate-300 text-xs">
                    <span className="flex items-center gap-1">
                      <ShieldCheck className="w-4 h-4 text-indigo-500" />
                      1-Year Manufacturer Warranty
                    </span>
                  </td>
                ))}
              </tr>
              <tr>
                <td className="p-3 font-semibold text-slate-500 text-xs">Action</td>
                {products.map((p) => (
                  <td key={p.id} className="p-3">
                    <button
                      onClick={() => addToCart(p, 1)}
                      className="flex items-center justify-center gap-1.5 w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-sm transition-colors"
                    >
                      <ShoppingCart className="w-3.5 h-3.5" />
                      Add to Cart
                    </button>
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
