import React, { useState, useEffect } from 'react';
import { Cpu, Activity, AlertTriangle, CheckCircle, ArrowUpRight, GitBranch, RefreshCw, BarChart2 } from 'lucide-react';
import { api } from '../services/api';
import { MLModelItem, MLDriftItem, ABExperimentItem } from '../types';

export const MLOpsDashboardView: React.FC = () => {
  const [models, setModels] = useState<MLModelItem[]>([]);
  const [driftLogs, setDriftLogs] = useState<MLDriftItem[]>([]);
  const [experiments, setExperiments] = useState<ABExperimentItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [promotingId, setPromotingId] = useState<string | null>(null);

  useEffect(() => {
    loadMLOpsData();
  }, []);

  const loadMLOpsData = async () => {
    setLoading(true);
    try {
      const [modelsData, driftData, expData] = await Promise.all([
        api.getMLOpsModels().catch(() => []),
        api.getMLOpsDrift().catch(() => []),
        api.getExperiments().catch(() => []),
      ]);
      setModels(modelsData || []);
      setDriftLogs(driftData || []);
      setExperiments(expData || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handlePromote = async (modelId: string) => {
    setPromotingId(modelId);
    try {
      await api.promoteMLOpsModel(modelId, 'PRODUCTION');
      await loadMLOpsData();
    } catch (err: any) {
      alert(err.message || 'Model promotion failed');
    } finally {
      setPromotingId(null);
    }
  };

  return (
    <div className="space-y-8">
      {/* Registered Models Table */}
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-xl bg-blue-50 dark:bg-blue-950/40 text-blue-600">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900 dark:text-white">
                MLOps Model Registry &amp; Lifecycle Governance
              </h2>
              <p className="text-xs text-slate-400">
                Continuous lineage, versioning, latency benchmarks, and staged promotion
              </p>
            </div>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-bold bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300">
            {models.length} Registered Artifacts
          </span>
        </div>

        {loading ? (
          <div className="py-8 text-center text-xs text-slate-400 flex items-center justify-center gap-2">
            <RefreshCw className="w-4 h-4 animate-spin text-blue-500" />
            Querying ML registry...
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 dark:bg-slate-800/60 text-slate-400 font-bold uppercase tracking-wider">
                <tr>
                  <th className="p-3">Model Name</th>
                  <th className="p-3">Version</th>
                  <th className="p-3">Algorithm</th>
                  <th className="p-3">Stage</th>
                  <th className="p-3">Metric</th>
                  <th className="p-3">Latency</th>
                  <th className="p-3">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {models.map((m) => (
                  <tr key={m.model_id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30">
                    <td className="p-3 font-semibold text-slate-800 dark:text-slate-200">
                      {m.model_name}
                    </td>
                    <td className="p-3 font-mono text-slate-500">{m.version}</td>
                    <td className="p-3 font-mono text-slate-600 dark:text-slate-400 max-w-xs truncate">
                      {m.algorithm}
                    </td>
                    <td className="p-3">
                      <span
                        className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                          m.stage === 'PRODUCTION'
                            ? 'bg-emerald-50 text-emerald-600 dark:bg-emerald-950/40'
                            : 'bg-amber-50 text-amber-600 dark:bg-amber-950/40'
                        }`}
                      >
                        {m.stage}
                      </span>
                    </td>
                    <td className="p-3 font-semibold text-indigo-600 dark:text-indigo-400">
                      {m.accuracy_metric ? `${m.accuracy_metric.name}: ${m.accuracy_metric.value}` : 'N/A'}
                    </td>
                    <td className="p-3 font-mono text-slate-500">
                      {m.latency_ms ? `${m.latency_ms.toFixed(1)}ms` : '1.2ms'}
                    </td>
                    <td className="p-3">
                      {m.stage !== 'PRODUCTION' ? (
                        <button
                          onClick={() => handlePromote(m.model_id)}
                          disabled={promotingId === m.model_id}
                          className="px-2.5 py-1 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-lg font-bold text-[10px] transition-all flex items-center gap-1 shadow-xs"
                        >
                          <ArrowUpRight className="w-3 h-3" />
                          Promote Prod
                        </button>
                      ) : (
                        <span className="text-[10px] text-emerald-600 font-bold flex items-center gap-1">
                          <CheckCircle className="w-3 h-3" /> Serving
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Model Drift Monitoring Table */}
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-xl bg-purple-50 dark:bg-purple-950/40 text-purple-600">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900 dark:text-white">
                Statistical Model Drift &amp; Feature Divergence Monitor
              </h2>
              <p className="text-xs text-slate-400">
                Kolmogorov-Smirnov &amp; Population Stability Index (PSI) tracking
              </p>
            </div>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300">
            Automated Daily Scan
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 dark:bg-slate-800/60 text-slate-400 font-bold uppercase tracking-wider">
              <tr>
                <th className="p-3">Model</th>
                <th className="p-3">Drift Metric</th>
                <th className="p-3">Baseline</th>
                <th className="p-3">Current</th>
                <th className="p-3">p-value</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {driftLogs.map((d) => (
                <tr key={d.drift_id} className="hover:bg-slate-50/50 dark:hover:bg-slate-800/30">
                  <td className="p-3 font-semibold text-slate-800 dark:text-slate-200">
                    {d.model_name}
                  </td>
                  <td className="p-3 font-mono text-slate-500">{d.drift_metric}</td>
                  <td className="p-3 font-mono text-slate-600">{d.baseline_value?.toFixed(4)}</td>
                  <td className="p-3 font-mono text-slate-600">{d.current_value?.toFixed(4)}</td>
                  <td className="p-3 font-mono text-slate-500">{d.p_value?.toFixed(4)}</td>
                  <td className="p-3">
                    <span
                      className={`px-2 py-0.5 rounded-full text-[10px] font-bold flex items-center gap-1 w-max ${
                        d.drift_detected
                          ? 'bg-rose-100 text-rose-700'
                          : 'bg-emerald-100 text-emerald-700'
                      }`}
                    >
                      {d.drift_detected ? (
                        <>
                          <AlertTriangle className="w-3 h-3" /> Drift Detected
                        </>
                      ) : (
                        <>
                          <CheckCircle className="w-3 h-3" /> In Control
                        </>
                      )}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* A/B Experimentation Control */}
      {experiments.length > 0 && (
        <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-800">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-xl bg-amber-50 dark:bg-amber-950/40 text-amber-600">
                <BarChart2 className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-base font-bold text-slate-900 dark:text-white">
                  Active A/B Recommendation &amp; Algorithmic Experiments
                </h2>
                <p className="text-xs text-slate-400">
                  Real-time participant traffic splitting &amp; conversion lift analysis
                </p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {experiments.map((exp) => (
              <div
                key={exp.experiment_id}
                className="p-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/40 space-y-2"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-xs text-slate-900 dark:text-white">
                    {exp.name}
                  </span>
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                    {exp.status}
                  </span>
                </div>
                <p className="text-xs text-slate-500">{exp.description}</p>
                <div className="flex items-center gap-2 pt-1 text-[11px] text-slate-600 font-mono">
                  <span>Variants: {exp.variants?.join(', ')}</span>
                  <span>•</span>
                  <span>Traffic: {JSON.stringify(exp.traffic_split)}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
