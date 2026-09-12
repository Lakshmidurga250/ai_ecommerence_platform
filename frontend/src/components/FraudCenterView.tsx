import React, { useState, useEffect } from 'react';
import { ShieldAlert, ShieldCheck, CheckCircle, XCircle, AlertTriangle, RefreshCw, Filter, ArrowUpRight } from 'lucide-react';
import { api } from '../services/api';
import { FraudAlertItem, FraudStatistics } from '../types';

export const FraudCenterView: React.FC = () => {
  const [alerts, setAlerts] = useState<FraudAlertItem[]>([]);
  const [stats, setStats] = useState<FraudStatistics | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('ALL');
  const [loading, setLoading] = useState<boolean>(true);
  const [resolvingId, setResolvingId] = useState<number | null>(null);

  useEffect(() => {
    loadFraudData();
  }, [statusFilter]);

  const loadFraudData = async () => {
    setLoading(true);
    try {
      const [alertsData, statsData] = await Promise.all([
        api.getFraudAlerts({ status: statusFilter !== 'ALL' ? statusFilter : undefined }),
        api.getFraudStatistics(),
      ]);
      setAlerts(alertsData || []);
      setStats(statsData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleResolve = async (alertId: number, resolution: 'APPROVED' | 'BLOCKED') => {
    setResolvingId(alertId);
    try {
      await api.resolveFraudAlert(alertId, resolution, `Admin manual resolution: ${resolution}`);
      await loadFraudData();
    } catch (err: any) {
      alert(err.message || 'Failed to resolve fraud alert');
    } finally {
      setResolvingId(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              Evaluated Orders
            </span>
            <span className="text-2xl font-black text-slate-900 dark:text-white mt-1 block">
              {stats.total_evaluated_orders}
            </span>
            <span className="text-[10px] text-emerald-600 font-semibold">100% Real-Time Scored</span>
          </div>

          <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <span className="text-[11px] font-bold text-rose-500 uppercase tracking-wider block">
              High Risk Alerts
            </span>
            <span className="text-2xl font-black text-rose-600 dark:text-rose-400 mt-1 block">
              {stats.high_risk_count}
            </span>
            <span className="text-[10px] text-rose-500 font-semibold">Score &gt;= 75/100</span>
          </div>

          <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <span className="text-[11px] font-bold text-amber-500 uppercase tracking-wider block">
              Quarantined / Blocked
            </span>
            <span className="text-2xl font-black text-amber-600 dark:text-amber-400 mt-1 block">
              {stats.blocked_order_count}
            </span>
            <span className="text-[10px] text-slate-400">Zero unauthorized capture</span>
          </div>

          <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
            <span className="text-[11px] font-bold text-emerald-500 uppercase tracking-wider block">
              Prevention Rate
            </span>
            <span className="text-2xl font-black text-emerald-600 dark:text-emerald-400 mt-1 block">
              {stats.fraud_prevention_rate_pct.toFixed(1)}%
            </span>
            <span className="text-[10px] text-emerald-600 font-semibold">Isolation Forest Shield</span>
          </div>
        </div>
      )}

      {/* Main Table Card */}
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-4">
        
        {/* Header & Filter */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-xl bg-rose-50 dark:bg-rose-950/40 text-rose-600">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900 dark:text-white">
                Fraud Intelligence &amp; Risk Quarantine Center
              </h2>
              <p className="text-xs text-slate-400">
                Explainable anomaly attribution &amp; human-in-the-loop dispute resolution
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <div className="flex rounded-xl bg-slate-100 dark:bg-slate-800 p-1">
              {['ALL', 'PENDING', 'APPROVED', 'BLOCKED'].map((status) => (
                <button
                  key={status}
                  onClick={() => setStatusFilter(status)}
                  className={`px-3 py-1 rounded-lg text-xs font-bold transition-colors ${
                    statusFilter === status
                      ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-white shadow-xs'
                      : 'text-slate-500 hover:text-slate-900'
                  }`}
                >
                  {status}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* List of Alerts */}
        {loading ? (
          <div className="py-8 text-center text-xs text-slate-400 flex items-center justify-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin text-rose-500" />
            Evaluating fraud alert queue...
          </div>
        ) : alerts.length === 0 ? (
          <div className="p-8 text-center text-xs text-slate-400 border border-dashed rounded-2xl">
            No transactions found in queue matching '{statusFilter}' status. System safe.
          </div>
        ) : (
          <div className="divide-y divide-slate-100 dark:divide-slate-800">
            {alerts.map((item) => (
              <div
                key={item.alert_id}
                className="py-4 flex flex-col md:flex-row md:items-center justify-between gap-4 text-xs"
              >
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2 font-bold text-slate-900 dark:text-white">
                    <span className="font-mono text-slate-600 dark:text-slate-300">
                      Alert #{item.alert_id}
                    </span>
                    <span className="text-slate-300">•</span>
                    <span>Order #{item.order_id}</span>
                    <span className="text-slate-300">•</span>
                    <span>{item.customer_name}</span>
                    <span className="text-slate-300">•</span>
                    <span className="font-black text-slate-900 dark:text-white">
                      ₹{item.order_amount?.toLocaleString('en-IN')}
                    </span>
                    <span
                      className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                        item.risk_level === 'HIGH'
                          ? 'bg-rose-100 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300'
                          : item.risk_level === 'MEDIUM'
                          ? 'bg-amber-100 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300'
                          : 'bg-emerald-100 text-emerald-700'
                      }`}
                    >
                      Risk: {item.risk_score}/100
                    </span>
                    <span
                      className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                        item.status === 'APPROVED'
                          ? 'bg-emerald-50 text-emerald-600'
                          : item.status === 'BLOCKED'
                          ? 'bg-rose-50 text-rose-600'
                          : 'bg-slate-100 text-slate-600'
                      }`}
                    >
                      {item.status}
                    </span>
                  </div>

                  {/* Factor Attribution Pills */}
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {item.flagged_factors?.map((factor, idx) => (
                      <span
                        key={idx}
                        className="bg-rose-50 dark:bg-rose-950/20 border border-rose-100 dark:border-rose-900/30 text-rose-700 dark:text-rose-300 px-2 py-0.5 rounded-lg text-[10px] font-medium"
                      >
                        ⚠ {factor}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Resolution Action Buttons */}
                {item.status === 'PENDING' && (
                  <div className="flex items-center gap-2 self-end md:self-center">
                    <button
                      onClick={() => handleResolve(item.alert_id, 'APPROVED')}
                      disabled={resolvingId === item.alert_id}
                      className="px-3 py-1.5 rounded-xl border border-emerald-300 text-emerald-700 dark:text-emerald-300 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 text-xs font-bold transition-all flex items-center gap-1"
                    >
                      <CheckCircle className="w-3.5 h-3.5 text-emerald-500" />
                      Approve
                    </button>
                    <button
                      onClick={() => handleResolve(item.alert_id, 'BLOCKED')}
                      disabled={resolvingId === item.alert_id}
                      className="px-3 py-1.5 rounded-xl bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold transition-all shadow-xs flex items-center gap-1"
                    >
                      <XCircle className="w-3.5 h-3.5" />
                      Block &amp; Cancel
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

      </div>
    </div>
  );
};
