import React from 'react';
import { Link } from 'react-router-dom';
import { Star, ShoppingCart, Eye, Sparkles } from 'lucide-react';
import { Product } from '../types';
import { useCart } from '../context/CartContext';
import { api } from '../services/api';

interface ProductCardProps {
  product: Product;
  badge?: string;
  explanation?: string;
  matchScore?: number;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  badge,
  explanation,
  matchScore,
}) => {
  const { addItem, loading } = useCart();

  const handleProductClick = () => {
    api.recordBehaviorEvent('PRODUCT_CLICK', product.id, {
      name: product.name,
      price: product.price,
    });
  };

  const handleAddToCart = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    await addItem(product.id, 1);
    api.recordBehaviorEvent('ADD_TO_CART', product.id, {
      price: product.price,
    });
  };

  const primaryImage =
    product.images && product.images.length > 0
      ? product.images.find((img) => img.is_primary)?.image_url || product.images[0].image_url
      : 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80';

  return (
    <div className="group relative bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col overflow-hidden">
      {/* Top Media Container */}
      <div className="relative aspect-square w-full overflow-hidden bg-slate-100 dark:bg-slate-800">
        <Link to={`/product/${product.slug}`} onClick={handleProductClick}>
          <img
            src={primaryImage}
            alt={product.name}
            className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500 ease-out"
            loading="lazy"
          />
        </Link>

        {/* Badges */}
        <div className="absolute top-3 left-3 flex flex-col gap-1.5 pointer-events-none">
          {badge && (
            <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-indigo-600 text-white shadow-md">
              {badge}
            </span>
          )}
          {product.discount_percent > 0 && (
            <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-rose-500 text-white shadow-md">
              -{product.discount_percent}%
            </span>
          )}
          {product.stock <= 5 && product.stock > 0 && (
            <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-amber-500 text-white shadow-md">
              Only {product.stock} left
            </span>
          )}
        </div>

        {/* AI Match Score Badge if applicable */}
        {matchScore !== undefined && (
          <div className="absolute top-3 right-3 flex items-center gap-1 bg-slate-900/80 backdrop-blur-md px-2.5 py-1 rounded-full text-xs font-semibold text-emerald-400 border border-emerald-500/30 shadow-md">
            <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
            <span>{Math.round(matchScore * 100)}% Match</span>
          </div>
        )}

        {/* Hover Quick Actions */}
        <div className="absolute inset-x-3 bottom-3 opacity-0 group-hover:opacity-100 transition-all duration-300 flex gap-2">
          <Link
            to={`/product/${product.slug}`}
            onClick={handleProductClick}
            className="flex-1 flex items-center justify-center gap-1.5 py-2.5 bg-white/95 dark:bg-slate-800/95 backdrop-blur-sm text-slate-800 dark:text-slate-100 rounded-xl text-xs font-semibold shadow-lg hover:bg-white dark:hover:bg-slate-800 transition-colors"
          >
            <Eye className="w-3.5 h-3.5" /> Quick View
          </Link>
          <button
            onClick={handleAddToCart}
            disabled={loading || product.stock <= 0}
            className="flex items-center justify-center px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            title="Add to Cart"
          >
            <ShoppingCart className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Product Information */}
      <div className="p-4 flex flex-col flex-1">
        {/* Category & Brand */}
        <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 mb-1.5 font-medium">
          <span>{product.category?.name || 'General'}</span>
          {product.brand && <span className="text-slate-700 dark:text-slate-300 font-semibold">{product.brand.name}</span>}
        </div>

        {/* Title */}
        <Link
          to={`/product/${product.slug}`}
          onClick={handleProductClick}
          className="text-sm font-semibold text-slate-800 dark:text-slate-100 hover:text-indigo-600 dark:hover:text-indigo-400 line-clamp-2 transition-colors mb-2"
        >
          {product.name}
        </Link>

        {/* AI Recommendation Reasoning */}
        {explanation && (
          <div className="mb-2.5 p-2 rounded-lg bg-indigo-50/80 dark:bg-indigo-950/40 border border-indigo-100 dark:border-indigo-900/50 text-[11px] text-indigo-700 dark:text-indigo-300 flex items-start gap-1.5">
            <Sparkles className="w-3.5 h-3.5 flex-shrink-0 mt-0.5 text-indigo-500" />
            <span className="line-clamp-2 italic">{explanation}</span>
          </div>
        )}

        {/* Rating and Sales */}
        <div className="flex items-center gap-2 mt-auto mb-3">
          <div className="flex items-center gap-1 text-amber-400">
            <Star className="w-4 h-4 fill-amber-400" />
            <span className="text-xs font-bold text-slate-700 dark:text-slate-300">
              {Number(product.rating || 0).toFixed(1)}
            </span>
          </div>
          <span className="text-xs text-slate-400">
            ({product.review_count || 0})
          </span>
          {product.sales_count > 0 && (
            <span className="text-xs text-slate-400 ml-auto">
              {product.sales_count} sold
            </span>
          )}
        </div>

        {/* Pricing */}
        <div className="flex items-baseline justify-between pt-2 border-t border-slate-100 dark:border-slate-800">
          <div className="flex items-baseline gap-2">
            <span className="text-lg font-extrabold text-slate-900 dark:text-white">
              ₹{Number(product.price).toLocaleString('en-IN')}
            </span>
            {product.compare_at_price && product.compare_at_price > product.price && (
              <span className="text-xs text-slate-400 line-through">
                ₹{Number(product.compare_at_price).toLocaleString('en-IN')}
              </span>
            )}
          </div>
          <span className={`text-xs font-semibold ${product.stock > 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-500'}`}>
            {product.stock > 0 ? 'In Stock' : 'Out of Stock'}
          </span>
        </div>

      </div>
    </div>
  );
};
