import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowUpRight, Plus, Check, Sparkles, TrendingUp, ShieldCheck } from 'lucide-react';
import { api } from '../services/api';
import { CrossSellResponse, UpsellResponse } from '../types';

interface CrossSellUpsellSectionProps {
  productId: number;
  productName: string;
  onAddToCart?: (productId: number) => void;
}

export const CrossSellUpsellSection: React.FC<CrossSellUpsellSectionProps> = ({
  productId,
  productName,
  onAddToCart,
}) => {
  const [activeTab, setActiveTab] = useState<'CROSS_SELL' | 'UPSELL'>('CROSS_SELL');
  const [crossSells, setCrossSells] = useState<CrossSellResponse | null>(null);
  const [upsells, setUpsells] = useState<UpsellResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (productId) {
      loadRecommendations();
    }
  }, [productId]);

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      const [crossData, upData] = await Promise.all([
        api.getCrossSells(productId, 3).catch(() => null),
        api.getUpsells(productId, 3).catch(() => null),
      ]);
      setCrossSells(crossData);
      setUpsells(upData);
    } catch (err) {
      console.error('Failed to load cross/upsell recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const hasCrossSells = crossSells?.cross_sell_items && crossSells.cross_sell_items.length > 0;
  const hasUpsells = upsells?.upsell_alternatives && upsells.upsell_alternatives.length > 0;

  if (!hasCrossSells && !hasUpsells) return null;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm my-8">
      {/* Tab Switcher */}
      <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-6">
        <div className="flex items-center gap-2">
          {hasCrossSells && (
            <button
              onClick={() => setActiveTab('CROSS_SELL')}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold transition-all ${
                activeTab === 'CROSS_SELL'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <Sparkles className="w-4 h-4" />
              Frequently Bought Together
            </button>
          )}

          {hasUpsells && (
            <button
              onClick={() => setActiveTab('UPSELL')}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold transition-all ${
                activeTab === 'UPSELL'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <TrendingUp className="w-4 h-4" />
              Upgrade to Premium
            </button>
          )}
        </div>
      </div>

      {loading ? (
        <div className="py-8 text-center text-slate-400 text-sm">Computing dynamic suggestions...</div>
      ) : activeTab === 'CROSS_SELL' && crossSells ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {crossSells.cross_sell_items.map(item => (
            <div
              key={item.id}
              className="group flex flex-col justify-between rounded-xl border border-slate-200 p-4 transition-all hover:border-indigo-500 hover:shadow-md"
            >
              <div>
                <div className="h-32 w-full rounded-lg bg-slate-50 flex items-center justify-center p-2 mb-3 overflow-hidden">
                  <img
                    src={item.image_url || 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400'}
                    alt={item.name}
                    className="h-full object-contain group-hover:scale-105 transition-transform"
                  />
                </div>
                <div className="flex items-center gap-1.5 mb-1">
                  <span className="text-[10px] font-bold text-emerald-700 bg-emerald-100/70 px-2 py-0.5 rounded-full">
                    {item.co_occurrence_lift}x Co-occurrence
                  </span>
                </div>
                <h4
                  onClick={() => navigate(`/products/${item.slug || item.id}`)}
                  className="font-bold text-sm text-slate-800 line-clamp-2 hover:text-indigo-600 cursor-pointer"
                >
                  {item.name}
                </h4>
                <p className="text-xs text-slate-500 line-clamp-2 mt-1">{item.recommendation_pitch}</p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                <div>
                  <span className="text-xs text-slate-400 block">Add-on Price</span>
                  <span className="font-extrabold text-base text-slate-900">
                    ₹{item.price.toLocaleString('en-IN')}
                  </span>
                </div>
                <button
                  onClick={() => onAddToCart && onAddToCart(item.id)}
                  className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-indigo-50 text-indigo-700 text-xs font-bold hover:bg-indigo-600 hover:text-white transition-colors"
                >
                  <Plus className="w-3.5 h-3.5" />
                  Add
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : activeTab === 'UPSELL' && upsells ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {upsells.upsell_alternatives.map(item => (
            <div
              key={item.id}
              className="group flex flex-col justify-between rounded-xl border border-indigo-100 bg-indigo-50/20 p-4 transition-all hover:border-indigo-500 hover:shadow-md"
            >
              <div>
                <div className="h-32 w-full rounded-lg bg-white flex items-center justify-center p-2 mb-3 overflow-hidden shadow-inner">
                  <img
                    src={item.image_url || 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400'}
                    alt={item.name}
                    className="h-full object-contain group-hover:scale-105 transition-transform"
                  />
                </div>
                <span className="text-[10px] font-bold text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded-full">
                  Flagship Trade-up
                </span>
                <h4
                  onClick={() => navigate(`/products/${item.slug || item.id}`)}
                  className="font-bold text-sm text-slate-800 line-clamp-2 mt-1.5 hover:text-indigo-600 cursor-pointer"
                >
                  {item.name}
                </h4>
                <ul className="mt-2 space-y-1">
                  {item.key_advantages.map((adv, idx) => (
                    <li key={idx} className="text-[11px] text-slate-600 flex items-center gap-1.5">
                      <span className="h-1.5 w-1.5 rounded-full bg-indigo-600 flex-shrink-0" />
                      {adv}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-200 flex items-center justify-between">
                <div>
                  <span className="text-[10px] text-indigo-600 font-bold block">
                    {item.price_delta_pct} (₹{item.price_delta.toLocaleString('en-IN')} diff)
                  </span>
                  <span className="font-extrabold text-base text-slate-900">
                    ₹{item.price.toLocaleString('en-IN')}
                  </span>
                </div>
                <button
                  onClick={() => navigate(`/products/${item.slug || item.id}`)}
                  className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-indigo-600 text-white text-xs font-bold hover:bg-indigo-500 transition-colors"
                >
                  View Spec
                  <ArrowUpRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
};
