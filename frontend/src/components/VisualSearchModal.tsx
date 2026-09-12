import React, { useState } from 'react';
import { X, Upload, Camera, Sparkles, ArrowRight, CheckCircle, Image as ImageIcon, Loader2 } from 'lucide-react';
import { api } from '../services/api';
import { VisualMatch } from '../types';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';

interface VisualSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const PRESET_SAMPLES = [
  {
    name: 'Wireless Earbuds',
    url: 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&auto=format&fit=crop',
    category: 'Electronics'
  },
  {
    name: 'Athletic Running Shoes',
    url: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&auto=format&fit=crop',
    category: 'Footwear'
  },
  {
    name: 'Analog Quartz Watch',
    url: 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=500&auto=format&fit=crop',
    category: 'Accessories'
  },
  {
    name: 'Cotton Oxford Shirt',
    url: 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500&auto=format&fit=crop',
    category: 'Clothing'
  }
];

export const VisualSearchModal: React.FC<VisualSearchModalProps> = ({ isOpen, onClose }) => {
  const [imageUrl, setImageUrl] = useState('');
  const [imageBase64, setImageBase64] = useState<string | null>(null);
  const [previewSrc, setPreviewSrc] = useState<string | null>(null);
  const [categoryHint, setCategoryHint] = useState('');
  const [loading, setLoading] = useState(false);
  const [matches, setMatches] = useState<VisualMatch[]>([]);
  const [executionMs, setExecutionMs] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();
  const { addToCart } = useCart();

  if (!isOpen) return null;

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onloadend = () => {
      const result = reader.result as string;
      setImageBase64(result);
      setPreviewSrc(result);
      setImageUrl('');
    };
    reader.readAsDataURL(file);
  };

  const handlePresetSelect = (preset: typeof PRESET_SAMPLES[0]) => {
    setImageUrl(preset.url);
    setPreviewSrc(preset.url);
    setImageBase64(null);
    setCategoryHint(preset.category);
  };

  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!imageUrl && !imageBase64) {
      setError('Please upload an image or provide an image URL');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await api.visualSearch({
        image_url: imageUrl || undefined,
        image_base64: imageBase64 || undefined,
        category_hint: categoryHint || undefined,
        top_k: 6,
      });

      setMatches(response.matches || []);
      setExecutionMs(response.execution_ms);
    } catch (err: any) {
      setError(err.message || 'Visual search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleProductClick = (productId: number) => {
    onClose();
    navigate(`/product/${productId}`);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="bg-white rounded-3xl shadow-2xl max-w-3xl w-full max-h-[90vh] flex flex-col border border-slate-100 overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="px-6 py-4 bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-800 text-white flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="p-2 bg-white/10 rounded-xl">
              <Camera className="w-5 h-5 text-cyan-300" />
            </div>
            <div>
              <h3 className="font-bold text-lg flex items-center gap-2">
                AI Visual Search Engine
                <span className="text-[10px] uppercase font-extrabold px-2 py-0.5 bg-cyan-400 text-slate-900 rounded-full tracking-wider">
                  Neural Embedding
                </span>
              </h3>
              <p className="text-xs text-blue-100">Find matching products by uploading a photo or selecting a style</p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-1.5 rounded-full hover:bg-white/20 text-white/80 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Content */}
        <div className="p-6 overflow-y-auto flex-1 space-y-6">
          
          {/* Upload & Input Area */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            {/* Drop / Upload zone */}
            <div className="relative border-2 border-dashed border-slate-300 hover:border-blue-500 rounded-2xl p-4 flex flex-col items-center justify-center text-center bg-slate-50 hover:bg-blue-50/30 transition-all cursor-pointer min-h-[160px]">
              <input 
                type="file" 
                accept="image/*" 
                onChange={handleFileUpload}
                className="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
              />
              {previewSrc ? (
                <div className="relative w-full h-32 rounded-xl overflow-hidden shadow-inner bg-slate-200">
                  <img src={previewSrc} alt="Preview" className="w-full h-full object-cover" />
                  <div className="absolute bottom-1 right-1 bg-black/60 text-white text-[10px] px-2 py-0.5 rounded-full backdrop-blur-xs flex items-center gap-1">
                    <CheckCircle className="w-3 h-3 text-emerald-400" /> Image Selected
                  </div>
                </div>
              ) : (
                <div className="space-y-2">
                  <div className="w-10 h-10 mx-auto rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">
                    <Upload className="w-5 h-5" />
                  </div>
                  <div>
                    <span className="text-xs font-bold text-slate-700 block">Click or Drag photo here</span>
                    <span className="text-[11px] text-slate-400">Supports JPG, PNG, WEBP up to 5MB</span>
                  </div>
                </div>
              )}
            </div>

            {/* URL Input & Presets */}
            <div className="space-y-3 flex flex-col justify-between">
              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1">Or paste image URL:</label>
                <div className="flex gap-2">
                  <input
                    type="url"
                    value={imageUrl}
                    onChange={(e) => {
                      setImageUrl(e.target.value);
                      setPreviewSrc(e.target.value);
                      setImageBase64(null);
                    }}
                    placeholder="https://example.com/product.jpg"
                    className="flex-1 text-xs border border-slate-200 rounded-xl px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block mb-1.5">Try sample presets:</label>
                <div className="grid grid-cols-2 gap-2">
                  {PRESET_SAMPLES.map((preset, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => handlePresetSelect(preset)}
                      className="text-left p-1.5 rounded-xl border border-slate-200 hover:border-blue-400 hover:bg-blue-50/50 text-[11px] font-medium text-slate-700 flex items-center gap-2 transition-colors truncate"
                    >
                      <ImageIcon className="w-3.5 h-3.5 text-blue-500 flex-shrink-0" />
                      <span className="truncate">{preset.name}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Action Button */}
              <button
                type="button"
                onClick={() => handleSearch()}
                disabled={loading || (!imageUrl && !imageBase64)}
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 text-white font-bold text-xs py-2.5 px-4 rounded-xl shadow-md transition-all flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Extracting Visual Embeddings...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 text-cyan-200" />
                    Search Visually Now
                  </>
                )}
              </button>
            </div>
          </div>

          {error && (
            <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-xl">
              {error}
            </div>
          )}

          {/* Results Section */}
          {matches.length > 0 && (
            <div className="space-y-3 pt-4 border-t border-slate-100">
              <div className="flex items-center justify-between">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-600 flex items-center gap-2">
                  <span>Visual Similarity Matches</span>
                  <span className="bg-blue-100 text-blue-800 text-[10px] font-extrabold px-2 py-0.5 rounded-full">
                    {matches.length} found
                  </span>
                </h4>
                {executionMs && (
                  <span className="text-[11px] text-slate-400 font-mono">
                    Inference: {executionMs.toFixed(1)}ms
                  </span>
                )}
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                {matches.map((item) => (
                  <div
                    key={item.product_id}
                    className="border border-slate-200 rounded-2xl p-3 hover:border-blue-400 hover:shadow-md transition-all bg-white flex flex-col justify-between"
                  >
                    <div>
                      <div className="relative aspect-video rounded-xl overflow-hidden bg-slate-100 mb-2">
                        <img 
                          src={item.image_url || 'https://via.placeholder.com/300x200?text=Product'} 
                          alt={item.product_name}
                          className="w-full h-full object-cover" 
                        />
                        <div className="absolute top-1.5 left-1.5 bg-blue-600/90 text-white font-bold text-[10px] px-2 py-0.5 rounded-full shadow-sm">
                          {(item.similarity_score * 100).toFixed(0)}% Match
                        </div>
                        <div className="absolute bottom-1.5 right-1.5 bg-slate-900/80 text-cyan-300 font-mono text-[9px] px-1.5 py-0.5 rounded">
                          Color {(item.color_match_confidence * 100).toFixed(0)}%
                        </div>
                      </div>

                      <h5 
                        onClick={() => handleProductClick(item.product_id)}
                        className="text-xs font-bold text-slate-800 hover:text-blue-600 cursor-pointer line-clamp-1"
                      >
                        {item.product_name}
                      </h5>
                      <span className="text-[10px] text-slate-400 font-semibold uppercase block">
                        {item.category}
                      </span>
                      <p className="text-[11px] text-slate-500 mt-1 line-clamp-2 leading-relaxed">
                        {item.reasoning}
                      </p>
                    </div>

                    <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between">
                      <span className="text-xs font-extrabold text-slate-900">
                        ₹{item.price.toLocaleString('en-IN')}
                      </span>
                      <div className="flex gap-1.5">
                        <button
                          onClick={() => addToCart(item.product_id, 1)}
                          className="px-2 py-1 bg-slate-100 hover:bg-blue-50 text-blue-600 font-bold text-[10px] rounded-lg transition-colors"
                        >
                          + Cart
                        </button>
                        <button
                          onClick={() => handleProductClick(item.product_id)}
                          className="px-2 py-1 bg-blue-600 hover:bg-blue-700 text-white font-bold text-[10px] rounded-lg transition-colors flex items-center gap-1"
                        >
                          View <ArrowRight className="w-2.5 h-2.5" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>

        {/* Footer */}
        <div className="px-6 py-3 bg-slate-50 border-t border-slate-100 flex justify-between items-center text-[11px] text-slate-500">
          <span>Neural Vector Cosine Similarity & Color Geometry</span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-xl border border-slate-200 hover:bg-slate-100 text-slate-700 font-semibold text-xs"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
};
