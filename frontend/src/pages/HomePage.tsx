import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, ArrowRight, ShieldCheck, Zap, Bot, TrendingUp, Layers } from 'lucide-react';
import { Product, Category } from '../types';
import { api } from '../services/api';
import { ProductCard } from '../components/ProductCard';
import { RecommendationSection } from '../components/RecommendationSection';
import { AIChatAssistantModal } from '../components/AIChatAssistantModal';
import { RecentlyViewedBar } from '../components/RecentlyViewedBar';


export const HomePage: React.FC = () => {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [isAIChatOpen, setIsAIChatOpen] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [prods, cats] = await Promise.all([
          api.getProducts({ is_featured: true, limit: 8 }),
          api.getCategories(),
        ]);
        setFeaturedProducts(prods);
        setCategories(cats);
      } catch (err) {
        console.error('Failed to load home page catalog data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white py-20 lg:py-28 px-4 sm:px-6 lg:px-8">
        {/* Ambient background glow elements */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-indigo-500/15 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 right-10 w-[400px] h-[400px] bg-purple-500/15 rounded-full blur-3xl pointer-events-none" />

        <div className="relative max-w-7xl mx-auto flex flex-col lg:flex-row items-center justify-between gap-12">
          <div className="max-w-2xl text-center lg:text-left">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold mb-6 backdrop-blur-md">
              <Sparkles className="w-4 h-4 text-indigo-400 animate-pulse" />
              <span>Next-Generation Multi-Vendor AI Marketplace</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-tight">
              Intelligent Shopping, <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400">
                Powered by Real ML.
              </span>
            </h1>

            <p className="mt-6 text-base sm:text-lg text-slate-300 leading-relaxed max-w-xl mx-auto lg:mx-0 font-normal">
              Experience dynamic personalization with 5-tier recommendation models, sub-word TF-IDF NLP search, grounded conversational concierges, and verified multi-vendor fulfillment.
            </p>

            <div className="mt-8 flex flex-wrap items-center justify-center lg:justify-start gap-4">
              <Link
                to="/products"
                className="px-6 py-3.5 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm shadow-xl shadow-indigo-600/30 hover:shadow-indigo-500/40 transition-all flex items-center gap-2 group"
              >
                <span>Explore Catalog</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>

              <button
                onClick={() => setIsAIChatOpen(true)}
                className="px-6 py-3.5 rounded-2xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-white font-semibold text-sm backdrop-blur-md transition-all flex items-center gap-2 shadow-lg"
              >
                <Bot className="w-4 h-4 text-purple-400" />
                <span>Ask AI Concierge</span>
              </button>
            </div>

            {/* Micro Stats */}
            <div className="mt-12 pt-8 border-t border-slate-800/80 grid grid-cols-3 gap-6 text-center lg:text-left">
              <div>
                <p className="text-2xl font-extrabold text-white">5-Tier</p>
                <p className="text-xs text-slate-400 mt-0.5">Ensemble ML</p>
              </div>
              <div>
                <p className="text-2xl font-extrabold text-white">0%</p>
                <p className="text-xs text-slate-400 mt-0.5">Mock Data</p>
              </div>
              <div>
                <p className="text-2xl font-extrabold text-white">&lt;10ms</p>
                <p className="text-xs text-slate-400 mt-0.5">Vector Search</p>
              </div>
            </div>
          </div>

          {/* Hero Visual Card */}
          <div className="w-full lg:w-auto relative flex justify-center">
            <div className="w-full max-w-md bg-gradient-to-b from-slate-800/60 to-slate-900/90 border border-slate-700/60 rounded-3xl p-6 backdrop-blur-xl shadow-2xl relative">
              <div className="flex items-center justify-between pb-4 border-b border-slate-800">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-rose-500" />
                  <div className="w-3 h-3 rounded-full bg-amber-500" />
                  <div className="w-3 h-3 rounded-full bg-emerald-500" />
                </div>
                <span className="text-xs text-slate-400 font-mono">ai_engine_active.py</span>
              </div>

              <div className="py-4 space-y-3 font-mono text-xs text-slate-300">
                <div className="flex items-center justify-between text-indigo-400">
                  <span>&gt; Model Pipeline:</span>
                  <span className="text-emerald-400">ONLINE</span>
                </div>
                <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800 space-y-1">
                  <p className="text-slate-400">L1: Bayesian Dampened Popularity</p>
                  <p className="text-slate-400">L2: TF-IDF Cosine Specification Vector</p>
                  <p className="text-slate-400">L3: User Neighborhood Collaborative</p>
                  <p className="text-slate-400">L4: Hybrid Ensemble Explainer</p>
                  <p className="text-slate-400">L5: Latent SVD Factorization</p>
                </div>
                <div className="flex items-center gap-2 text-purple-300 text-[11px]">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Real-time continuous inference pipeline</span>
                </div>
              </div>

              <button
                onClick={() => setIsAIChatOpen(true)}
                className="w-full mt-2 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl text-center text-xs font-bold text-white shadow-md hover:opacity-95 transition-opacity"
              >
                Launch Live Interactive Demonstration
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Bar */}
      <section className="py-8 bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 flex items-center gap-2">
              <Layers className="w-4 h-4 text-indigo-500" /> Browse by Department
            </h3>
            <Link to="/products" className="text-xs font-semibold text-indigo-600 dark:text-indigo-400 hover:underline">
              View All Categories &rarr;
            </Link>
          </div>

          <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-none">
            {categories.map((cat) => (
              <Link
                key={cat.id}
                to={`/products?category=${cat.slug}`}
                className="flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/60 shadow-sm hover:border-indigo-500 dark:hover:border-indigo-500 hover:shadow transition-all flex-shrink-0 text-sm font-semibold text-slate-700 dark:text-slate-200"
              >
                <span>{cat.name}</span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products Grid */}
      <section className="py-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <div className="flex items-end justify-between mb-8">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 dark:bg-amber-950/50 text-amber-600 dark:text-amber-400 text-xs font-bold uppercase tracking-wider mb-2">
              <TrendingUp className="w-3.5 h-3.5" /> Market Highlights
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
              Featured Verified Products
            </h2>
          </div>
          <Link
            to="/products"
            className="text-sm font-semibold text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 flex items-center gap-1"
          >
            <span>Full Catalog</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-80 bg-slate-100 dark:bg-slate-800 animate-pulse rounded-2xl" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {featuredProducts.map((product) => (
              <ProductCard key={product.id} product={product} badge="Featured" />
            ))}
          </div>
        )}
      </section>

      {/* 5-Tier Recommendation Section */}
      <RecommendationSection defaultStrategy="HYBRID" />

      {/* Recently Viewed History */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <RecentlyViewedBar />
      </div>

      {/* Platform Features / Guarantees */}

      <section className="py-16 bg-slate-50 dark:bg-slate-900/50 border-t border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="flex items-start gap-4 p-6 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700/60 shadow-sm">
              <div className="p-3 rounded-xl bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400">
                <Sparkles className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">Grounded AI Intent</h3>
                <p className="mt-1 text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                  Natural language queries parsed into structured brand, budget, and attribute filters with zero hallucination.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4 p-6 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700/60 shadow-sm">
              <div className="p-3 rounded-xl bg-emerald-50 dark:bg-emerald-950/50 text-emerald-600 dark:text-emerald-400">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">Isolation Forest Fraud Shield</h3>
                <p className="mt-1 text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                  Real-time transaction anomaly scoring protecting sellers and buyers on every single checkout.
                </p>
              </div>
            </div>

            <div className="flex items-start gap-4 p-6 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700/60 shadow-sm">
              <div className="p-3 rounded-xl bg-purple-50 dark:bg-purple-950/50 text-purple-600 dark:text-purple-400">
                <Zap className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">Demand Forecasting</h3>
                <p className="mt-1 text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                  Random Forest regressors predict product demand with authentic MAE &amp; RMSE performance tracking.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Floating AI Assistant Trigger Modal */}
      <AIChatAssistantModal isOpen={isAIChatOpen} onClose={() => setIsAIChatOpen(false)} />
    </div>
  );
};
