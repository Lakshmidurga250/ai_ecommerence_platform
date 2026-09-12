import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, ShoppingBag, Star, Crown, ArrowRight, Zap, Gift } from 'lucide-react';
import { api } from '../services/api';
import { NextBestAction } from '../types';

interface NextBestActionBannerProps {
  userId?: number;
}

export const NextBestActionBanner: React.FC<NextBestActionBannerProps> = ({ userId = 1 }) => {
  const [nba, setNba] = useState<NextBestAction | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadNextAction();
  }, [userId]);

  const loadNextAction = async () => {
    try {
      setLoading(true);
      const data = await api.getNextBestAction(userId);
      setNba(data);
    } catch (err) {
      console.error('Failed to load Next-Best-Action:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !nba) return null;

  const getTheme = (type: string) => {
    switch (type) {
      case 'ABANDONED_CART_DISCOUNT':
        return {
          bg: 'bg-gradient-to-r from-amber-500 via-orange-500 to-rose-500',
          icon: <ShoppingBag className="w-5 h-5 text-white" />,
          badge: 'Exclusive Offer'
        };
      case 'REQUEST_VERIFIED_REVIEW':
        return {
          bg: 'bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600',
          icon: <Star className="w-5 h-5 text-amber-300" />,
          badge: 'Reward Points'
        };
      case 'LOYALTY_TIER_NUDGE':
        return {
          bg: 'bg-gradient-to-r from-purple-600 via-fuchsia-600 to-pink-600',
          icon: <Crown className="w-5 h-5 text-amber-300" />,
          badge: 'VIP Upgrade'
        };
      case 'CROSS_SELL_ACCESSORY':
        return {
          bg: 'bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600',
          icon: <Sparkles className="w-5 h-5 text-white" />,
          badge: 'Recommended Pairing'
        };
      default:
        return {
          bg: 'bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900',
          icon: <Zap className="w-5 h-5 text-indigo-400" />,
          badge: 'Curated For You'
        };
    }
  };

  const theme = getTheme(nba.action_type);

  return (
    <div className={`relative overflow-hidden rounded-2xl ${theme.bg} p-4 sm:p-5 text-white shadow-lg my-4`}>
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 relative z-10">
        <div className="flex items-center gap-3.5">
          <div className="p-2.5 rounded-xl bg-white/20 backdrop-blur-md shadow-inner flex-shrink-0">
            {theme.icon}
          </div>
          <div>
            <div className="flex items-center gap-2 mb-0.5">
              <span className="text-[10px] font-black uppercase tracking-wider bg-white/20 px-2 py-0.5 rounded-full">
                {theme.badge}
              </span>
              <span className="text-xs text-white/80 font-medium">
                AI Next-Best-Action • {Math.round(nba.confidence * 100)}% match
              </span>
            </div>
            <h4 className="text-base font-bold leading-snug">{nba.headline}</h4>
            <p className="text-xs text-white/90 line-clamp-1 mt-0.5">{nba.description}</p>
          </div>
        </div>

        <button
          onClick={() => navigate(nba.target_route)}
          className="inline-flex items-center gap-2 whitespace-nowrap px-4 py-2.5 rounded-xl bg-white text-slate-900 font-bold text-xs hover:bg-slate-100 transition-all shadow-md active:scale-95"
        >
          {nba.cta_label}
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
