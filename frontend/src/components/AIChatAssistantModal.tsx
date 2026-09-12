import React, { useState, useRef, useEffect } from 'react';
import {
  Bot, X, Send, Sparkles, ShoppingBag, ArrowRight, Loader2,
  Check, ThumbsUp, ThumbsDown, RotateCcw, Award, Package, ShieldCheck,
  TrendingUp, ShoppingCart
} from 'lucide-react';
import { ShoppingAssistantResponse, Product } from '../types';
import { api } from '../services/api';
import { useCart } from '../context/CartContext';
import { Link } from 'react-router-dom';

interface Message {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  response?: ShoppingAssistantResponse;
  suggestedActions?: Array<{ label: string; action: string; payload?: any }>;
  feedbackGiven?: 'up' | 'down' | null;
}

interface AIChatAssistantModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AIChatAssistantModal: React.FC<AIChatAssistantModalProps> = ({ isOpen, onClose }) => {
  const { addToCart } = useCart();
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState<string>(() => 'sess-' + Math.random().toString(36).substring(2, 10));
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'init-1',
      sender: 'assistant',
      text: 'Hello! I am your Autonomous AI Shopping Concierge.\n\nTell me what you need, for example:\n• "I need wireless headphones under ₹5,000 for gaming with good battery life."\n• "Compare boAt Rockerz with Sony headphones."\n• "Where is my latest order?"\n• "Add running shoes under ₹3,000 to my cart."',
      suggestedActions: [
        { label: 'Gaming Headphones < ₹5k', action: 'SEND_MESSAGE', payload: { text: 'I need wireless headphones under ₹5,000 for gaming with good battery life.' } },
        { label: 'Compare Top Earbuds', action: 'SEND_MESSAGE', payload: { text: 'Compare top wireless earbuds in our catalog' } },
        { label: 'Track My Orders', action: 'SEND_MESSAGE', payload: { text: 'Where is my order?' } }
      ]
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [addedItems, setAddedItems] = useState<{ [id: number]: boolean }>({});
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const handleResetChat = () => {
    const newSess = 'sess-' + Math.random().toString(36).substring(2, 10);
    setSessionId(newSess);
    setMessages([
      {
        id: 'init-reset-' + Date.now(),
        sender: 'assistant',
        text: 'Session reset! How can I assist you with your shopping today? Ask for any product, budget, comparison, or order lookup.',
        suggestedActions: [
          { label: 'Headphones under ₹5,000 for gaming', action: 'SEND_MESSAGE', payload: { text: 'I need wireless headphones under ₹5,000 for gaming with good battery life.' } },
          { label: 'Compare boAt with Sony', action: 'SEND_MESSAGE', payload: { text: 'Compare boAt with Sony headphones' } }
        ]
      }
    ]);
  };

  const handleAddToCart = async (productId: number, e?: React.MouseEvent) => {
    if (e) e.stopPropagation();
    try {
      await addToCart(productId, 1);
      setAddedItems((prev) => ({ ...prev, [productId]: true }));
      setTimeout(() => {
        setAddedItems((prev) => ({ ...prev, [productId]: false }));
      }, 2500);
    } catch (err) {
      console.error(err);
    }
  };

  const handleFeedback = async (msgId: string, isPositive: boolean) => {
    try {
      await api.sendShoppingAgentFeedback(sessionId, isPositive);
      setMessages((prev) =>
        prev.map((m) => (m.id === msgId ? { ...m, feedbackGiven: isPositive ? 'up' : 'down' } : m))
      );
    } catch (err) {
      console.error(err);
    }
  };

