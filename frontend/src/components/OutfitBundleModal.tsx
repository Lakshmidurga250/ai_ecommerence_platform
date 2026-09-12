import React, { useState, useEffect } from 'react';
import { Sparkles, ShoppingBag, Check, Plus, ArrowRight, Tag, ShieldCheck } from 'lucide-react';
import { api } from '../services/api';
import { OutfitBundle } from '../types';

interface OutfitBundleModalProps {
  productId: number;
  productName: string;
  isOpen: boolean;
  onClose: () => void;
  onAddBundleToCart?: (productIds: number[]) => void;
}

export const OutfitBundleModal: React.FC<OutfitBundleModalProps> = ({
  productId,
  productName,
  isOpen,
  onClose,
  onAddBundleToCart,
}) => {
  const [bundle, setBundle] = useState<OutfitBundle | null>(null);
  const [loading, setLoading] = useState(false);
  const [added, setAdded] = useState(false);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);

  useEffect(() => {
    if (isOpen && productId) {
      loadOutfit();
    }
  }, [isOpen, productId]);

  const loadOutfit = async () => {
    try {
      setLoading(true);
      const data = await api.getProductOutfit(productId, 3, 12.0);
      setBundle(data);
      if (data?.items) {
        setSelectedIds(data.items.map(i => i.id));
      }
    } catch (err) {
      console.error('Failed to load outfit bundle:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  const toggleItem = (id: number) => {
    if (selectedIds.includes(id)) {
      if (selectedIds.length > 1) {
        setSelectedIds(selectedIds.filter(i => i !== id));
      }
    } else {
      setSelectedIds([...selectedIds, id]);
    }
  };

  const handleAddToCart = () => {
    if (onAddBundleToCart) {
      onAddBundleToCart(selectedIds);
    }
    setAdded(true);
    setTimeout(() => {
      setAdded(false);
      onClose();
    }, 1500);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="relative w-full max-w-2xl rounded-2xl bg-white shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="bg-gradient-to-r from-violet-600 via-indigo-600 to-blue-600 p-6 text-white">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-lg bg-white/20 backdrop-blur-md">
                <Sparkles className="w-5 h-5 text-amber-300" />
              </div>
              <div>
                <h3 className="font-bold text-lg">AI Outfit & Setup Generator</h3>
                <p className="text-xs text-white/80">Style Compatibility & Ecosystem Pairing</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="rounded-full p-1.5 text-white/80 hover:bg-white/10 hover:text-white transition-colors"
            >
              ✕
            </button>
          </div>
          {bundle && (
            <div className="mt-3 inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/15 text-xs font-medium backdrop-blur-sm">
              <Tag className="w-3.5 h-3.5 text-amber-300" />
              {bundle.theme_title}
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-6">
          {loading ? (
            <div className="py-12 text-center text-slate-500">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-indigo-600 border-t-transparent mb-2"></div>
              <p className="text-sm font-medium">Synthesizing compatible combination...</p>
            </div>
          ) : bundle ? (
            <div className="space-y-6">
              {/* Product Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {bundle.items.map((item, idx) => {
                  const isSelected = selectedIds.includes(item.id);
                  return (
                    <div
                      key={item.id}
                      onClick={() => toggleItem(item.id)}
                      className={`relative cursor-pointer rounded-xl border p-3 transition-all ${
                        isSelected
                          ? 'border-indigo-600 bg-indigo-50/40 shadow-sm'
                          : 'border-slate-200 bg-slate-50/50 opacity-60'
                      }`}
                    >
                      <div className="absolute top-2 right-2 z-10">
                        <div
                          className={`w-5 h-5 rounded-full flex items-center justify-center text-xs ${
                            isSelected ? 'bg-indigo-600 text-white' : 'border border-slate-300 bg-white'
                          }`}
                        >
                          {isSelected && <Check className="w-3 h-3" />}
                        </div>
                      </div>

                      <div className="h-28 w-full rounded-lg bg-white overflow-hidden mb-2 flex items-center justify-center p-2">
                        <img
                          src={item.image_url || 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400'}
                          alt={item.name}
                          className="h-full object-contain"
                        />
                      </div>

                      <span className="inline-block text-[10px] font-semibold text-indigo-700 uppercase tracking-wide bg-indigo-100/60 px-1.5 py-0.5 rounded mb-1">
                        {item.role}
                      </span>
                      <h4 className="text-xs font-semibold text-slate-800 line-clamp-2 leading-tight">
                        {item.name}
                      </h4>
                      <p className="mt-1 font-bold text-sm text-slate-900">
                        ₹{item.price.toLocaleString('en-IN')}
                      </p>
                    </div>
                  );
                })}
              </div>

              {/* Pricing & Savings Banner */}
              <div className="rounded-xl bg-slate-900 p-4 text-white flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-400 line-through">
                      ₹{bundle.original_total_price.toLocaleString('en-IN')}
                    </span>
                    <span className="rounded bg-emerald-500/20 px-2 py-0.5 text-xs font-semibold text-emerald-400">
                      Save {bundle.bundle_discount_pct}%
                    </span>
                  </div>
                  <div className="text-2xl font-black text-white">
                    ₹{bundle.bundle_price.toLocaleString('en-IN')}
                  </div>
                  <p className="text-[11px] text-emerald-300">
                    Instant savings of ₹{bundle.total_savings.toLocaleString('en-IN')} applied
                  </p>
                </div>

                <button
                  onClick={handleAddToCart}
                  disabled={added || selectedIds.length === 0}
                  className={`inline-flex items-center gap-2 px-5 py-3 rounded-xl font-semibold text-sm transition-all shadow-lg ${
                    added
                      ? 'bg-emerald-600 text-white'
                      : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-600/30'
                  }`}
                >
                  {added ? (
                    <>
                      <Check className="w-4 h-4" />
                      Bundle Added!
                    </>
                  ) : (
                    <>
                      <ShoppingBag className="w-4 h-4" />
                      Add Complete Outfit
                    </>
                  )}
                </button>
              </div>
            </div>
          ) : (
            <p className="text-center text-slate-500 py-6 text-sm">No complementary items available.</p>
          )}
        </div>
      </div>
    </div>
  );
};
