import React, { useState, useEffect } from 'react';
import { TrendingUp, DollarSign, Percent, ArrowUpRight, ArrowDownRight, Sparkles, Check, CheckCircle2, RefreshCw } from 'lucide-react';
import { api } from '../services/api';
import { PricingRecommendation } from '../types';

export const DynamicPricingWidget: React.FC = () => {
  const [recommendations, setRecommendations] = useState<PricingRecommendation[]>([]);
  const [strategyFilter, setStrategyFilter] = useState<string>('ALL');
  const [appliedMap, setAppliedMap] = useState<Record<number, boolean>>({});
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadRecommendations();
  }, [strategyFilter]);

  const loadRecommendations = async () => {
    setLoading(true);
    try {
      const data = await api.getSellerPricingRecommendations({
        strategy: strategyFilter !== 'ALL' ? strategyFilter : undefined,
      });
      setRecommendations(data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApply = (recId: number) => {
    setAppliedMap((prev) => ({ ...prev, [recId]: true }));
  };

  const avgDemandLift = recommendations.length > 0
    ? (recommendations.reduce((acc, r) => acc + (r.expected_demand_lift_pct || 0), 0) / recommendations.length)
    : 0;

  const avgRevenueShift = recommendations.length > 0
    ? (recommendations.reduce((acc, r) => acc + (r.expected_revenue_shift_pct || 0), 0) / recommendations.length)
    : 0;

  return (
    <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 sm:p-8 shadow-sm my-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100 dark:border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 bg-indigo-50 dark:bg-indigo-950/60 rounded-xl text-indigo-600 dark:text-indigo-400">
              <TrendingUp className="w-5 h-5" />
            </span>
            <h3 className="text-lg font-bold text-slate-900 dark:text-white">
              AI Dynamic Pricing &amp; Elasticity Engine
            </h3>
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-blue-100 dark:bg-blue-900/40 text-blue-800 dark:text-blue-300 uppercase tracking-wider">
              Real-Time
            </span>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            Price elasticity curve optimization based on stock velocity, competitor benchmark, and demand surges
          </p>
        </div>

        {/* Strategy Filter */}
        <div className="flex items-center gap-2">
          <label className="text-xs font-semibold text-slate-500">Strategy:</label>
          <select
            value={strategyFilter}
            onChange={(e) => setStrategyFilter(e.target.value)}
            className="text-xs border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-1.5 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="ALL">All Strategies</option>
            <option value="DEMAND_SURGE">Demand Surge</option>
            <option value="COMPETITOR_MATCH">Competitor Match</option>
            <option value="SLOW_MOVING_LIQUIDATION">Inventory Liquidation</option>
            <option value="MARGIN_MAXIMIZATION">Margin Maximization</option>
          </select>
        </div>
      </div>

      {/* Overview Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 my-6">
        <div className="p-4 rounded-2xl bg-indigo-50/50 dark:bg-indigo-950/20 border border-indigo-100 dark:border-indigo-900/30">
          <span className="text-[11px] font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider block">
            Pricing Opportunities
          </span>
          <span className="text-2xl font-black text-slate-900 dark:text-white mt-1 block">
            {recommendations.length} Products
          </span>
          <span className="text-[10px] text-slate-500">Elasticity optimized suggestions</span>
        </div>

        <div className="p-4 rounded-2xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-100 dark:border-emerald-900/30">
          <span className="text-[11px] font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider block">
            Avg. Expected Demand Lift
          </span>
          <span className="text-2xl font-black text-emerald-600 dark:text-emerald-400 mt-1 block flex items-center gap-1">
            <ArrowUpRight className="w-5 h-5" />
            +{avgDemandLift.toFixed(1)}%
          </span>
          <span className="text-[10px] text-slate-500">Projected volume acceleration</span>
        </div>

        <div className="p-4 rounded-2xl bg-blue-50/50 dark:bg-blue-950/20 border border-blue-100 dark:border-blue-900/30">
          <span className="text-[11px] font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider block">
            Avg. Projected Revenue Shift
          </span>
          <span className="text-2xl font-black text-blue-600 dark:text-blue-400 mt-1 block flex items-center gap-1">
            <ArrowUpRight className="w-5 h-5" />
            +{avgRevenueShift.toFixed(1)}%
          </span>
          <span className="text-[10px] text-slate-500">Net revenue enhancement</span>
        </div>
      </div>

      {/* Pricing Recommendation Cards */}
      {loading ? (
        <div className="py-8 text-center text-slate-400 text-xs">
          <RefreshCw className="w-5 h-5 animate-spin mx-auto mb-2 text-indigo-500" />
          Calculating price elasticity gradients...
        </div>
      ) : recommendations.length === 0 ? (
        <div className="py-8 text-center text-slate-400 text-xs font-medium">
          No pricing adjustments needed. Current prices are optimally aligned with market equilibrium.
        </div>
      ) : (
        <div className="space-y-3">
          {recommendations.slice(0, 5).map((rec) => {
            const isApplied = appliedMap[rec.recommendation_id];
            const isPriceDrop = rec.price_delta < 0;

            return (
              <div
                key={rec.recommendation_id}
                className="p-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/40 dark:bg-slate-850 hover:bg-slate-50 dark:hover:bg-slate-800/80 transition-all flex flex-col md:flex-row md:items-center justify-between gap-4"
              >
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-slate-900 dark:text-white">
                      {rec.product_name}
                    </span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-100 text-indigo-700 dark:bg-indigo-950 dark:text-indigo-300">
                      {rec.strategy}
                    </span>
                    <span className="text-[10px] font-mono text-slate-400">
                      Elasticity: {rec.elasticity?.toFixed(2)}
                    </span>
                  </div>

                  <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 leading-relaxed">
                    {rec.rationale}
                  </p>

                  <div className="flex items-center gap-4 mt-2 text-xs">
                    <span className="text-emerald-600 dark:text-emerald-400 font-semibold">
                      +{rec.expected_demand_lift_pct}% Demand
                    </span>
                    <span className="text-blue-600 dark:text-blue-400 font-semibold">
                      +{rec.expected_revenue_shift_pct}% Revenue
                    </span>
                  </div>
                </div>

                {/* Price Shift Comparison & Action */}
                <div className="flex items-center gap-4 self-end md:self-center">
                  <div className="text-right">
                    <div className="flex items-center justify-end gap-2">
                      <span className="text-xs text-slate-400 line-through">
                        ₹{rec.current_price.toLocaleString('en-IN')}
                      </span>
                      <span className="text-base font-black text-slate-900 dark:text-white">
                        ₹{rec.recommended_price.toLocaleString('en-IN')}
                      </span>
                    </div>
                    <span className={`text-[10px] font-bold inline-flex items-center gap-0.5 ${
                      isPriceDrop ? 'text-blue-600' : 'text-emerald-600'
                    }`}>
                      {isPriceDrop ? <ArrowDownRight className="w-3 h-3" /> : <ArrowUpRight className="w-3 h-3" />}
                      {rec.price_delta_pct > 0 ? `+${rec.price_delta_pct}%` : `${rec.price_delta_pct}%`}
                    </span>
                  </div>

                  <button
                    onClick={() => handleApply(rec.recommendation_id)}
                    disabled={isApplied}
                    className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 shadow-sm ${
                      isApplied
                        ? 'bg-emerald-600 text-white cursor-default'
                        : 'bg-indigo-600 hover:bg-indigo-700 text-white'
                    }`}
                  >
                    {isApplied ? (
                      <>
                        <CheckCircle2 className="w-3.5 h-3.5" /> Applied
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-3.5 h-3.5" /> Accept Price
                      </>
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
