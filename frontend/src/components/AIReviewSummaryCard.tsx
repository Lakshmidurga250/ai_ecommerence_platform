import React, { useEffect, useState } from 'react';
import { Sparkles, ThumbsUp, ThumbsDown, ShieldCheck, AlertTriangle, CheckCircle2, BarChart3, HelpCircle } from 'lucide-react';
import { api } from '../services/api';
import { ReviewIntelligenceSummary } from '../types';

interface AIReviewSummaryCardProps {
  productId: number;
}

export const AIReviewSummaryCard: React.FC<AIReviewSummaryCardProps> = ({ productId }) => {
  const [summary, setSummary] = useState<ReviewIntelligenceSummary | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    api.getReviewIntelligence(productId)
      .then((data) => {
        if (isMounted) {
          setSummary(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (isMounted) {
          setError(err.message || 'Failed to load AI review intelligence');
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [productId]);

  if (loading) {
    return (
      <div className="p-6 bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-slate-700 rounded-3xl animate-pulse space-y-4 my-8">
        <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded w-1/3"></div>
        <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-3/4"></div>
        <div className="grid grid-cols-2 gap-4 pt-4">
          <div className="h-16 bg-slate-200 dark:bg-slate-700 rounded-xl"></div>
          <div className="h-16 bg-slate-200 dark:bg-slate-700 rounded-xl"></div>
        </div>
      </div>
    );
  }

  if (error || !summary) {
    return null;
  }

  const aspects = summary.aspect_breakdown ? Object.entries(summary.aspect_breakdown) : [];

  return (
    <div className="my-10 bg-gradient-to-br from-indigo-900/5 via-white to-blue-900/5 dark:from-slate-900 dark:via-slate-850 dark:to-slate-900 border border-indigo-100 dark:border-indigo-950/50 rounded-3xl p-6 sm:p-8 shadow-sm">
      
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-6 border-b border-slate-200/80 dark:border-slate-750">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-600 to-blue-600 flex items-center justify-center text-white shadow-md shadow-indigo-500/20">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-extrabold text-base sm:text-lg text-slate-900 dark:text-white flex items-center gap-2">
              AI Review Intelligence &amp; Consensus
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 bg-indigo-100 dark:bg-indigo-900/50 text-indigo-700 dark:text-indigo-300 rounded-full">
                Sentiment Engine
              </span>
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Synthesized from {summary.total_reviews_analyzed} customer reviews with NLP aspect extraction
            </p>
          </div>
        </div>

        {/* Badges */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center gap-1.5 px-3 py-1 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/40 rounded-full text-xs font-bold">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
            <span>{(summary.authenticity_score * 100).toFixed(0)}% Authenticity</span>
          </div>
          <div className="flex items-center gap-1 px-3 py-1 bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800/40 rounded-full text-xs font-semibold">
            <CheckCircle2 className="w-3.5 h-3.5 text-blue-500" />
            <span>{(summary.verified_purchase_ratio * 100).toFixed(0)}% Verified Buyers</span>
          </div>
          {summary.suspicious_review_count > 0 && (
            <div className="flex items-center gap-1 px-2.5 py-1 bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 border border-amber-200 rounded-full text-[11px] font-medium">
              <AlertTriangle className="w-3 h-3 text-amber-500" />
              <span>{summary.suspicious_review_count} Suspicious Filtered</span>
            </div>
          )}
        </div>
      </div>

      {/* AI Consensus Summary Paragraph */}
      <div className="mt-5 p-4 bg-white dark:bg-slate-800/90 rounded-2xl border border-slate-100 dark:border-slate-700/60 shadow-xs">
        <p className="text-sm text-slate-700 dark:text-slate-200 leading-relaxed font-medium">
          <span className="font-bold text-indigo-600 dark:text-indigo-400">Key Takeaway: </span>
          {summary.consensus_summary}
        </p>
      </div>

      {/* Pros & Cons Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
        
        {/* Pros */}
        <div className="p-4 bg-emerald-50/40 dark:bg-emerald-950/10 rounded-2xl border border-emerald-100 dark:border-emerald-900/30">
          <h4 className="text-xs font-bold text-emerald-800 dark:text-emerald-300 uppercase tracking-wider flex items-center gap-1.5 mb-3">
            <ThumbsUp className="w-3.5 h-3.5 text-emerald-600" />
            What Buyers Praised
          </h4>
          <div className="flex flex-wrap gap-2">
            {summary.top_pros && summary.top_pros.length > 0 ? (
              summary.top_pros.map((pro, idx) => (
                <span 
                  key={idx} 
                  className="text-xs px-2.5 py-1 bg-emerald-100/70 dark:bg-emerald-900/40 text-emerald-800 dark:text-emerald-200 rounded-xl font-medium"
                >
                  ✓ {pro}
                </span>
              ))
            ) : (
              <span className="text-xs text-slate-400">Consistently positive reception</span>
            )}
          </div>
        </div>

        {/* Cons */}
        <div className="p-4 bg-rose-50/40 dark:bg-rose-950/10 rounded-2xl border border-rose-100 dark:border-rose-900/30">
          <h4 className="text-xs font-bold text-rose-800 dark:text-rose-300 uppercase tracking-wider flex items-center gap-1.5 mb-3">
            <ThumbsDown className="w-3.5 h-3.5 text-rose-600" />
            Points to Consider
          </h4>
          <div className="flex flex-wrap gap-2">
            {summary.top_cons && summary.top_cons.length > 0 ? (
              summary.top_cons.map((con, idx) => (
                <span 
                  key={idx} 
                  className="text-xs px-2.5 py-1 bg-rose-100/70 dark:bg-rose-900/40 text-rose-800 dark:text-rose-200 rounded-xl font-medium"
                >
                  ⚠ {con}
                </span>
              ))
            ) : (
              <span className="text-xs text-slate-400">No major negative trends reported</span>
            )}
          </div>
        </div>

      </div>

      {/* Aspect Satisfaction Scores */}
      {aspects.length > 0 && (
        <div className="mt-6 pt-5 border-t border-slate-200/80 dark:border-slate-750">
          <h4 className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider flex items-center gap-1.5 mb-3">
            <BarChart3 className="w-3.5 h-3.5 text-indigo-500" />
            Aspect Satisfaction Breakdown
          </h4>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {aspects.map(([name, data]) => {
              const pct = Math.round(data.sentiment_score * 100);
              return (
                <div 
                  key={name} 
                  className="p-3 bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700/50 shadow-xs"
                >
                  <div className="flex justify-between items-center mb-1 text-xs">
                    <span className="font-bold text-slate-700 dark:text-slate-200 capitalize">
                      {name}
                    </span>
                    <span className={`font-extrabold ${
                      pct >= 80 ? 'text-emerald-600 dark:text-emerald-400' :
                      pct >= 60 ? 'text-blue-600 dark:text-blue-400' : 'text-amber-600'
                    }`}>
                      {pct}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-100 dark:bg-slate-700 h-1.5 rounded-full overflow-hidden">
                    <div 
                      className={`h-full rounded-full ${
                        pct >= 80 ? 'bg-emerald-500' : pct >= 60 ? 'bg-blue-500' : 'bg-amber-500'
                      }`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

    </div>
  );
};
