import React, { useEffect, useState } from 'react';
import { Sparkles, TrendingUp, AlertCircle, Award, Gift, Clock, ShoppingBag, Heart, CheckCircle, RefreshCw } from 'lucide-react';
import { api } from '../services/api';
import { Customer360Profile, LoyaltyProfile } from '../types';

export const Customer360Card: React.FC = () => {
  const [profile, setProfile] = useState<Customer360Profile | null>(null);
  const [loyalty, setLoyalty] = useState<LoyaltyProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [redeeming, setRedeeming] = useState<boolean>(false);
  const [redeemSuccess, setRedeemSuccess] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [pData, lData] = await Promise.all([
        api.getMyCustomer360().catch(() => null),
        api.getMyLoyaltyProfile().catch(() => null),
      ]);
      setProfile(pData);
      setLoyalty(lData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRedeem = async (points: number) => {
    setRedeeming(true);
    setRedeemSuccess(null);
    try {
      const res = await api.redeemLoyaltyPoints(points);
      setRedeemSuccess(res.message || `Successfully redeemed ${points} points!`);
      await loadData();
    } catch (err: any) {
      alert(err.message || 'Redemption failed');
    } finally {
      setRedeeming(false);
    }
  };

  if (loading) {
    return (
      <div className="p-6 bg-slate-50 dark:bg-slate-800/40 rounded-3xl border border-slate-200 dark:border-slate-700 animate-pulse space-y-4 my-6">
        <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded w-1/4"></div>
        <div className="grid grid-cols-4 gap-4">
          <div className="h-20 bg-slate-200 dark:bg-slate-700 rounded-2xl"></div>
          <div className="h-20 bg-slate-200 dark:bg-slate-700 rounded-2xl"></div>
          <div className="h-20 bg-slate-200 dark:bg-slate-700 rounded-2xl"></div>
          <div className="h-20 bg-slate-200 dark:bg-slate-700 rounded-2xl"></div>
        </div>
      </div>
    );
  }

  if (!profile) return null;

  return (
    <div className="mt-8 bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-2xl border border-indigo-900/60 relative overflow-hidden">
      
      {/* Subtle Background Glow */}
      <div className="absolute -top-24 -right-24 w-72 h-72 bg-blue-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-24 -left-24 w-72 h-72 bg-purple-600/10 rounded-full blur-3xl pointer-events-none" />

      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-white/10">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-1.5 bg-indigo-500/20 rounded-lg text-cyan-300">
              <Sparkles className="w-4 h-4" />
            </span>
            <h3 className="text-lg font-black tracking-tight text-white">
              Customer 360 &amp; Predictive Intelligence
            </h3>
            <span className="text-[10px] uppercase font-extrabold px-2.5 py-0.5 rounded-full bg-cyan-400 text-slate-950 tracking-wider">
              AI Powered
            </span>
          </div>
          <p className="text-xs text-indigo-200 mt-1">
            Real-time RFM cohort segmentation, churn risk modeling, and lifetime value prediction
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-3.5 py-1.5 rounded-xl bg-white/10 border border-white/20 text-xs font-bold text-amber-300 flex items-center gap-1.5 shadow-inner">
            <Award className="w-3.5 h-3.5" />
            {profile.customer_tier} Tier
          </span>
          <span className="px-3.5 py-1.5 rounded-xl bg-blue-500/20 border border-blue-400/30 text-xs font-bold text-blue-200">
            {profile.rfm.rfm_segment}
          </span>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3.5 mt-6">
        <div className="p-3.5 rounded-2xl bg-white/5 border border-white/10">
          <span className="text-[10px] uppercase tracking-wider text-indigo-300 font-bold block">
            Predicted CLV (12-Mo)
          </span>
          <span className="text-lg sm:text-xl font-black text-cyan-300 mt-0.5 block">
            ₹{profile.predictive_metrics.predicted_clv.toLocaleString('en-IN')}
          </span>
          <span className="text-[10px] text-slate-400">Projected customer value</span>
        </div>

        <div className="p-3.5 rounded-2xl bg-white/5 border border-white/10">
          <span className="text-[10px] uppercase tracking-wider text-indigo-300 font-bold block">
            Churn Probability
          </span>
          <div className="flex items-center gap-2 mt-0.5">
            <span className="text-lg sm:text-xl font-black text-white">
              {(profile.predictive_metrics.churn_probability * 100).toFixed(0)}%
            </span>
            <span className={`text-[10px] px-2 py-0.5 rounded font-bold ${
              profile.predictive_metrics.churn_risk_level === 'LOW' ? 'bg-emerald-500/20 text-emerald-300' :
              profile.predictive_metrics.churn_risk_level === 'MEDIUM' ? 'bg-amber-500/20 text-amber-300' : 'bg-rose-500/20 text-rose-300'
            }`}>
              {profile.predictive_metrics.churn_risk_level}
            </span>
          </div>
          <span className="text-[10px] text-slate-400">Gradient churn model</span>
        </div>

        <div className="p-3.5 rounded-2xl bg-white/5 border border-white/10">
          <span className="text-[10px] uppercase tracking-wider text-indigo-300 font-bold block">
            Average Order Value
          </span>
          <span className="text-lg sm:text-xl font-black text-white mt-0.5 block">
            ₹{profile.rfm.aov.toLocaleString('en-IN')}
          </span>
          <span className="text-[10px] text-slate-400">{profile.rfm.frequency_orders} total orders</span>
        </div>

        <div className="p-3.5 rounded-2xl bg-white/5 border border-white/10">
          <span className="text-[10px] uppercase tracking-wider text-indigo-300 font-bold block">
            Next Purchase ETA
          </span>
          <span className="text-lg sm:text-xl font-black text-white mt-0.5 block">
            {profile.predictive_metrics.next_expected_purchase_days} Days
          </span>
          <span className="text-[10px] text-slate-400">Recency: {profile.rfm.recency_days}d ago</span>
        </div>
      </div>

      {/* Loyalty & Rewards Section */}
      {loyalty && (
        <div className="mt-6 p-4 rounded-2xl bg-gradient-to-r from-amber-500/10 via-purple-500/10 to-indigo-500/10 border border-amber-400/20 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-400/20 text-amber-300 flex items-center justify-center">
              <Gift className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-sm text-amber-200">Loyalty Balance:</span>
                <span className="font-black text-base text-amber-300">{loyalty.current_points} Points</span>
                <span className="text-[10px] text-slate-400">({loyalty.lifetime_points} lifetime)</span>
              </div>
              <p className="text-xs text-slate-300">
                100 points = ₹100 instant store credit towards checkout
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => handleRedeem(100)}
              disabled={redeeming || loyalty.current_points < 100}
              className="px-4 py-2 bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-slate-950 font-extrabold text-xs rounded-xl shadow-md transition-all flex items-center gap-1.5"
            >
              {redeeming ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <CheckCircle className="w-3.5 h-3.5" />}
              Redeem 100 Pts (₹100 Off)
            </button>
          </div>
        </div>
      )}

      {redeemSuccess && (
        <div className="mt-3 p-3 bg-emerald-500/20 border border-emerald-400/40 text-emerald-200 text-xs rounded-xl font-medium">
          {redeemSuccess}
        </div>
      )}

      {/* Customer Affinity & Retention Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
        
        {/* Affinity Preferences */}
        <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
          <h4 className="text-xs font-bold uppercase tracking-wider text-indigo-300 mb-2 flex items-center gap-1.5">
            <Heart className="w-3.5 h-3.5 text-rose-400" />
            Category &amp; Brand Affinity
          </h4>
          <div className="space-y-2">
            <div>
              <span className="text-[11px] text-slate-400 block mb-1">Top Categories:</span>
              <div className="flex flex-wrap gap-1.5">
                {profile.preferences.favorite_categories.map((cat, i) => (
                  <span key={i} className="text-xs px-2.5 py-0.5 bg-blue-500/20 text-blue-200 rounded-lg font-medium">
                    {cat}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <span className="text-[11px] text-slate-400 block mb-1">Top Brands:</span>
              <div className="flex flex-wrap gap-1.5">
                {profile.preferences.favorite_brands.map((b, i) => (
                  <span key={i} className="text-xs px-2.5 py-0.5 bg-purple-500/20 text-purple-200 rounded-lg font-medium">
                    {b}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Personalized Retention Recommendations */}
        <div className="p-4 rounded-2xl bg-white/5 border border-white/10">
          <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-300 mb-2 flex items-center gap-1.5">
            <TrendingUp className="w-3.5 h-3.5 text-cyan-400" />
            AI Retention Playbook
          </h4>
          <div className="space-y-2">
            {profile.retention_recommendations.map((rec, idx) => (
              <div key={idx} className="p-2.5 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between gap-2">
                <div>
                  <span className="font-bold text-xs text-white block">{rec.action}</span>
                  <span className="text-[10px] text-slate-400">{rec.reason}</span>
                </div>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase whitespace-nowrap ${
                  rec.urgency === 'HIGH' ? 'bg-rose-500/30 text-rose-300' :
                  rec.urgency === 'MEDIUM' ? 'bg-amber-500/30 text-amber-300' : 'bg-blue-500/30 text-blue-300'
                }`}>
                  {rec.urgency}
                </span>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};
