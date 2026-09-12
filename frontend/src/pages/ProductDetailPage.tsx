import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Star, ShoppingCart, ShieldCheck, Truck, RotateCcw, Sparkles, Check, ChevronRight } from 'lucide-react';
import { Product } from '../types';
import { api } from '../services/api';
import { useCart } from '../context/CartContext';
import { RecommendationSection } from '../components/RecommendationSection';

export const ProductDetailPage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [selectedImage, setSelectedImage] = useState<string>('');
  const [quantity, setQuantity] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(true);
  const [addedSuccess, setAddedSuccess] = useState<boolean>(false);
  const { addItem, loading: cartLoading } = useCart();

  useEffect(() => {
    const fetchProduct = async () => {
      if (!slug) return;
      setLoading(true);
      try {
        const data = await api.getProductBySlug(slug);
        setProduct(data);
        if (data.images && data.images.length > 0) {
          const primary = data.images.find((i) => i.is_primary) || data.images[0];
          setSelectedImage(primary.image_url);
        }
        api.recordBehaviorEvent('PRODUCT_VIEW', data.id);
      } catch (err) {
        console.error('Failed to load product detail:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [slug]);

  const handleAddToCart = async () => {
    if (!product) return;
    await addItem(product.id, quantity);
    api.recordBehaviorEvent('ADD_TO_CART', product.id, { quantity, price: product.price });
    setAddedSuccess(true);
    setTimeout(() => setAddedSuccess(false), 3000);
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 animate-pulse space-y-8">
        <div className="h-6 bg-slate-200 dark:bg-slate-800 rounded w-1/4" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          <div className="aspect-square bg-slate-200 dark:bg-slate-800 rounded-3xl" />
          <div className="space-y-4">
            <div className="h-8 bg-slate-200 dark:bg-slate-800 rounded w-3/4" />
            <div className="h-6 bg-slate-200 dark:bg-slate-800 rounded w-1/3" />
            <div className="h-24 bg-slate-200 dark:bg-slate-800 rounded" />
          </div>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-20 text-center">
        <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100">Product Not Found</h2>
        <p className="text-slate-500 mt-2">The product you are looking for may have been moved or archived.</p>
        <Link to="/products" className="inline-block mt-4 px-6 py-2.5 bg-indigo-600 text-white rounded-xl text-sm font-semibold">
          Return to Catalog
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Breadcrumbs */}
      <nav className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 mb-6">
        <Link to="/" className="hover:text-indigo-600">Home</Link>
        <ChevronRight className="w-3.5 h-3.5" />
        <Link to="/products" className="hover:text-indigo-600">Catalog</Link>
        {product.category && (
          <>
            <ChevronRight className="w-3.5 h-3.5" />
            <Link to={`/products?category=${product.category.slug}`} className="hover:text-indigo-600">
              {product.category.name}
            </Link>
          </>
        )}
        <ChevronRight className="w-3.5 h-3.5" />
        <span className="text-slate-800 dark:text-slate-200 font-semibold truncate max-w-xs">{product.name}</span>
      </nav>

      {/* Hero Product Info */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
        {/* Images Gallery */}
        <div className="flex flex-col gap-4">
          <div className="aspect-square w-full rounded-3xl overflow-hidden bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-800 shadow-inner">
            <img
              src={selectedImage || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800'}
              alt={product.name}
              className="w-full h-full object-contain p-4"
            />
          </div>
          {product.images && product.images.length > 1 && (
            <div className="flex gap-3 overflow-x-auto pb-2">
              {product.images.map((img) => (
                <button
                  key={img.id}
                  onClick={() => setSelectedImage(img.image_url)}
                  className={`w-20 h-20 rounded-xl overflow-hidden border-2 flex-shrink-0 transition-all ${
                    selectedImage === img.image_url ? 'border-indigo-600 shadow-md' : 'border-slate-200 dark:border-slate-800 opacity-70 hover:opacity-100'
                  }`}
                >
                  <img src={img.image_url} alt="" className="w-full h-full object-cover" />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Product Details & Purchasing */}
        <div className="flex flex-col">
          <div className="flex items-center gap-2 mb-2">
            {product.brand && (
              <span className="px-2.5 py-1 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-semibold">
                {product.brand.name}
              </span>
            )}
            <span className="text-xs text-slate-400 font-mono">SKU: {product.sku}</span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white leading-tight">
            {product.name}
          </h1>

          {/* Rating */}
          <div className="flex items-center gap-3 mt-3">
            <div className="flex items-center gap-1 text-amber-400">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={`w-4 h-4 ${
                    i < Math.floor(product.rating || 0) ? 'fill-amber-400 text-amber-400' : 'text-slate-300 dark:text-slate-700'
                  }`}
                />
              ))}
              <span className="text-sm font-bold text-slate-800 dark:text-slate-200 ml-1">
                {Number(product.rating || 0).toFixed(1)}
              </span>
            </div>
            <span className="text-xs text-slate-400">({product.review_count || 0} reviews)</span>
            <span className="text-xs text-slate-400">•</span>
            <span className="text-xs text-emerald-600 font-semibold">{product.sales_count || 0} verified orders</span>
          </div>

          {/* Price Block */}
          <div className="mt-6 p-4 rounded-2xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-baseline justify-between">
            <div>
              <div className="flex items-baseline gap-3">
                <span className="text-3xl font-black text-slate-900 dark:text-white">
                  ${Number(product.price).toFixed(2)}
                </span>
                {product.compare_at_price && product.compare_at_price > product.price && (
                  <span className="text-base text-slate-400 line-through">
                    ${Number(product.compare_at_price).toFixed(2)}
                  </span>
                )}
                {product.discount_percent > 0 && (
                  <span className="px-2 py-0.5 rounded-full text-xs font-bold bg-rose-500 text-white">
                    Save {product.discount_percent}%
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-400 mt-1">Inclusive of estimated local taxes &amp; duties</p>
            </div>

            <div className="text-right">
              <span className={`text-xs font-bold px-3 py-1 rounded-full ${
                product.stock > 0 ? 'bg-emerald-50 text-emerald-600 dark:bg-emerald-950/40 dark:text-emerald-400' : 'bg-rose-50 text-rose-600'
              }`}>
                {product.stock > 0 ? `${product.stock} In Stock` : 'Out of Stock'}
              </span>
            </div>
          </div>

          {/* Short Description */}
          <p className="mt-6 text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            {product.short_description || product.description}
          </p>

          {/* Purchase Stepper & Actions */}
          <div className="mt-8 pt-6 border-t border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row items-center gap-4">
            <div className="flex items-center border border-slate-200 dark:border-slate-700 rounded-xl bg-white dark:bg-slate-800 p-1">
              <button
                onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                className="px-3 py-1 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg text-sm font-bold"
                disabled={quantity <= 1}
              >
                -
              </button>
              <span className="px-4 text-sm font-bold text-slate-900 dark:text-white">{quantity}</span>
              <button
                onClick={() => setQuantity((q) => Math.min(product.stock, q + 1))}
                className="px-3 py-1 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg text-sm font-bold"
                disabled={quantity >= product.stock}
              >
                +
              </button>
            </div>

            <button
              onClick={handleAddToCart}
              disabled={cartLoading || product.stock <= 0}
              className={`flex-1 w-full sm:w-auto py-3.5 px-6 rounded-2xl font-bold text-sm shadow-xl flex items-center justify-center gap-2 transition-all ${
                addedSuccess
                  ? 'bg-emerald-600 text-white shadow-emerald-600/30'
                  : 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-indigo-600/30'
              } disabled:opacity-50`}
            >
              {addedSuccess ? (
                <>
                  <Check className="w-4 h-4" /> Added to Bag!
                </>
              ) : (
                <>
                  <ShoppingCart className="w-4 h-4" /> Add to Shopping Bag
                </>
              )}
            </button>
          </div>

          {/* Value Props */}
          <div className="mt-8 grid grid-cols-3 gap-4 pt-6 border-t border-slate-200 dark:border-slate-800 text-center">
            <div className="flex flex-col items-center gap-1.5 text-xs text-slate-500">
              <ShieldCheck className="w-5 h-5 text-indigo-500" />
              <span>Authentic Guarantee</span>
            </div>
            <div className="flex flex-col items-center gap-1.5 text-xs text-slate-500">
              <Truck className="w-5 h-5 text-indigo-500" />
              <span>Express Delivery</span>
            </div>
            <div className="flex flex-col items-center gap-1.5 text-xs text-slate-500">
              <RotateCcw className="w-5 h-5 text-indigo-500" />
              <span>30-Day Easy Returns</span>
            </div>
          </div>
        </div>
      </div>

      {/* Specifications / Attributes Table */}
      {product.attributes && Object.keys(product.attributes).length > 0 && (
        <div className="mb-16 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 sm:p-8">
          <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-4">
            Technical Specifications
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(product.attributes).map(([key, val]) => (
              <div key={key} className="flex justify-between py-2 border-b border-slate-100 dark:border-slate-800 text-xs">
                <span className="font-semibold text-slate-500 dark:text-slate-400 capitalize">{key.replace(/_/g, ' ')}</span>
                <span className="font-medium text-slate-800 dark:text-slate-200">{String(val)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Grounded Recommendations for this Product */}
      <RecommendationSection
        productId={product.id}
        title="Frequently Purchased Together &amp; Similar Products"
        defaultStrategy="CONTENT_BASED"
      />
    </div>
  );
};
