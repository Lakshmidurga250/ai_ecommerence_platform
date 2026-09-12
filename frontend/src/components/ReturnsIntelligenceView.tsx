import React, { useState, useEffect } from 'react';
import { RotateCcw, ShieldAlert, DollarSign, Truck, AlertCircle } from 'lucide-react';
import { api } from '../services/api';
import { ReturnsDashboard } from '../types';

export const ReturnsIntelligenceView: React.FC = () => {
  const [dashboard, setDashboard] = useState<ReturnsDashboard | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReturnsData();
  }, []);

  const loadReturnsData = async () => {
    try {
      setLoading(true);
      const data = await api.getReturnsDashboard();
      setDashboard(data);
    } catch (err) {
      console.error('Failed to load returns dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-slate-500">Loading returns analytics...</div>;
  }

  if (!dashboard) return null;

  return (
    <div className="space-y-6">
      {/* Top KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase">Platform Return Rate</span>
            <RotateCcw className="w-4 h-4 text-indigo-600" />
          </div>
          <div className="text-2xl font-black text-slate-900 mt-2">
            {dashboard.returns_kpis.overall_platform_return_rate}
          </div>
          <p className="text-[11px] text-emerald-600 mt-1 font-medium">-1.4% vs industry baseline</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase">Refund Value</span>
            <DollarSign className="w-4 h-4 text-rose-600" />
          </div>
          <div className="text-2xl font-black text-slate-900 mt-2">
            ₹{dashboard.returns_kpis.total_refund_value_inr.toLocaleString('en-IN')}
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Across {dashboard.returns_kpis.total_return_requests} processed returns</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase">Reverse Logistics Cost</span>
            <Truck className="w-4 h-4 text-amber-600" />
          </div>
          <div className="text-2xl font-black text-slate-900 mt-2">
            ₹{dashboard.returns_kpis.reverse_logistics_cost_inr.toLocaleString('en-IN')}
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Carrier dispatch & intake inspection</p>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase">Abuse Risk Rate</span>
            <ShieldAlert className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-black text-slate-900 mt-2">
            {dashboard.returns_kpis.fraudulent_abuse_rate}
          </div>
          <p className="text-[11px] text-emerald-600 mt-1 font-medium">Under strict 2.0% threshold</p>
        </div>
      </div>

      {/* Breakdowns Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Return Reasons */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h4 className="font-bold text-sm text-slate-900 mb-4">Top Return Reasons</h4>
          <div className="space-y-3">
            {dashboard.top_return_reasons.map((r, i) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-100">
                <div>
                  <p className="text-xs font-bold text-slate-800">{r.reason}</p>
                  <p className="text-[10px] text-slate-400 mt-0.5">Primary: {r.primary_category}</p>
                </div>
                <span className="text-xs font-black text-indigo-700 bg-indigo-50 px-2.5 py-1 rounded-lg border border-indigo-100">
                  {r.percentage}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Category Volatility */}
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h4 className="font-bold text-sm text-slate-900 mb-4">Category Return Volatility</h4>
          <div className="space-y-3">
            {dashboard.category_return_rates.map((c, i) => {
              const badgeColor =
                c.risk_tier === 'HIGH'
                  ? 'bg-rose-100 text-rose-700 border-rose-200'
                  : c.risk_tier === 'MEDIUM'
                  ? 'bg-amber-100 text-amber-700 border-amber-200'
                  : 'bg-emerald-100 text-emerald-700 border-emerald-200';
              return (
                <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-100">
                  <div>
                    <p className="text-xs font-bold text-slate-800">{c.category}</p>
                    <p className="text-[10px] text-slate-400 mt-0.5">Return Rate: {c.return_rate}</p>
                  </div>
                  <span className={`text-[10px] font-black uppercase px-2.5 py-1 rounded-lg border ${badgeColor}`}>
                    {c.risk_tier} Risk
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
