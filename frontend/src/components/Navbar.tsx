import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingCart, Heart, User as UserIcon, Search, Sparkles, LogOut, LayoutDashboard, Store, Shield } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { api } from '../services/api';

interface NavbarProps {
  onOpenAssistant?: () => void;
  onOpenAIChat?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onOpenAssistant, onOpenAIChat }) => {
  const handleOpenAssistant = () => {
    if (onOpenAIChat) onOpenAIChat();
    else if (onOpenAssistant) onOpenAssistant();
  };
  const { user, logout, isSeller, isAdmin } = useAuth();
  const { itemCount } = useCart();
  const navigate = useNavigate();

  const [searchQuery, setSearchQuery] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [categories, setCategories] = useState<any[]>([]);
  const searchRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api.getCategories().then(setCategories).catch(() => {});
  }, []);

  useEffect(() => {
    if (searchQuery.trim().length >= 2) {
      api.getSearchSuggestions(searchQuery.trim()).then(setSuggestions).catch(() => setSuggestions([]));
    } else {
      setSuggestions([]);
    }
  }, [searchQuery]);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(e.target as Node)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setShowSuggestions(false);
      navigate(`/products?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setSearchQuery(suggestion);
    setShowSuggestions(false);
    navigate(`/products?q=${encodeURIComponent(suggestion)}`);
  };

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-sm">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-blue-700 via-indigo-700 to-blue-800 text-white text-xs py-1.5 px-4 text-center font-medium flex justify-between items-center max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <span className="bg-white/20 text-white px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">AI Powered</span>
          <span>Next-Gen Multi-Vendor Marketplace with Neural Personalization</span>
        </div>
        <div className="flex gap-4">
          {isSeller && (
            <Link to="/seller/dashboard" className="hover:underline flex items-center gap-1">
              <Store className="w-3 h-3" /> Seller Center
            </Link>
          )}
          {isAdmin && (
            <Link to="/admin/dashboard" className="hover:underline flex items-center gap-1">
              <Shield className="w-3 h-3" /> Admin Console
            </Link>
          )}
        </div>
      </div>

      {/* Main Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between gap-4">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2.5 flex-shrink-0">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center text-white font-black text-xl shadow-md shadow-blue-500/20">
            AI
          </div>
          <div>
            <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
              OmniCommerce
            </span>
            <span className="text-[10px] block font-semibold text-blue-600 tracking-wider uppercase -mt-1">
              Intelligent Market
            </span>
          </div>
        </Link>

        {/* Search Bar with AI suggestions */}
        <div ref={searchRef} className="flex-1 max-w-2xl relative">
          <form onSubmit={handleSearchSubmit} className="relative flex items-center">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setShowSuggestions(true);
              }}
              onFocus={() => setShowSuggestions(true)}
              placeholder="Search products, brands, or try 'black running shoes under 4000'..."
              className="w-full bg-slate-100/80 hover:bg-slate-100 focus:bg-white border border-slate-300 focus:border-blue-500 rounded-full py-2.5 pl-11 pr-24 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all shadow-inner"
            />
            <Search className="w-4 h-4 text-slate-400 absolute left-4 pointer-events-none" />
            <button
              type="submit"
              className="absolute right-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-4 py-1.5 rounded-full transition-colors shadow-sm"
            >
              Search
            </button>
          </form>

          {/* Auto-complete Dropdown */}
          {showSuggestions && suggestions.length > 0 && (
            <div className="absolute top-full left-0 right-0 mt-1.5 bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden z-50 py-1.5">
              <div className="text-[11px] font-semibold text-slate-400 px-4 py-1 uppercase tracking-wider">Suggestions</div>
              {suggestions.map((s, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSuggestionClick(s)}
                  className="w-full text-left px-4 py-2 text-sm text-slate-700 hover:bg-blue-50 hover:text-blue-600 flex items-center gap-2 transition-colors"
                >
                  <Search className="w-3.5 h-3.5 text-slate-400" />
                  <span>{s}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-3">
          {/* AI Assistant Button */}
          <button
            onClick={handleOpenAssistant}
            className="flex items-center gap-1.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-xs font-bold px-3.5 py-2 rounded-full shadow-md shadow-blue-500/20 hover:from-blue-700 hover:to-indigo-700 transition-all transform hover:scale-[1.02]"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Ask AI Assistant</span>
          </button>

          {/* Wishlist */}
          <Link
            to="/wishlist"
            className="p-2 text-slate-600 hover:text-rose-600 hover:bg-slate-100 rounded-full transition-colors relative"
            title="Wishlist"
          >
            <Heart className="w-5 h-5" />
          </Link>

          {/* Cart */}
          <Link
            to="/cart"
            className="p-2 text-slate-600 hover:text-blue-600 hover:bg-slate-100 rounded-full transition-colors relative"
            title="Shopping Cart"
          >
            <ShoppingCart className="w-5 h-5" />
            {itemCount > 0 && (
              <span className="absolute -top-0.5 -right-0.5 bg-blue-600 text-white text-[10px] font-bold w-5 h-5 rounded-full flex items-center justify-center shadow-sm">
                {itemCount}
              </span>
            )}
          </Link>

          {/* User Account */}
          {user ? (
            <div className="relative group">
              <button className="flex items-center gap-1.5 p-1.5 text-slate-700 hover:bg-slate-100 rounded-lg text-sm font-medium transition-colors">
                <div className="w-8 h-8 rounded-full bg-slate-200 text-slate-700 font-bold flex items-center justify-center text-xs">
                  {user.username.slice(0, 2).toUpperCase()}
                </div>
                <span className="hidden md:inline text-xs font-semibold">{user.username}</span>
              </button>
              <div className="absolute right-0 top-full mt-1 w-48 bg-white border border-slate-200 rounded-xl shadow-xl py-1 hidden group-hover:block z-50">
                <div className="px-4 py-2 border-b border-slate-100">
                  <p className="text-xs font-bold text-slate-800">{user.username}</p>
                  <p className="text-[11px] text-slate-500 truncate">{user.email}</p>
                </div>
                <Link to="/account" className="block px-4 py-2 text-xs text-slate-700 hover:bg-slate-50 font-medium">
                  My Profile & Alerts
                </Link>
                <Link to="/orders" className="block px-4 py-2 text-xs text-slate-700 hover:bg-slate-50">
                  My Orders
                </Link>

                {isSeller && (
                  <Link to="/seller/dashboard" className="block px-4 py-2 text-xs text-blue-600 font-medium hover:bg-blue-50">
                    Seller Dashboard
                  </Link>
                )}
                {isAdmin && (
                  <Link to="/admin/dashboard" className="block px-4 py-2 text-xs text-indigo-600 font-medium hover:bg-indigo-50">
                    Admin Console
                  </Link>
                )}
                <button
                  onClick={logout}
                  className="w-full text-left px-4 py-2 text-xs text-rose-600 hover:bg-rose-50 flex items-center gap-1.5"
                >
                  <LogOut className="w-3.5 h-3.5" /> Sign Out
                </button>
              </div>
            </div>
          ) : (
            <Link
              to="/login"
              className="text-xs font-bold text-blue-600 border border-blue-600 hover:bg-blue-600 hover:text-white px-3.5 py-1.5 rounded-full transition-all"
            >
              Sign In
            </Link>
          )}
        </div>
      </div>

      {/* Category Pills Bar */}
      <div className="bg-slate-50 border-t border-slate-200/60 overflow-x-auto no-scrollbar">
        <div className="max-w-7xl mx-auto px-4 py-2 flex items-center gap-2">
          <Link
            to="/products"
            className="text-xs font-semibold px-3 py-1 rounded-full text-slate-700 hover:text-blue-600 hover:bg-white transition-all whitespace-nowrap"
          >
            All Products
          </Link>
          {categories.map((cat) => (
            <Link
              key={cat.id}
              to={`/products?category_id=${cat.id}`}
              className="text-xs font-medium px-3 py-1 rounded-full text-slate-600 hover:text-blue-600 hover:bg-white transition-all whitespace-nowrap"
            >
              {cat.name}
            </Link>
          ))}
        </div>
      </div>
    </header>
  );
};
