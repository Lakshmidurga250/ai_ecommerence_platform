import React, { useState, useEffect } from 'react';
import { Filter, TrendingDown, CheckCircle, AlertTriangle, ArrowRight } from 'lucide-react';
import { api } from '../services/api';
import { FunnelAnalytics } from '../types';

export const CustomerFunnelWidget: React.FC = () => {
  const [funnel, setFunnel] = useState<FunnelAnalytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFunnel();
  }, []);

  const loadFunnel = async () => {
    try {
      setLoading(true);
      const data = await api.getFunnelAnalytics();
      setFunnel(data);
    } catch (err) {
      console.error('Failed to load funnel analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="animate-pulse space-y-4">
          <div className="h-6 w-48 bg-slate-200 rounded"></div>
          <div className="h-32 bg-slate-100 rounded"></div>
        </div>
      </div>
    );
  }

  if (!funnel) return null;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-6 border-b border-slate-100 gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Filter className="w-5 h-5 text-indigo-600" />
            <h3 className="font-bold text-lg text-slate-900">Customer Journey Funnel</h3>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Step-by-step conversion tracking and bottleneck friction points
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-indigo-50 px-3 py-1.5 border border-indigo-100">
            <span className="text-[10px] uppercase font-bold text-indigo-700 block">End-to-End Conversion</span>
            <span className="text-base font-black text-indigo-900">
              {funnel.funnel_summary.overall_conversion_rate}
            </span>
          </div>
          <div className="rounded-xl bg-amber-50 px-3 py-1.5 border border-amber-100">
            <span className="text-[10px] uppercase font-bold text-amber-700 block">Top Bottleneck</span>
            <span className="text-xs font-bold text-amber-900">
              {funnel.funnel_summary.primary_bottleneck} ({funnel.funnel_summary.max_stage_dropoff} drop)
            </span>
          </div>
        </div>
      </div>

      {/* Funnel Steps */}
      <div className="mt-6 space-y-3">
        {funnel.funnel_steps.map((step, idx) => {
          const widthPct = Math.max(12, 100 - idx * 16);
          return (
            <div key={step.stage_key} className="space-y-1">
              <div className="flex justify-between text-xs font-semibold text-slate-700">
                <span>{step.label}</span>
                <span className="text-slate-900 font-extrabold">
                  {step.visitor_count.toLocaleString('en-IN')} users ({step.overall_conversion_pct})
                </span>
              </div>
              <div className="h-3.5 w-full bg-slate-100 rounded-full overflow-hidden p-0.5">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-indigo-700 transition-all duration-500"
                  style={{ width: `${widthPct}%` }}
                />
              </div>
              {idx > 0 && (
                <div className="flex justify-end text-[10px] text-rose-500 font-medium">
                  <TrendingDown className="w-3 h-3 mr-0.5" />
                  {step.dropoff_pct} drop from previous step
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* AI Friction Optimization Tips */}
      <div className="mt-6 pt-4 border-t border-slate-100 bg-slate-50/60 -mx-6 -mb-6 p-6 rounded-b-2xl">
        <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wide flex items-center gap-1.5 mb-2">
          <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
          AI Funnel Optimization Playbook
        </h4>
        <div className="space-y-2">
          {funnel.ai_optimization_recommendations.map((rec, i) => (
            <div key={i} className="text-xs text-slate-600 bg-white p-2.5 rounded-xl border border-slate-200">
              <span className="font-bold text-slate-800">{rec.stage}: </span>
              {rec.action}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
