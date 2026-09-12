import React, { useState, useRef, useEffect } from 'react';
import { Bot, X, Send, Sparkles, ShoppingBag, ArrowRight, Loader2 } from 'lucide-react';
import { ShoppingAssistantResponse, Product } from '../types';
import { api } from '../services/api';
import { Link } from 'react-router-dom';

interface Message {
  sender: 'user' | 'assistant';
  text: string;
  response?: ShoppingAssistantResponse;
  suggestedActions?: Array<{ label: string; action: string; payload?: any }>;
}

interface AIChatAssistantModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AIChatAssistantModal: React.FC<AIChatAssistantModalProps> = ({ isOpen, onClose }) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: 'assistant',
      text: 'Hello! I am your AI Shopping & Support Concierge. Ask me about your orders, returns, platform shipping, or product recommendations like "Find headphones under $400".',
    },
  ]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const handleSend = async (queryText?: string) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || loading) return;

    const userMsg: Message = { sender: 'user', text: textToSend };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      let replyText = '';
      let suggestedActions: any[] = [];
      let shoppingResponse: any = null;

      try {
        const supportRes = await api.aiSupportChat(textToSend);
        if (supportRes && supportRes.intent !== 'GENERAL' && supportRes.reply) {
          replyText = supportRes.reply;
          suggestedActions = supportRes.suggested_actions || [];
        }
      } catch (e) {}

      if (!replyText) {
        const response = await api.chatAssistant(textToSend);
        replyText = response.assistant_reply;
        shoppingResponse = response;
      }

      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: replyText,
          response: shoppingResponse,
          suggestedActions: suggestedActions
        },
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'assistant',
          text: "I'm having trouble retrieving recommendations right now. Please try again or browse our catalog.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const samplePrompts = [
    'Where is my order?',
    'What is your return policy?',
    'Noise-cancelling headphones under $400',
    'How long does standard delivery take?',
  ];


  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center sm:justify-end sm:p-6 bg-slate-900/60 backdrop-blur-sm transition-opacity">
      <div className="bg-white dark:bg-slate-900 w-full sm:w-[480px] h-[85vh] sm:h-[640px] rounded-t-3xl sm:rounded-3xl shadow-2xl flex flex-col overflow-hidden border border-slate-200 dark:border-slate-800 animate-in slide-in-from-bottom-5">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 via-indigo-700 to-purple-700 p-4 text-white flex items-center justify-between shadow-md">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-white/20 flex items-center justify-center backdrop-blur-md">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-1.5 font-bold text-sm">
                <span>AI Shopping Concierge</span>
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              </div>
              <p className="text-[11px] text-indigo-100 font-normal">Grounded Catalog & Intent Engine</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Message Log */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 text-sm bg-slate-50/50 dark:bg-slate-950/50">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
            >
              <div
                className={`max-w-[85%] p-3.5 rounded-2xl ${
                  msg.sender === 'user'
                    ? 'bg-indigo-600 text-white rounded-br-none shadow-sm'
                    : 'bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 rounded-bl-none border border-slate-200 dark:border-slate-700/60 shadow-sm'
                }`}
              >
                <p className="whitespace-pre-wrap leading-relaxed">{msg.text}</p>

                {/* Grounded Suggested Actions */}
                {msg.suggestedActions && msg.suggestedActions.length > 0 && (
                  <div className="mt-3 pt-2 border-t border-slate-100 dark:border-slate-700/60 flex flex-wrap gap-1.5">
                    {msg.suggestedActions.map((act, i) => (
                      <button
                        key={i}
                        onClick={() => {
                          if (act.action === 'SEND_MESSAGE') {
                            handleSend(act.payload?.text || act.label);
                          } else if (act.action === 'NAVIGATE' && act.payload?.path) {
                            onClose();
                            window.location.href = act.payload.path;
                          }
                        }}
                        className="text-xs bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 font-semibold px-2.5 py-1 rounded-lg border border-indigo-200/60 hover:bg-indigo-100 transition-colors"
                      >
                        {act.label}
                      </button>
                    ))}
                  </div>
                )}

                {/* Intent Extraction Metadata */}
                {msg.response?.parsed_intent && (
                  <div className="mt-2.5 pt-2 border-t border-slate-100 dark:border-slate-700/60 text-[11px] space-y-1">
                    <div className="font-semibold text-indigo-600 dark:text-indigo-400 flex items-center gap-1">
                      <Sparkles className="w-3 h-3" /> Extracted Parameters:
                    </div>

                    <div className="flex flex-wrap gap-1 mt-1">
                      {msg.response.parsed_intent.extracted_brand && (
                        <span className="bg-slate-100 dark:bg-slate-700 px-1.5 py-0.5 rounded text-slate-700 dark:text-slate-300">
                          Brand: {msg.response.parsed_intent.extracted_brand}
                        </span>
                      )}
                      {msg.response.parsed_intent.extracted_category && (
                        <span className="bg-slate-100 dark:bg-slate-700 px-1.5 py-0.5 rounded text-slate-700 dark:text-slate-300">
                          Category: {msg.response.parsed_intent.extracted_category}
                        </span>
                      )}
                      {msg.response.parsed_intent.max_price && (
                        <span className="bg-slate-100 dark:bg-slate-700 px-1.5 py-0.5 rounded text-slate-700 dark:text-slate-300">
                          Max: ${msg.response.parsed_intent.max_price}
                        </span>
                      )}
                      {msg.response.parsed_intent.extracted_color && (
                        <span className="bg-slate-100 dark:bg-slate-700 px-1.5 py-0.5 rounded text-slate-700 dark:text-slate-300">
                          Color: {msg.response.parsed_intent.extracted_color}
                        </span>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* Grounded Products Carousel/Cards */}
              {msg.response?.grounded_products && msg.response.grounded_products.length > 0 && (
                <div className="w-full mt-2.5 space-y-2">
                  <div className="text-xs font-semibold text-slate-500 dark:text-slate-400 flex items-center gap-1">
                    <ShoppingBag className="w-3.5 h-3.5 text-indigo-500" /> Grounded Catalog Matches (
                    {msg.response.grounded_products.length})
                  </div>
                  <div className="flex gap-2.5 overflow-x-auto pb-2 scrollbar-none">
                    {msg.response.grounded_products.map((p: Product) => (
                      <Link
                        key={p.id}
                        to={`/product/${p.slug}`}
                        onClick={onClose}
                        className="flex-shrink-0 w-48 bg-white dark:bg-slate-800 p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 hover:border-indigo-500 transition-all group flex flex-col justify-between"
                      >
                        <div className="aspect-square w-full rounded-lg overflow-hidden bg-slate-100 dark:bg-slate-900 mb-2">
                          <img
                            src={
                              p.images && p.images.length > 0
                                ? p.images[0].image_url
                                : 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300'
                            }
                            alt={p.name}
                            className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                          />
                        </div>
                        <h4 className="text-xs font-semibold text-slate-800 dark:text-slate-200 line-clamp-2 mb-1">
                          {p.name}
                        </h4>
                        <div className="flex items-center justify-between text-xs font-bold text-indigo-600 dark:text-indigo-400 mt-auto pt-1">
                          <span>${p.price.toFixed(2)}</span>
                          <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                        </div>
                      </Link>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-slate-400 text-xs p-2">
              <Loader2 className="w-4 h-4 animate-spin text-indigo-600" />
              <span>Analyzing catalog and parsing intent...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Suggestion Chips */}
        {messages.length <= 2 && (
          <div className="px-4 py-2 border-t border-slate-100 dark:border-slate-800 flex gap-1.5 overflow-x-auto bg-slate-50 dark:bg-slate-900">
            {samplePrompts.map((prompt, i) => (
              <button
                key={i}
                onClick={() => handleSend(prompt)}
                className="text-[11px] whitespace-nowrap px-2.5 py-1 rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:border-indigo-500 hover:text-indigo-600 transition-colors"
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
              placeholder="Ask for advice, specs, or products..."
              className="flex-1 bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 px-3.5 py-2.5 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 border border-transparent"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={!input.trim() || loading}
              className="p-2.5 rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-40 disabled:hover:bg-indigo-600 transition-colors shadow-sm"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
