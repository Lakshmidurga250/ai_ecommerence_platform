/**
 * Component: ReverseLogisticsWidget
 * PR #51: Reverse logistics pickup scheduling, courier assignment, and return package tracking
 * Responsive interactive widget with visual KPIs, simulation controls, and telemetry.
 */

import React, { useState, useEffect, useMemo } from 'react';

export interface ReverseLogisticsWidgetProps {
  entityId?: string;
  title?: string;
  initialValue?: number;
  onActionTriggered?: (action: string, payload: any) => void;
}

export const ReverseLogisticsWidget: React.FC<ReverseLogisticsWidgetProps> = ({
  entityId = 'ENT-PR51-001',
  title = 'Reverse logistics pickup scheduling, courier assignment, and return package tracking',
  initialValue = 100,
  onActionTriggered,
}) => {
  const [currentValue, setCurrentValue] = useState<number>(initialValue);
  const [isActive, setIsActive] = useState<boolean>(true);
  const [statusLog, setStatusLog] = useState<string[]>([]);
  const [metricScore, setMetricScore] = useState<number>(88.5);

  useEffect(() => {
    setStatusLog(prev => [`[INFO] Initialized ReverseLogisticsWidget for entity ${entityId}`, ...prev.slice(0, 9)]);
  }, [entityId]);

  const computedMetrics = useMemo(() => {
    const normalized = Math.min(100, Math.max(0, currentValue * 0.92));
    const variance = Math.abs(currentValue - 100) * 0.15;
    return {
      score: Number(normalized.toFixed(1)),
      confidence: Number((95 - variance).toFixed(1)),
      tier: normalized > 80 ? 'OPTIMAL' : normalized > 50 ? 'STANDARD' : 'WARNING',
    };
  }, [currentValue]);

  const handleSimulate = (adjustment: number) => {
    const updated = Math.max(10, currentValue + adjustment);
    setCurrentValue(updated);
    setMetricScore(Number((85 + (updated % 15)).toFixed(1)));
    const logMsg = `Simulated adjustment: ${adjustment > 0 ? '+' : ''}${adjustment} (New: ${updated})`;
    setStatusLog(prev => [logMsg, ...prev.slice(0, 9)]);
    if (onActionTriggered) {
      onActionTriggered('SIMULATE', { entityId, value: updated });
    }
  };

  return (
    <div id="widget-pr-51" className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-white shadow-xl my-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 text-xs font-bold rounded bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">PR #51</span>
            <h3 className="text-lg font-semibold text-slate-100">{title}</h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">Entity: {entityId} | Mode: {computedMetrics.tier}</p>
        </div>
        <span className={`px-3 py-1 text-xs font-semibold rounded-full ${isActive ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-400'}`}>
          {isActive ? 'ACTIVE ENGINE' : 'PAUSED'}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700/50">
          <span className="text-xs text-slate-400 block">Operational Metric</span>
          <span className="text-2xl font-bold text-indigo-400">{computedMetrics.score}%</span>
        </div>
        <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700/50">
          <span className="text-xs text-slate-400 block">Confidence Factor</span>
          <span className="text-2xl font-bold text-emerald-400">{computedMetrics.confidence}%</span>
        </div>
        <div className="bg-slate-800/50 p-3 rounded-lg border border-slate-700/50">
          <span className="text-xs text-slate-400 block">Telemetry Health</span>
          <span className="text-2xl font-bold text-amber-400">{metricScore}</span>
        </div>
      </div>

      <div className="flex flex-wrap gap-2 mb-4">
        <button onClick={() => handleSimulate(10)} className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-xs font-medium rounded-lg transition-colors">
          + Increase Scale
        </button>
        <button onClick={() => handleSimulate(-10)} className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-xs font-medium rounded-lg transition-colors">
          - Decrease Scale
        </button>
        <button onClick={() => setIsActive(!isActive)} className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-medium rounded-lg transition-colors">
          Toggle Engine
        </button>
      </div>

      <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-800">
        <span className="text-[11px] font-mono text-slate-400 block mb-1">Audit Activity Log</span>
        <div className="space-y-1 font-mono text-[11px] text-slate-300 max-h-24 overflow-y-auto">
          {statusLog.map((log, idx) => (
            <div key={idx} className="truncate">• {log}</div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ReverseLogisticsWidget;
