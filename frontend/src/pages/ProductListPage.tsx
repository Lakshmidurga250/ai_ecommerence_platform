import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Filter, SlidersHorizontal, ArrowUpDown, Sparkles, X, Check } from 'lucide-react';
import { Product, Category } from '../types';
import { api } from '../services/api';
import { ProductCard } from '../components/ProductCard';

export const ProductListPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const queryParam = searchParams.get('q') || '';
  const categoryParam = searchParams.get('category') || '';

  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedCategory, setSelectedCategory] = useState<string>(categoryParam);
  const [minPrice, setMinPrice] = useState<number>(0);
  const [maxPrice, setMaxPrice] = useState<number>(2000);
  const [sortBy, setSortBy] = useState<string>('rating_desc');
  const [inStockOnly, setInStockOnly] = useState<boolean>(false);
  const [parsedIntent, setParsedIntent] = useState<any>(null);

  useEffect(() => {
    const fetchCats = async () => {
      try {
        const cats = await api.getCategories();
        setCategories(cats);
      } catch (err) {
        console.error(err);
      }
    };
    fetchCats();
  }, []);

  useEffect(() => {
    setSelectedCategory(categoryParam);
  }, [categoryParam]);

  useEffect(() => {
    const fetchCatalog = async () => {
      setLoading(true);
      try {
        if (queryParam) {
          // If query present, also inspect AI parsed intent
          api.parseSearchIntent(queryParam).then((intent) => {
            setParsedIntent(intent);
          }).catch(() => {});

          const res = await api.searchProducts(queryParam);
          setProducts(res);
        } else {
          setParsedIntent(null);
          const params: Record<string, any> = {};
          if (selectedCategory) params['category'] = selectedCategory;
          const res = await api.getProducts(params);
          setProducts(res);
        }
      } catch (err) {
        console.error('Failed to load products:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCatalog();
  }, [queryParam, selectedCategory]);

  // Client-side filtering and sorting for interactive experience
  const filteredProducts = products.filter((p) => {
    if (p.price < minPrice || p.price > maxPrice) return false;
    if (inStockOnly && p.stock <= 0) return false;
    return true;
  }).sort((a, b) => {
    if (sortBy === 'price_asc') return a.price - b.price;
    if (sortBy === 'price_desc') return b.price - a.price;
    if (sortBy === 'rating_desc') return (b.rating || 0) - (a.rating || 0);
    if (sortBy === 'sales_desc') return (b.sales_count || 0) - (a.sales_count || 0);
    return 0;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
      {/* Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 mb-6 border-b border-slate-200 dark:border-slate-800 gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
            {queryParam ? `Search Results for "${queryParam}"` : selectedCategory ? `Department: ${selectedCategory}` : 'Catalog'}
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
            Showing {filteredProducts.length} verified products
          </p>
        </div>

        {/* Sort selector */}
        <div className="flex items-center gap-2">
          <ArrowUpDown className="w-4 h-4 text-slate-400" />
          <span className="text-xs font-semibold text-slate-600 dark:text-slate-300">Sort by:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-semibold text-slate-800 dark:text-slate-200 px-3 py-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="rating_desc">Highest Rated</option>
            <option value="sales_desc">Most Popular</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
          </select>
        </div>
      </div>

      {/* AI Parsed Intent Callout if active */}
      {parsedIntent && (
        <div className="mb-6 p-4 rounded-2xl bg-indigo-50/80 dark:bg-indigo-950/40 border border-indigo-200/80 dark:border-indigo-900/60 flex items-center justify-between flex-wrap gap-3">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-indigo-600 dark:text-indigo-400 flex-shrink-0" />
            <div>
              <span className="text-xs font-bold text-indigo-900 dark:text-indigo-200">
                AI Semantic Intent Extracted:
              </span>
              <div className="flex flex-wrap gap-2 mt-1 text-xs">
                {parsedIntent.extracted_brand && (
                  <span className="px-2 py-0.5 rounded-md bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-indigo-200 dark:border-indigo-800">
                    Brand: <b>{parsedIntent.extracted_brand}</b>
                  </span>
                )}
                {parsedIntent.extracted_category && (
                  <span className="px-2 py-0.5 rounded-md bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-indigo-200 dark:border-indigo-800">
                    Category: <b>{parsedIntent.extracted_category}</b>
                  </span>
                )}
                {parsedIntent.max_price && (
                  <span className="px-2 py-0.5 rounded-md bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-indigo-200 dark:border-indigo-800">
                    Budget ceiling: <b>${parsedIntent.max_price}</b>
                  </span>
                )}
              </div>
            </div>
          </div>
          <button
            onClick={() => {
              setSearchParams({});
              setParsedIntent(null);
            }}
            className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1"
          >
            Clear Filter <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* Main Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Left Filter Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-6">
            <div className="flex items-center justify-between font-bold text-sm text-slate-800 dark:text-slate-200">
              <span className="flex items-center gap-2">
                <SlidersHorizontal className="w-4 h-4 text-indigo-500" /> Filters
              </span>
              {(selectedCategory || minPrice > 0 || maxPrice < 2000 || inStockOnly) && (
                <button
                  onClick={() => {
                    setSelectedCategory('');
                    setMinPrice(0);
                    setMaxPrice(2000);
                    setInStockOnly(false);
                    setSearchParams({});
                  }}
                  className="text-xs text-rose-500 hover:underline font-normal"
                >
                  Reset all
                </button>
              )}
            </div>

            {/* Categories */}
            <div>
              <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-3">
                Department
              </h3>
              <div className="space-y-1.5">
                <button
                  onClick={() => {
                    setSelectedCategory('');
                    setSearchParams({});
                  }}
                  className={`w-full text-left px-3 py-1.5 rounded-xl text-xs font-semibold transition-colors flex items-center justify-between ${
                    !selectedCategory
                      ? 'bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                  }`}
                >
                  <span>All Categories</span>
                  {!selectedCategory && <Check className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />}
                </button>
                {categories.map((cat) => {
                  const isSelected = selectedCategory === cat.slug;
                  return (
                    <button
                      key={cat.id}
                      onClick={() => {
                        setSelectedCategory(cat.slug);
                        setSearchParams({ category: cat.slug });
                      }}
                      className={`w-full text-left px-3 py-1.5 rounded-xl text-xs font-semibold transition-colors flex items-center justify-between ${
                        isSelected
                          ? 'bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400'
                          : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                      }`}
                    >
                      <span>{cat.name}</span>
                      {isSelected && <Check className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Price Filter */}
            <div>
              <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-3">
                Price Ceiling: ${maxPrice}
              </h3>
              <input
                type="range"
                min="0"
                max="2000"
                step="50"
                value={maxPrice}
                onChange={(e) => setMaxPrice(Number(e.target.value))}
                className="w-full accent-indigo-600 cursor-pointer"
              />
              <div className="flex justify-between text-[11px] text-slate-400 mt-1">
                <span>$0</span>
                <span>$1000</span>
                <span>$2000+</span>
              </div>
            </div>

            {/* Stock Availability */}
            <div className="pt-4 border-t border-slate-100 dark:border-slate-800">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={inStockOnly}
                  onChange={(e) => setInStockOnly(e.target.checked)}
                  className="rounded text-indigo-600 focus:ring-indigo-500 w-4 h-4"
                />
                <span className="text-xs font-medium text-slate-700 dark:text-slate-300">
                  In Stock Only
                </span>
              </label>
            </div>
          </div>
        </div>

        {/* Products Grid */}
        <div className="lg:col-span-3">
          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="h-80 bg-slate-100 dark:bg-slate-800 animate-pulse rounded-2xl" />
              ))}
            </div>
          ) : filteredProducts.length === 0 ? (
            <div className="p-12 text-center rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
              <Filter className="w-10 h-10 mx-auto text-slate-400 mb-3" />
              <h3 className="text-base font-bold text-slate-800 dark:text-slate-200">
                No matching products found
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-sm mx-auto">
                Try expanding your price range, clearing category filters, or searching for broader terms.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
              {filteredProducts.map((p) => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
