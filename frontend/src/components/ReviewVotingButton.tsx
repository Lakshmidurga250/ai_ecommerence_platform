import React, { useState } from 'react';
import { ThumbsUp, ThumbsDown } from 'lucide-react';
import { api } from '../services/api';

interface ReviewVotingButtonProps {
  reviewId: number;
  initialHelpfulCount?: number;
  initialUnhelpfulCount?: number;
}

export const ReviewVotingButton: React.FC<ReviewVotingButtonProps> = ({
  reviewId,
  initialHelpfulCount = 0,
  initialUnhelpfulCount = 0
}) => {
  const [helpfulCount, setHelpfulCount] = useState(initialHelpfulCount);
  const [unhelpfulCount, setUnhelpfulCount] = useState(initialUnhelpfulCount);
  const [userVote, setUserVote] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(false);

  const handleVote = async (isHelpful: boolean) => {
    if (loading) return;
    try {
      setLoading(true);
      const res = await api.voteReviewHelpfulness(reviewId, isHelpful);
      if (res) {
        setHelpfulCount(res.helpful_votes);
        setUnhelpfulCount(res.unhelpful_votes);
        setUserVote(isHelpful);
      }
    } catch (err) {
      console.error("Failed to submit review vote:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center gap-3 text-xs text-slate-500 dark:text-slate-400">
      <span className="font-medium">Was this review helpful?</span>

      {/* Helpful Button */}
      <button
        onClick={() => handleVote(true)}
        disabled={loading}
        className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg border transition-all ${
          userVote === true
            ? 'bg-blue-50 dark:bg-blue-950/60 border-blue-300 dark:border-blue-700 text-blue-600 dark:text-blue-400 font-bold'
            : 'border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800'
        }`}
        title="Vote Helpful"
      >
        <ThumbsUp className={`w-3.5 h-3.5 ${userVote === true ? 'text-blue-600 dark:text-blue-400' : ''}`} />
        <span>Yes ({helpfulCount})</span>
      </button>

      {/* Unhelpful Button */}
      <button
        onClick={() => handleVote(false)}
        disabled={loading}
        className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg border transition-all ${
          userVote === false
            ? 'bg-red-50 dark:bg-red-950/60 border-red-300 dark:border-red-700 text-red-600 dark:text-red-400 font-bold'
            : 'border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800'
        }`}
        title="Vote Unhelpful"
      >
        <ThumbsDown className={`w-3.5 h-3.5 ${userVote === false ? 'text-red-600 dark:text-red-400' : ''}`} />
        <span>No ({unhelpfulCount})</span>
      </button>
    </div>
  );
};
