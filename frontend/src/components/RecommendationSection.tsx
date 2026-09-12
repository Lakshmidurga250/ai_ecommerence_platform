import React, { useState, useEffect } from 'react';
import { Sparkles, Cpu, Layers, Flame, Users, Network } from 'lucide-react';
import { RecommendationItem } from '../types';
import { api } from '../services/api';
import { ProductCard } from './ProductCard';

interface RecommendationSectionProps {
  productId?: number;
  title?: string;
  defaultStrategy?: 'HYBRID' | 'POPULARITY' | 'CONTENT_BASED' | 'COLLABORATIVE' | 'MATRIX_FACTORIZATION';
}

const STRATEGIES = [
  { id: 'HYBRID', label: 'Hybrid AI Ensemble', icon: Sparkles, desc: 'Weighted multi-model recommender combining behavioral and contextual signals' },
  { id: 'POPULARITY', label: 'Bayesian Trending', icon: Flame, desc: 'Bayesian-dampened popularity with recency decay' },
  { id: 'CONTENT_BASED', label: 'Attribute Cosine', icon: Layers, desc: 'TF-IDF cosine similarity across catalog specifications and tags' },
  { id: 'COLLABORATIVE', label: 'Collaborative Filter', icon: Users, desc: 'User-user neighborhood interaction affinity matrix' },
  { id: 'MATRIX_FACTORIZATION', label: 'Latent Matrix', icon: Network, desc: 'Low-rank matrix decomposition of customer preference vectors' },
];

export const RecommendationSection: React.FC<RecommendationSectionProps> = ({
  productId,
  title = 'AI-Powered Recommendations For You',
  defaultStrategy = 'HYBRID',
}) => {
  const [selectedStrategy, setSelectedStrategy] = useState<string>(defaultStrategy);
  const [items, setItems] = useState<RecommendationItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    const fetchRecommendations = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await api.getRecommendations(selectedStrategy, productId);
        if (isMounted) {
          setItems(res);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err.message || 'Failed to fetch recommendations');
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchRecommendations();
    return () => {
      isMounted = false;
    };
  }, [selectedStrategy, productId]);

  const activeStrategyObj = STRATEGIES.find((s) => s.id === selectedStrategy) || STRATEGIES[0];

  return (
    <section className="py-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 text-xs font-bold tracking-wider uppercase mb-2">
            <Cpu className="w-3.5 h-3.5" /> 5-Tier ML Recommendation Engine
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            {title}
          </h2>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
            {activeStrategyObj.desc}
          </p>
        </div>

        {/* Strategy Switcher Pills */}
        <div className="flex flex-wrap gap-2 bg-slate-100 dark:bg-slate-800/80 p-1.5 rounded-2xl border border-slate-200 dark:border-slate-700/60 max-w-full overflow-x-auto">
          {STRATEGIES.map((s) => {
            const Icon = s.icon;
            const isActive = selectedStrategy === s.id;
            return (
              <button
                key={s.id}
                onClick={() => setSelectedStrategy(s.id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all duration-200 ${
                  isActive
                    ? 'bg-white dark:bg-slate-900 text-indigo-600 dark:text-indigo-400 shadow-sm border border-slate-200/60 dark:border-slate-700'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-indigo-600 dark:text-indigo-400' : 'text-slate-400'}`} />
                {s.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Content State */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <div
              key={i}
              className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 animate-pulse flex flex-col gap-4"
            >
              <div className="w-full aspect-square bg-slate-200 dark:bg-slate-800 rounded-xl" />
              <div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-3/4" />
              <div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-1/2" />
              <div className="h-8 bg-slate-200 dark:bg-slate-800 rounded-xl mt-auto" />
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="p-8 text-center rounded-2xl bg-rose-50 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/40 text-rose-600 dark:text-rose-400">
          <p className="text-sm font-medium">{error}</p>
        </div>
      ) : items.length === 0 ? (
        <div className="p-12 text-center rounded-2xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800">
          <Sparkles className="w-8 h-8 mx-auto text-slate-400 mb-2" />
          <p className="text-sm text-slate-500 dark:text-slate-400 font-medium">
            No personalized recommendations for this criteria yet.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {items.map((item) => (
            <ProductCard
              key={item.product.id}
              product={item.product}
              explanation={item.explanation}
              matchScore={item.score}
              badge={item.model_type}
            />
          ))}
        </div>
      )}
    </section>
  );
};
