import React, { useState, useEffect } from 'react';
import { HelpCircle, MessageSquare, CheckCircle, Send, PlusCircle, Sparkles } from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';

interface ProductQnASectionProps {
  productId: number;
}

export const ProductQnASection: React.FC<ProductQnASectionProps> = ({ productId }) => {
  const { user } = useAuth();
  const [questions, setQuestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isAsking, setIsAsking] = useState(false);
  const [newQuestionText, setNewQuestionText] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);

  useEffect(() => {
    loadQuestions();
  }, [productId]);

  const loadQuestions = async () => {
    try {
      setLoading(true);
      const data = await api.getProductQnA(productId);
      setQuestions(data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleAskSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newQuestionText.trim()) return;

    try {
      setSubmitting(true);
      await api.askProductQuestion(productId, newQuestionText.trim());
      setFeedback("Thank you! Your question has been posted to our community.");
      setNewQuestionText('');
      setIsAsking(false);
      loadQuestions();
      setTimeout(() => setFeedback(null), 4000);
    } catch (err: any) {
      setFeedback(err.message || "Failed to submit question. Please ensure you are logged in.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 sm:p-8 border border-slate-200 dark:border-slate-800 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100 dark:border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 bg-blue-100 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 rounded-xl">
              <HelpCircle className="w-5 h-5" />
            </span>
            <h2 className="text-xl font-bold text-slate-900 dark:text-white">Customer Questions & Answers</h2>
          </div>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Real inquiries answered by verified sellers and community shoppers
          </p>
        </div>

        <button
          onClick={() => setIsAsking(!isAsking)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded-xl shadow-sm transition-all hover:scale-[1.02]"
        >
          <PlusCircle className="w-4 h-4" />
          Ask a Question
        </button>
      </div>

      {feedback && (
        <div className="my-4 p-3 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 text-sm rounded-xl border border-emerald-200">
          {feedback}
        </div>
      )}

      {/* Ask Question Form */}
      {isAsking && (
        <form onSubmit={handleAskSubmit} className="my-6 p-4 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
          <label className="block text-sm font-semibold text-slate-800 dark:text-slate-200 mb-2">
            Have a question about specifications, compatibility, or warranty?
          </label>
          <textarea
            value={newQuestionText}
            onChange={(e) => setNewQuestionText(e.target.value)}
            placeholder="e.g. Does this laptop come with a stylus pen included in the box?"
            rows={3}
            className="w-full px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-900 dark:text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <div className="flex justify-end gap-3 mt-3">
            <button
              type="button"
              onClick={() => setIsAsking(false)}
              className="px-4 py-2 text-sm text-slate-600 dark:text-slate-400 hover:text-slate-900"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting || !newQuestionText.trim()}
              className="flex items-center gap-1.5 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-sm font-semibold rounded-xl"
            >
              <Send className="w-3.5 h-3.5" />
              {submitting ? 'Submitting...' : 'Post Question'}
            </button>
          </div>
        </form>
      )}

      {/* Question List */}
      <div className="mt-6 space-y-6">
        {loading ? (
          <div className="py-8 text-center text-sm text-slate-400">Loading community questions...</div>
        ) : questions.length === 0 ? (
          <div className="py-8 text-center text-slate-500 dark:text-slate-400">
            <MessageSquare className="w-8 h-8 mx-auto text-slate-300 mb-2" />
            <p className="font-medium text-sm">No questions asked yet.</p>
            <p className="text-xs text-slate-400 mt-0.5">Be the first to ask the seller about this product!</p>
          </div>
        ) : (
          questions.map((q) => (
            <div key={q.id} className="border-b border-slate-100 dark:border-slate-800 pb-5 last:border-0">
              <div className="flex items-start gap-3">
                <span className="font-extrabold text-blue-600 dark:text-blue-400 text-sm mt-0.5">Q:</span>
                <div className="flex-1">
                  <h4 className="font-semibold text-slate-900 dark:text-white text-sm">{q.question}</h4>
                  <p className="text-xs text-slate-400 mt-0.5">Asked by {q.asked_by}</p>

                  {/* Answers */}
                  <div className="mt-3 space-y-3">
                    {q.answers && q.answers.length > 0 ? (
                      q.answers.map((a: any) => (
                        <div key={a.id} className="flex items-start gap-3 bg-slate-50 dark:bg-slate-800/40 p-3 rounded-xl border border-slate-100 dark:border-slate-800">
                          <span className="font-extrabold text-emerald-600 dark:text-emerald-400 text-sm mt-0.5">A:</span>
                          <div className="flex-1">
                            <p className="text-sm text-slate-800 dark:text-slate-200">{a.answer}</p>
                            <div className="flex items-center gap-2 mt-1.5">
                              {a.is_seller_reply && (
                                <span className="flex items-center gap-1 text-[11px] font-bold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/60 px-2 py-0.5 rounded-md">
                                  <CheckCircle className="w-3 h-3 text-blue-500" />
                                  Verified Seller
                                </span>
                              )}
                              <span className="text-xs text-slate-400">By {a.answered_by}</span>
                            </div>
                          </div>
                        </div>
                      ))
                    ) : (
                      <p className="text-xs italic text-slate-400">Waiting for seller reply...</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
