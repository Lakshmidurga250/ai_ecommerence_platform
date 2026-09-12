import React, { useState, useEffect, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  Filter, SlidersHorizontal, ArrowUpDown, Sparkles, X, Check, Star, 
  ChevronLeft, ChevronRight, RotateCcw, Tag
} from 'lucide-react';
import { Product, Category, Brand } from '../types';
import { api } from '../services/api';
import { ProductCard } from '../components/ProductCard';

export const ProductListPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const queryParam = searchParams.get('q') || '';
  const categoryParam = searchParams.get('category') || '';
  const brandParam = searchParams.get('brand') || '';

  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [brands, setBrands] = useState<Brand[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  
  // Filtering States
  const [selectedCategory, setSelectedCategory] = useState<string>(categoryParam);
  const [selectedBrand, setSelectedBrand] = useState<string>(brandParam);
  const [minPrice, setMinPrice] = useState<number>(0);
  const [maxPrice, setMaxPrice] = useState<number>(220000);
  const [minRating, setMinRating] = useState<number>(0);
  const [inStockOnly, setInStockOnly] = useState<boolean>(false);
  const [sortBy, setSortBy] = useState<string>('featured');
  const [parsedIntent, setParsedIntent] = useState<any>(null);

  // Pagination States
  const [currentPage, setCurrentPage] = useState<number>(1);
  const itemsPerPage = 18;

  // Fetch Taxonomy
  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        const [cats, brs] = await Promise.all([
          api.getCategories().catch(() => []),
          api.getBrands().catch(() => [])
        ]);
        setCategories(cats);
        setBrands(brs);
      } catch (err) {
        console.error('Failed to fetch taxonomy:', err);
      }
    };
    fetchMetadata();
  }, []);

  // Sync with URL parameters
  useEffect(() => {
    setSelectedCategory(categoryParam);
    setSelectedBrand(brandParam);
    setCurrentPage(1);
  }, [categoryParam, brandParam]);

  // Fetch Catalog from Backend
  useEffect(() => {
    const fetchCatalog = async () => {
      setLoading(true);
      try {
        if (queryParam) {
          api.parseSearchIntent(queryParam).then((intent) => {
            setParsedIntent(intent);
          }).catch(() => {});

          const res = await api.searchProducts(queryParam);
          setProducts(res);
        } else {
          setParsedIntent(null);
          const params: Record<string, any> = { limit: 250 };
          if (selectedCategory) params['category'] = selectedCategory;
          if (selectedBrand) params['brand'] = selectedBrand;
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
  }, [queryParam, selectedCategory, selectedBrand]);

  // Client-side filtering & sorting
  const filteredProducts = useMemo(() => {
    return products.filter((p) => {
      // Category filter (if loaded in bulk)
      if (selectedCategory && p.category?.slug !== selectedCategory && p.category?.name !== selectedCategory) {
        return false;
      }
      // Brand filter
      if (selectedBrand && p.brand?.slug !== selectedBrand && p.brand?.name !== selectedBrand) {
        return false;
      }
      // Price range
      if (p.price < minPrice || p.price > maxPrice) return false;
      // Minimum rating
      if (minRating > 0 && (p.rating || 0) < minRating) return false;
      // Stock availability
      if (inStockOnly && p.stock <= 0) return false;
      return true;
    }).sort((a, b) => {
      if (sortBy === 'price_asc') return a.price - b.price;
      if (sortBy === 'price_desc') return b.price - a.price;
      if (sortBy === 'rating_desc') return (b.rating || 0) - (a.rating || 0);
      if (sortBy === 'sales_desc') return (b.sales_count || 0) - (a.sales_count || 0);
      if (sortBy === 'discount_desc') return (b.discount_percent || 0) - (a.discount_percent || 0);
      if (sortBy === 'newest') return (new Date(b.created_at || '').getTime()) - (new Date(a.created_at || '').getTime());
      // Default: featured descending, then rating descending
      return ((b.is_featured ? 1 : 0) - (a.is_featured ? 1 : 0)) || ((b.rating || 0) - (a.rating || 0));
    });
  }, [products, selectedCategory, selectedBrand, minPrice, maxPrice, minRating, inStockOnly, sortBy]);

  // Reset page when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [selectedCategory, selectedBrand, minPrice, maxPrice, minRating, inStockOnly, sortBy, queryParam]);

  // Paginated View
  const totalPages = Math.max(1, Math.ceil(filteredProducts.length / itemsPerPage));
  const paginatedProducts = useMemo(() => {
    const start = (currentPage - 1) * itemsPerPage;
    return filteredProducts.slice(start, start + itemsPerPage);
  }, [filteredProducts, currentPage, itemsPerPage]);

  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleResetAll = () => {
    setSelectedCategory('');
    setSelectedBrand('');
    setMinPrice(0);
    setMaxPrice(220000);
    setMinRating(0);
    setInStockOnly(false);
    setSortBy('featured');
    setSearchParams({});
    setParsedIntent(null);
  };

  const hasActiveFilters = Boolean(
    selectedCategory || selectedBrand || minPrice > 0 || maxPrice < 220000 || minRating > 0 || inStockOnly
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">
      {/* Top Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 mb-6 border-b border-slate-200 dark:border-slate-800 gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            {queryParam 
              ? `Search Results for "${queryParam}"` 
              : selectedCategory 
                ? `${categories.find(c => c.slug === selectedCategory)?.name || selectedCategory}` 
                : 'Marketplace Catalog'}
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
            {filteredProducts.length > 0 
              ? `Showing ${(currentPage - 1) * itemsPerPage + 1}–${Math.min(currentPage * itemsPerPage, filteredProducts.length)} of ${filteredProducts.length} verified products`
              : '0 products found'}
          </p>
        </div>

        {/* Sort Selector */}
        <div className="flex items-center gap-2">
          <ArrowUpDown className="w-4 h-4 text-slate-400" />
          <span className="text-xs font-semibold text-slate-600 dark:text-slate-300">Sort by:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-semibold text-slate-800 dark:text-slate-200 px-3 py-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm"
          >
            <option value="featured">Featured & Best Matches</option>
            <option value="rating_desc">Highest Customer Rating</option>
            <option value="sales_desc">Most Popular (Best Sellers)</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="discount_desc">Biggest Discounts</option>
            <option value="newest">Newest Arrivals</option>
          </select>
        </div>
      </div>

      {/* AI Parsed Intent Callout if active */}
      {parsedIntent && (
        <div className="mb-6 p-4 rounded-2xl bg-indigo-50/80 dark:bg-indigo-950/40 border border-indigo-200/80 dark:border-indigo-900/60 flex items-center justify-between flex-wrap gap-3 shadow-sm">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-indigo-600 dark:text-indigo-400 flex-shrink-0" />
            <div>
              <span className="text-xs font-bold text-indigo-900 dark:text-indigo-200">
                AI Semantic Intent Extracted:
              </span>
              <div className="flex flex-wrap gap-2 mt-1 text-xs">
                {parsedIntent.extracted_brand && (
                  <span className="px-2.5 py-0.5 rounded-md bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-indigo-200 dark:border-indigo-800 font-medium">
                    Brand: <b>{parsedIntent.extracted_brand}</b>
                  </span>
                )}
                {parsedIntent.extracted_category && (
                  <span className="px-2.5 py-0.5 rounded-md bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-indigo-200 dark:border-indigo-800 font-medium">
                    Category: <b>{parsedIntent.extracted_category}</b>
                  </span>
                )}
                {parsedIntent.max_price && (
                  <span className="px-2.5 py-0.5 rounded-md bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-indigo-200 dark:border-indigo-800 font-medium">
                    Budget ceiling: <b>₹{Number(parsedIntent.max_price).toLocaleString('en-IN')}</b>
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

      {/* Active Filter Chips */}
      {hasActiveFilters && (
        <div className="flex flex-wrap items-center gap-2 mb-6 text-xs">
          <span className="font-semibold text-slate-400">Active Filters:</span>
          {selectedCategory && (
            <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 font-medium border border-indigo-200 dark:border-indigo-800">
              Department: {categories.find(c => c.slug === selectedCategory)?.name || selectedCategory}
              <X 
                className="w-3.5 h-3.5 cursor-pointer hover:text-indigo-900" 
                onClick={() => {
                  setSelectedCategory('');
                  const newParams = new URLSearchParams(searchParams);
                  newParams.delete('category');
                  setSearchParams(newParams);
                }} 
              />
            </span>
          )}
          {selectedBrand && (
            <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 font-medium border border-indigo-200 dark:border-indigo-800">
              Brand: {brands.find(b => b.slug === selectedBrand)?.name || selectedBrand}
              <X 
                className="w-3.5 h-3.5 cursor-pointer hover:text-indigo-900" 
                onClick={() => {
                  setSelectedBrand('');
                  const newParams = new URLSearchParams(searchParams);
                  newParams.delete('brand');
                  setSearchParams(newParams);
                }} 
              />
            </span>
          )}
          {maxPrice < 220000 && (
            <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-medium border border-slate-200 dark:border-slate-700">
              Under ₹{maxPrice.toLocaleString('en-IN')}
              <X className="w-3.5 h-3.5 cursor-pointer hover:text-slate-900" onClick={() => setMaxPrice(220000)} />
            </span>
          )}
          {minRating > 0 && (
            <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 font-medium border border-amber-200 dark:border-amber-800">
              {minRating}★ & above
              <X className="w-3.5 h-3.5 cursor-pointer hover:text-amber-900" onClick={() => setMinRating(0)} />
            </span>
          )}
          {inStockOnly && (
            <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 font-medium border border-emerald-200 dark:border-emerald-800">
              In Stock Only
              <X className="w-3.5 h-3.5 cursor-pointer hover:text-emerald-900" onClick={() => setInStockOnly(false)} />
            </span>
          )}
          <button
            onClick={handleResetAll}
            className="text-rose-500 hover:text-rose-600 font-semibold ml-2 underline"
          >
            Clear all
          </button>
        </div>
      )}

      {/* Main Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Left Filter Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-6 sticky top-24">
            <div className="flex items-center justify-between font-bold text-sm text-slate-800 dark:text-slate-200">
              <span className="flex items-center gap-2">
                <SlidersHorizontal className="w-4 h-4 text-indigo-500" /> Filters
              </span>
              {hasActiveFilters && (
                <button
                  onClick={handleResetAll}
                  className="text-xs text-rose-500 hover:underline font-medium flex items-center gap-1"
                >
                  <RotateCcw className="w-3 h-3" /> Reset all
                </button>
              )}
            </div>

            {/* Departments */}
            <div>
              <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-3">
                Department
              </h3>
              <div className="space-y-1 max-h-56 overflow-y-auto pr-1">
                <button
                  onClick={() => {
                    setSelectedCategory('');
                    const newParams = new URLSearchParams(searchParams);
                    newParams.delete('category');
                    setSearchParams(newParams);
                  }}
                  className={`w-full text-left px-3 py-2 rounded-xl text-xs font-semibold transition-colors flex items-center justify-between ${
                    !selectedCategory
                      ? 'bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 font-bold'
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
                        const newParams = new URLSearchParams(searchParams);
                        newParams.set('category', cat.slug);
                        setSearchParams(newParams);
                      }}
                      className={`w-full text-left px-3 py-2 rounded-xl text-xs font-semibold transition-colors flex items-center justify-between ${
                        isSelected
                          ? 'bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 font-bold'
                          : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                      }`}
                    >
                      <span className="truncate">{cat.name}</span>
                      {isSelected && <Check className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Brands */}
            <div className="pt-4 border-t border-slate-100 dark:border-slate-800">
              <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-3 flex items-center justify-between">
                <span>Brand</span>
                {selectedBrand && (
                  <button onClick={() => setSelectedBrand('')} className="text-[10px] text-indigo-500 font-normal hover:underline">
                    Clear
                  </button>
                )}
              </h3>
              <div className="space-y-1 max-h-48 overflow-y-auto pr-1">
                {brands.map((b) => {
                  const isSelected = selectedBrand === b.slug;
                  return (
                    <button
                      key={b.id}
                      onClick={() => setSelectedBrand(isSelected ? '' : b.slug)}
                      className={`w-full text-left px-3 py-1.5 rounded-lg text-xs transition-colors flex items-center justify-between ${
                        isSelected
                          ? 'bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 font-bold'
                          : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                      }`}
                    >
                      <span>{b.name}</span>
                      {isSelected && <Check className="w-3.5 h-3.5 text-indigo-600" />}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Price Filter Slider */}
            <div className="pt-4 border-t border-slate-100 dark:border-slate-800">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                  Price Ceiling
                </h3>
                <span className="text-xs font-extrabold text-indigo-600 dark:text-indigo-400">
                  ₹{maxPrice.toLocaleString('en-IN')}
                </span>
              </div>
              <input
                type="range"
                min="500"
                max="220000"
                step="1000"
                value={maxPrice}
                onChange={(e) => setMaxPrice(Number(e.target.value))}
                className="w-full accent-indigo-600 cursor-pointer h-1.5 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none"
              />
              <div className="flex justify-between text-[11px] text-slate-400 mt-1.5 font-mono">
                <span>₹500</span>
                <span>₹50,000</span>
                <span>₹2,20,000</span>
              </div>
            </div>

            {/* Customer Rating Filter */}
            <div className="pt-4 border-t border-slate-100 dark:border-slate-800">
              <h3 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-2">
                Customer Rating
              </h3>
              <div className="space-y-1">
                {[
                  { label: '4★ & above', val: 4.0 },
                  { label: '3★ & above', val: 3.0 },
                  { label: 'All Ratings', val: 0.0 }
                ].map((item) => (
                  <button
                    key={item.val}
                    onClick={() => setMinRating(item.val)}
                    className={`w-full text-left px-3 py-1.5 rounded-lg text-xs flex items-center justify-between ${
                      minRating === item.val
                        ? 'bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 font-bold'
                        : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                    }`}
                  >
                    <span className="flex items-center gap-1.5">
                      {item.val > 0 && <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />}
                      {item.label}
                    </span>
                    {minRating === item.val && <Check className="w-3.5 h-3.5" />}
                  </button>
                ))}
              </div>
            </div>

            {/* Stock Availability */}
            <div className="pt-4 border-t border-slate-100 dark:border-slate-800">
              <label className="flex items-center gap-2.5 cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={inStockOnly}
                  onChange={(e) => setInStockOnly(e.target.checked)}
                  className="rounded text-indigo-600 focus:ring-indigo-500 w-4 h-4 cursor-pointer"
                />
                <span className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                  In Stock Only
                </span>
              </label>
            </div>
          </div>
        </div>

        {/* Products Grid & Pagination */}
        <div className="lg:col-span-3 flex flex-col">
          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="h-96 bg-slate-100 dark:bg-slate-800/60 animate-pulse rounded-2xl border border-slate-200 dark:border-slate-800" />
              ))}
            </div>
          ) : filteredProducts.length === 0 ? (
            <div className="p-16 text-center rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 my-auto shadow-sm">
              <Filter className="w-12 h-12 mx-auto text-slate-300 dark:text-slate-600 mb-4" />
              <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                No matching products found
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-2 max-w-sm mx-auto">
                No items match your current filter combination. Try expanding the price ceiling, selecting a different department, or clearing brand filters.
              </p>
              <button
                onClick={handleResetAll}
                className="mt-6 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition-colors shadow-md inline-flex items-center gap-1.5"
              >
                <RotateCcw className="w-3.5 h-3.5" /> Reset all filters
              </button>
            </div>
          ) : (
            <>
              {/* Product Cards Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
                {paginatedProducts.map((p) => (
                  <ProductCard key={p.id} product={p} />
                ))}
              </div>

              {/* Pagination Controls */}
              {totalPages > 1 && (
                <div className="mt-12 flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 border-t border-slate-200 dark:border-slate-800">
                  <div className="text-xs text-slate-500 dark:text-slate-400">
                    Page <span className="font-bold text-slate-800 dark:text-slate-200">{currentPage}</span> of{' '}
                    <span className="font-bold text-slate-800 dark:text-slate-200">{totalPages}</span>
                  </div>

                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={() => handlePageChange(currentPage - 1)}
                      disabled={currentPage === 1}
                      className="p-2 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                      title="Previous page"
                    >
                      <ChevronLeft className="w-4 h-4" />
                    </button>

                    {/* Page Numbers */}
                    {Array.from({ length: totalPages }, (_, i) => i + 1)
                      .filter(page => page === 1 || page === totalPages || Math.abs(page - currentPage) <= 1)
                      .map((page, idx, array) => {
                        const showEllipsis = idx > 0 && page - array[idx - 1] > 1;
                        return (
                          <React.Fragment key={page}>
                            {showEllipsis && <span className="px-1 text-slate-400 text-xs">...</span>}
                            <button
                              onClick={() => handlePageChange(page)}
                              className={`w-8 h-8 rounded-xl text-xs font-bold transition-colors ${
                                currentPage === page
                                  ? 'bg-indigo-600 text-white shadow-md'
                                  : 'border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
                              }`}
                            >
                              {page}
                            </button>
                          </React.Fragment>
                        );
                      })}

                    <button
                      onClick={() => handlePageChange(currentPage + 1)}
                      disabled={currentPage === totalPages}
                      className="p-2 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
                      title="Next page"
                    >
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};