  const handleSend = async (queryText?: string) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || loading) return;

    const userMsgId = 'usr-' + Date.now();
    const userMsg: Message = { id: userMsgId, sender: 'user', text: textToSend };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await api.chatAssistant(textToSend, sessionId);
      const asstMsgId = 'asst-' + Date.now();

      setMessages((prev) => [
        ...prev,
        {
          id: asstMsgId,
          sender: 'assistant',
          text: response.assistant_reply,
          response: response,
          suggestedActions: response.action_pills || []
        },
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: 'err-' + Date.now(),
          sender: 'assistant',
          text: "I experienced a brief connection hiccup while querying our neural catalog. Please try again or browse our categories.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const samplePrompts = [
    'I need wireless headphones under ₹5,000 for gaming with good battery life.',
    'Compare boAt Rockerz with Sony headphones',
    'Add to cart the first headphones',
    'Where is my order status?',
    'Running shoes under ₹3,500'
  ];

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center sm:justify-end sm:p-6 bg-slate-900/60 backdrop-blur-sm transition-opacity">
      <div className="bg-white dark:bg-slate-900 w-full sm:w-[500px] h-[90vh] sm:h-[680px] rounded-t-3xl sm:rounded-3xl shadow-2xl flex flex-col overflow-hidden border border-slate-200 dark:border-slate-800 animate-in slide-in-from-bottom-5">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 via-indigo-700 to-purple-700 p-3.5 text-white flex items-center justify-between shadow-md">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-white/20 flex items-center justify-center backdrop-blur-md">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-1.5 font-bold text-sm">
                <span>AI Shopping Concierge</span>
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              </div>
              <p className="text-[10px] text-indigo-100 font-normal">
                Autonomous Commerce • Grounded Catalog • Live Cart Actions
              </p>
            </div>
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={handleResetChat}
              title="Reset conversation (New Chat)"
              className="p-1.5 rounded-lg text-white/80 hover:text-white hover:bg-white/15 transition-colors flex items-center gap-1 text-[11px] font-medium"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">New Chat</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-white/80 hover:text-white hover:bg-white/15 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Message Stream */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 text-sm bg-slate-50/50 dark:bg-slate-950/50">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
            >
              <div
                className={`max-w-[92%] p-3.5 rounded-2xl ${
                  msg.sender === 'user'
                    ? 'bg-indigo-600 text-white rounded-br-none shadow-sm'
                    : 'bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-bl-none border border-slate-200 dark:border-slate-700/60 shadow-sm'
                }`}
              >
                <p className="whitespace-pre-wrap leading-relaxed text-xs sm:text-sm">{msg.text}</p>

                {/* Extracted Requirements Chips */}
                {msg.response?.extracted_requirements && Object.keys(msg.response.extracted_requirements).length > 0 && (
                  <div className="mt-2.5 pt-2 border-t border-slate-100 dark:border-slate-700/60">
                    <div className="text-[10px] font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider mb-1 flex items-center gap-1">
                      <Sparkles className="w-3 h-3" /> Extracted Requirements
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {msg.response.extracted_requirements.category_name && (
                        <span className="text-[10px] bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 font-semibold px-2 py-0.5 rounded-md border border-indigo-200/50">
                          Category: {msg.response.extracted_requirements.category_name}
                        </span>
                      )}
                      {msg.response.extracted_requirements.max_budget && (
                        <span className="text-[10px] bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 font-semibold px-2 py-0.5 rounded-md border border-emerald-200/50">
                          Budget: ≤ ₹{msg.response.extracted_requirements.max_budget.toLocaleString()}
                        </span>
                      )}
                      {msg.response.extracted_requirements.use_case && (
                        <span className="text-[10px] bg-purple-50 dark:bg-purple-950/60 text-purple-700 dark:text-purple-300 font-semibold px-2 py-0.5 rounded-md border border-purple-200/50">
                          Use Case: {msg.response.extracted_requirements.use_case}
                        </span>
                      )}
                      {msg.response.extracted_requirements.requirements?.map((req, rIdx) => (
                        <span key={rIdx} className="text-[10px] bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 font-semibold px-2 py-0.5 rounded-md border border-amber-200/50">
                          Req: {req}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Side-by-Side Product Comparison Table */}
                {msg.response?.comparison_table && msg.response.comparison_table.products && msg.response.comparison_table.products.length >= 2 && (
                  <div className="mt-3 pt-2.5 border-t border-slate-100 dark:border-slate-700/60 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                        Side-by-Side Specification Comparison
                      </span>
                    </div>

                    {/* Winner Banner */}
                    {msg.response.comparison_table.winner && (
                      <div className="p-2.5 rounded-xl bg-gradient-to-r from-amber-500/10 via-indigo-500/10 to-purple-500/10 border border-amber-500/30 flex items-start gap-2">
                        <Award className="w-4 h-4 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
                        <div className="text-[11px] leading-tight text-slate-800 dark:text-slate-200 font-medium">
                          {msg.response.comparison_table.winner.verdict}
                        </div>
                      </div>
                    )}

                    {/* Comparison Grid */}
                    <div className="overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-700">
                      <table className="w-full text-left text-[11px]">
                        <thead className="bg-slate-100 dark:bg-slate-750 text-slate-700 dark:text-slate-300 font-bold">
                          <tr>
                            <th className="p-2">Feature</th>
                            {msg.response.comparison_table.products.map((cp: any) => (
                              <th key={cp.product_id} className="p-2 max-w-[120px] truncate">
                                {cp.name}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
                          {msg.response.comparison_table.comparison_rows?.map((row, rIdx) => (
                            <tr key={rIdx} className={rIdx % 2 === 0 ? 'bg-white dark:bg-slate-800' : 'bg-slate-50/50 dark:bg-slate-800/50'}>
                              <td className="p-2 font-semibold text-slate-600 dark:text-slate-400">{row.feature}</td>
                              {row.values.map((v, vIdx) => (
                                <td key={vIdx} className="p-2 font-medium text-slate-800 dark:text-slate-200">
                                  {v}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {/* Grounded Suggested Actions & Action Pills */}
                {msg.suggestedActions && msg.suggestedActions.length > 0 && (
                  <div className="mt-3 pt-2 border-t border-slate-100 dark:border-slate-700/60 flex flex-wrap gap-1.5">
                    {msg.suggestedActions.map((act, i) => (
                      <button
                        key={i}
                        onClick={() => {
                          if (act.action === 'SEND_MESSAGE' || act.action === 'search') {
                            handleSend(act.payload?.text || act.payload?.q || act.label);
                          } else if (act.action === 'add_to_cart' && act.payload?.product_id) {
                            handleAddToCart(act.payload.product_id);
                          } else if (act.action === 'view_product' && act.payload?.slug) {
                            onClose();
                            window.location.href = `/product/${act.payload.slug}`;
                          } else if (act.action === 'navigate' && act.payload?.path) {
                            onClose();
                            window.location.href = act.payload.path;
                          } else {
                            handleSend(act.label);
                          }
                        }}
                        className="text-[11px] bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 font-semibold px-2.5 py-1 rounded-lg border border-indigo-200/60 hover:bg-indigo-100 dark:hover:bg-indigo-900 transition-colors flex items-center gap-1"
                      >
                        <Sparkles className="w-3 h-3 text-indigo-500" />
                        <span>{act.label}</span>
                      </button>
                    ))}
                  </div>
                )}

                {/* Grounded Feedback buttons */}
                {msg.sender === 'assistant' && (
                  <div className="mt-2 pt-1 flex items-center justify-between text-[10px] text-slate-400 border-t border-slate-100 dark:border-slate-700/40">
                    <div className="flex items-center gap-1">
                      <ShieldCheck className="w-3 h-3 text-emerald-500" />
                      <span>Verified Catalog Truth</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <span>Was this helpful?</span>
                      <button
                        onClick={() => handleFeedback(msg.id, true)}
                        className={`p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-700 ${msg.feedbackGiven === 'up' ? 'text-emerald-500 font-bold' : 'text-slate-400'}`}
                        title="Helpful"
                      >
                        <ThumbsUp className="w-3 h-3" />
                      </button>
                      <button
                        onClick={() => handleFeedback(msg.id, false)}
                        className={`p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-700 ${msg.feedbackGiven === 'down' ? 'text-rose-500 font-bold' : 'text-slate-400'}`}
                        title="Not helpful"
                      >
                        <ThumbsDown className="w-3 h-3" />
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* Grounded Product Recommendation Cards Carousel */}
              {msg.response?.grounded_products && msg.response.grounded_products.length > 0 && (
                <div className="w-full mt-2.5 space-y-1.5">
                  <div className="text-[11px] font-bold text-slate-500 dark:text-slate-400 flex items-center justify-between px-1">
                    <span className="flex items-center gap-1">
                      <ShoppingBag className="w-3.5 h-3.5 text-indigo-500" />
                      Recommended Catalog Matches ({msg.response.grounded_products.length})
                    </span>
                    <span className="text-[10px] text-indigo-600 font-medium">100% In Stock</span>
                  </div>

                  <div className="flex gap-3 overflow-x-auto pb-2 no-scrollbar">
                    {msg.response.grounded_products.map((p: any) => {
                      const isAdded = !!addedItems[p.id];
                      return (
                        <div
                          key={p.id}
                          className="flex-shrink-0 w-52 bg-white dark:bg-slate-800 p-3 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm flex flex-col justify-between hover:border-indigo-400 transition-all group"
                        >
                          <div className="relative aspect-square w-full rounded-xl overflow-hidden bg-slate-100 dark:bg-slate-900 mb-2">
                            <img
                              src={
                                p.images && p.images.length > 0
                                  ? p.images[0].image_url
                                  : p.image_url || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300'
                              }
                              alt={p.name}
                              className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                            />
                            <div className="absolute top-1.5 right-1.5 px-1.5 py-0.5 rounded-full bg-slate-900/80 text-white text-[10px] font-bold backdrop-blur-sm">
                              ★ {p.rating?.toFixed(1) || '4.5'}
                            </div>
                          </div>

                          <div>
                            <h4 className="text-xs font-bold text-slate-900 dark:text-slate-100 line-clamp-2 mb-1">
                              {p.name}
                            </h4>
                            {p.explanation && (
                              <p className="text-[10px] text-slate-500 dark:text-slate-400 line-clamp-2 mb-2 italic">
                                {p.explanation}
                              </p>
                            )}
                          </div>

                          <div className="pt-2 border-t border-slate-100 dark:border-slate-700 flex items-center justify-between mt-auto">
                            <div>
                              <span className="text-xs font-black text-indigo-600 dark:text-indigo-400">
                                ₹{Math.round(p.price).toLocaleString()}
                              </span>
                            </div>

                            <div className="flex items-center gap-1.5">
                              <Link
                                to={`/product/${p.slug}`}
                                onClick={onClose}
                                className="p-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 text-xs transition-colors"
                                title="View Product Details"
                              >
                                <ArrowRight className="w-3.5 h-3.5" />
                              </Link>
                              <button
                                onClick={(e) => handleAddToCart(p.id, e)}
                                className={`p-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1 ${
                                  isAdded
                                    ? 'bg-emerald-600 text-white'
                                    : 'bg-indigo-600 hover:bg-indigo-700 text-white'
                                }`}
                                title="Add to Cart"
                              >
                                {isAdded ? <Check className="w-3.5 h-3.5" /> : <ShoppingCart className="w-3.5 h-3.5" />}
                              </button>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-slate-400 text-xs p-2">
              <Loader2 className="w-4 h-4 animate-spin text-indigo-600" />
              <span>Analyzing catalog truth, requirements, and ranking options...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Suggestion Chips */}
        {messages.length <= 2 && (
          <div className="px-3 py-2 border-t border-slate-100 dark:border-slate-800 flex gap-1.5 overflow-x-auto bg-slate-50 dark:bg-slate-900 no-scrollbar">
            {samplePrompts.map((prompt, i) => (
              <button
                key={i}
                onClick={() => handleSend(prompt)}
                className="text-[11px] whitespace-nowrap px-2.5 py-1 rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:border-indigo-500 hover:text-indigo-600 transition-colors shadow-2xs"
              >
                {prompt}
              </button>
            ))}
          </div>
        )}

        {/* Input Bar */}
        <div className="p-3 border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything: 'wireless headphones under ₹5,000 for gaming'..."
              className="flex-1 bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 px-3.5 py-2.5 rounded-xl text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 border border-transparent"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="p-2.5 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-40 disabled:hover:bg-indigo-600 transition-colors shadow-sm"
              title="Send Message"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
