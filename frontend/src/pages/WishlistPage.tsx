import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Heart, ShoppingCart, Trash2, ArrowRight } from 'lucide-react';
import { Product } from '../types';
import { api } from '../services/api';
import { useCart } from '../context/CartContext';

export const WishlistPage: React.FC = () => {
  const [wishlistItems, setWishlistItems] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const { addItem } = useCart();

  useEffect(() => {
    // Fetch top 3 featured products as starter wishlist items if empty
    const loadWishlist = async () => {
      try {
        const prods = await api.getProducts({ limit: 3 });
        setWishlistItems(prods);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadWishlist();
  }, []);

  const handleRemove = (id: number) => {
    setWishlistItems((prev) => prev.filter((p) => p.id !== id));
  };

  const handleMoveToCart = async (product: Product) => {
    await addItem(product.id, 1);
    handleRemove(product.id);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full">
      <div className="flex items-center justify-between pb-6 mb-8 border-b border-slate-200 dark:border-slate-800">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white flex items-center gap-2">
            <Heart className="w-7 h-7 text-rose-500 fill-rose-500" /> My Saved Wishlist
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
            Items you've saved for later purchases
          </p>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-64 bg-slate-100 dark:bg-slate-800 rounded-3xl animate-pulse" />
          ))}
        </div>
      ) : wishlistItems.length === 0 ? (
        <div className="p-16 text-center rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
          <Heart className="w-12 h-12 mx-auto text-slate-300 mb-3" />
          <h3 className="text-base font-bold text-slate-800 dark:text-slate-200">
            Your Wishlist is Empty
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Explore our smart marketplace and save products for later.
          </p>
          <Link
            to="/products"
            className="inline-flex items-center gap-2 mt-4 px-6 py-2.5 bg-indigo-600 text-white rounded-xl text-xs font-bold shadow-md"
          >
            <span>Browse Products</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {wishlistItems.map((p) => (
            <div
              key={p.id}
              className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm flex flex-col justify-between"
            >
              <div className="aspect-square w-full rounded-2xl bg-slate-100 dark:bg-slate-800 overflow-hidden mb-3">
                <img
                  src={
                    p.images && p.images.length > 0
                      ? p.images[0].image_url
                      : 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'
                  }
                  alt={p.name}
                  className="w-full h-full object-cover"
                />
              </div>

              <div>
                <Link
                  to={`/product/${p.slug}`}
                  className="text-sm font-bold text-slate-800 dark:text-slate-200 hover:text-indigo-600 line-clamp-2"
                >
                  {p.name}
                </Link>
                <p className="text-base font-black text-slate-900 dark:text-white mt-2">
                  ${Number(p.price).toFixed(2)}
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex gap-2">
                <button
                  onClick={() => handleMoveToCart(p)}
                  className="flex-1 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-bold flex items-center justify-center gap-1.5 transition-colors"
                >
                  <ShoppingCart className="w-3.5 h-3.5" /> Move to Bag
                </button>
                <button
                  onClick={() => handleRemove(p.id)}
                  className="p-2.5 text-slate-400 hover:text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/30 rounded-xl transition-colors"
                  title="Remove"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
