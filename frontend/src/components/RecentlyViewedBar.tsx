import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { History, ArrowRight, ShoppingCart } from 'lucide-react';
import { api } from '../services/api';
import { useCart } from '../context/CartContext';

export const RecentlyViewedBar: React.FC = () => {
  const [items, setItems] = useState<any[]>([]);
  const { addToCart } = useCart();

  useEffect(() => {
    api.getRecentlyViewed(8)
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setItems(data);
        }
      })
      .catch(() => {});
  }, []);

  if (!items || items.length === 0) return null;

  return (
    <section className="my-10 bg-slate-50 dark:bg-slate-900/60 p-6 rounded-2xl border border-slate-200 dark:border-slate-800">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="p-1.5 bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-lg">
            <History className="w-4 h-4" />
          </span>
          <h3 className="font-bold text-slate-900 dark:text-white text-base">
            Recently Viewed by You
          </h3>
        </div>
        <Link to="/products" className="text-xs font-semibold text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1">
          Explore More <ArrowRight className="w-3 h-3" />
        </Link>
      </div>

      <div className="flex items-center gap-4 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-slate-300 dark:scrollbar-thumb-slate-700">
        {items.map((prod) => (
          <div
            key={prod.id}
            className="w-44 flex-shrink-0 bg-white dark:bg-slate-800 rounded-xl p-3 border border-slate-200/80 dark:border-slate-700/80 shadow-xs hover:shadow-md transition-all group"
          >
            <Link to={`/product/${prod.slug}`} className="block">
              <div className="h-28 bg-slate-100 dark:bg-slate-700 rounded-lg overflow-hidden flex items-center justify-center mb-2">
                {prod.images && prod.images.length > 0 ? (
                  <img src={prod.images[0].image_url} alt={prod.name} className="w-full h-full object-cover group-hover:scale-105 transition-all" />
                ) : (
                  <div className="text-xs text-slate-400">No Image</div>
                )}
              </div>
              <h4 className="text-xs font-semibold text-slate-800 dark:text-slate-200 truncate">{prod.name}</h4>
              <p className="text-xs font-bold text-slate-900 dark:text-white mt-1">${prod.price?.toFixed(2)}</p>
            </Link>

            <button
              onClick={() => addToCart(prod, 1)}
              className="mt-2 w-full flex items-center justify-center gap-1 py-1.5 bg-slate-100 hover:bg-blue-600 hover:text-white text-slate-700 dark:bg-slate-700 dark:text-slate-200 text-xs font-semibold rounded-lg transition-colors"
            >
              <ShoppingCart className="w-3 h-3" />
              Add
            </button>
          </div>
        ))}
      </div>
    </section>
  );
};
