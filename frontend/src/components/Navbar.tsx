import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import {
  ShoppingCart, Heart, User as UserIcon, Search, Sparkles, LogOut,
  LayoutDashboard, Store, Shield, Camera, Menu, X, ChevronDown,
  Cpu, Layers, Bot, Compass, ShieldAlert, BarChart3, Package
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { api } from '../services/api';
import { VisualSearchModal } from './VisualSearchModal';

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
  const location = useLocation();

  const [searchQuery, setSearchQuery] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [categories, setCategories] = useState<any[]>([]);
  const [isVisualSearchOpen, setIsVisualSearchOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isAIDropdownOpen, setIsAIDropdownOpen] = useState(false);

  const searchRef = useRef<HTMLDivElement>(null);
  const aiDropdownRef = useRef<HTMLDivElement>(null);

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
      if (aiDropdownRef.current && !aiDropdownRef.current.contains(e.target as Node)) {
        setIsAIDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Close mobile drawer on route change
  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location.pathname]);

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

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="sticky top-0 z-40 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 shadow-sm">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-800 text-white text-xs py-1.5 px-4 font-medium">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span className="bg-white/20 text-white px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">AI Platform V3</span>
            <span className="hidden sm:inline">Autonomous Shopping Concierge & Neural Marketplace</span>
          </div>
          <div className="flex items-center gap-4 text-xs">
            {isSeller && (
              <Link to="/seller/dashboard" className={`hover:underline flex items-center gap-1 ${isActive('/seller/dashboard') ? 'font-bold underline' : ''}`}>
                <Store className="w-3 h-3" /> Seller Center
              </Link>
            )}
            {isAdmin && (
              <Link to="/admin/dashboard" className={`hover:underline flex items-center gap-1 ${isActive('/admin/dashboard') ? 'font-bold underline' : ''}`}>
                <Shield className="w-3 h-3" /> Admin Command Center
              </Link>
            )}
            {user && (
              <Link to="/account" className="hover:underline flex items-center gap-1 hidden md:flex">
                <UserIcon className="w-3 h-3" /> My Account
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Main Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex items-center justify-between gap-4">
        {/* Mobile menu toggle & Logo */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="p-2 rounded-lg text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800 md:hidden focus:outline-none"
            aria-label="Toggle Navigation Menu"
          >
            {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>

          <Link to="/" className="flex items-center gap-2.5 flex-shrink-0 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-700 flex items-center justify-center text-white font-black text-xl shadow-md shadow-indigo-500/20 group-hover:scale-105 transition-transform">
              AI
            </div>
            <div>
              <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-slate-900 to-indigo-950 dark:from-white dark:to-slate-200 bg-clip-text text-transparent">
                OmniCommerce
              </span>
              <span className="text-[10px] block font-bold text-indigo-600 dark:text-indigo-400 tracking-wider uppercase -mt-1">
                AI Autonomous Market
              </span>
            </div>
          </Link>
        </div>

        {/* Search Bar with AI suggestions & Visual Search */}
        <div ref={searchRef} className="flex-1 max-w-2xl relative hidden sm:block">
          <form onSubmit={handleSearchSubmit} className="relative flex items-center">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setShowSuggestions(true);
              }}
              onFocus={() => setShowSuggestions(true)}
              placeholder="Search catalog or ask 'wireless headphones under ₹5,000 for gaming'..."
              className="w-full bg-slate-100/90 dark:bg-slate-800/90 hover:bg-slate-100 dark:hover:bg-slate-800 focus:bg-white dark:focus:bg-slate-900 border border-slate-200 dark:border-slate-700 focus:border-indigo-500 rounded-full py-2.5 pl-11 pr-28 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 transition-all text-slate-800 dark:text-slate-100"
            />
            <Search className="w-4 h-4 text-slate-400 absolute left-4 pointer-events-none" />
            <div className="absolute right-1.5 flex items-center gap-1">
              <button
                type="button"
                onClick={() => setIsVisualSearchOpen(true)}
                title="Visual Search by Image (AI CLIP ViT)"
                className="p-1.5 text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-slate-700 rounded-full transition-colors"
              >
                <Camera className="w-4 h-4" />
              </button>
              <button
                type="submit"
                className="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold px-4 py-1.5 rounded-full transition-colors shadow-sm"
              >
                Search
              </button>
            </div>
          </form>

          {/* Auto-complete Dropdown */}
          {showSuggestions && suggestions.length > 0 && (
            <div className="absolute top-full left-0 right-0 mt-1.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl shadow-xl overflow-hidden z-50 py-1.5 animate-in fade-in-50">
              <div className="text-[11px] font-semibold text-slate-400 dark:text-slate-400 px-4 py-1 uppercase tracking-wider">Suggestions</div>
              {suggestions.map((s, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSuggestionClick(s)}
                  className="w-full text-left px-4 py-2 text-sm text-slate-700 dark:text-slate-200 hover:bg-indigo-50 dark:hover:bg-slate-700 hover:text-indigo-600 dark:hover:text-indigo-400 flex items-center gap-2 transition-colors"
                >
                  <Search className="w-3.5 h-3.5 text-slate-400" />
                  <span>{s}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Navigation Actions & Controls */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* AI Intelligence Hub Dropdown */}
          <div ref={aiDropdownRef} className="relative hidden lg:block">
            <button
              onClick={() => setIsAIDropdownOpen(!isAIDropdownOpen)}
              className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-200 hover:bg-indigo-50 dark:hover:bg-slate-800 hover:text-indigo-600 transition-colors border border-slate-200/80 dark:border-slate-700"
            >
              <Cpu className="w-3.5 h-3.5 text-indigo-600" />
              <span>AI Features</span>
              <ChevronDown className="w-3 h-3 text-slate-400" />
            </button>

            {isAIDropdownOpen && (
              <div className="absolute right-0 top-full mt-2 w-64 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl shadow-2xl p-2 z-50 animate-in fade-in-50">
                <div className="px-3 py-1.5 text-[11px] font-bold text-slate-400 uppercase tracking-wider">Intelligent AI Modules</div>
                <button
                  onClick={() => {
                    setIsAIDropdownOpen(false);
                    handleOpenAssistant();
                  }}
                  className="w-full text-left flex items-start gap-2.5 p-2.5 rounded-xl hover:bg-indigo-50 dark:hover:bg-slate-700 transition-colors"
                >
                  <div className="p-1.5 rounded-lg bg-indigo-100 dark:bg-indigo-900/60 text-indigo-600 dark:text-indigo-300">
                    <Bot className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-800 dark:text-slate-100">AI Shopping Concierge</div>
                    <p className="text-[11px] text-slate-500">Autonomous conversational product discovery</p>
                  </div>
                </button>

                <button
                  onClick={() => {
                    setIsAIDropdownOpen(false);
                    setIsVisualSearchOpen(true);
                  }}
                  className="w-full text-left flex items-start gap-2.5 p-2.5 rounded-xl hover:bg-indigo-50 dark:hover:bg-slate-700 transition-colors"
                >
                  <div className="p-1.5 rounded-lg bg-purple-100 dark:bg-purple-900/60 text-purple-600 dark:text-purple-300">
                    <Camera className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-800 dark:text-slate-100">Visual Product Search</div>
                    <p className="text-[11px] text-slate-500">Find products with image embeddings</p>
                  </div>
                </button>

                <Link
                  to="/products"
                  onClick={() => setIsAIDropdownOpen(false)}
                  className="w-full text-left flex items-start gap-2.5 p-2.5 rounded-xl hover:bg-indigo-50 dark:hover:bg-slate-700 transition-colors"
                >
                  <div className="p-1.5 rounded-lg bg-blue-100 dark:bg-blue-900/60 text-blue-600 dark:text-blue-300">
                    <Compass className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-800 dark:text-slate-100">Neural Product Catalog</div>
                    <p className="text-[11px] text-slate-500">Hybrid BM25 + Semantic ranking</p>
                  </div>
                </Link>

                {isAdmin && (
                  <Link
                    to="/admin/dashboard"
                    onClick={() => setIsAIDropdownOpen(false)}
                    className="w-full text-left flex items-start gap-2.5 p-2.5 rounded-xl hover:bg-indigo-50 dark:hover:bg-slate-700 transition-colors"
                  >
                    <div className="p-1.5 rounded-lg bg-rose-100 dark:bg-rose-900/60 text-rose-600 dark:text-rose-300">
                      <ShieldAlert className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="text-xs font-bold text-slate-800 dark:text-slate-100">Fraud & MLOps Console</div>
                      <p className="text-[11px] text-slate-500">Live drift, triage, & models</p>
                    </div>
                  </Link>
                )}
              </div>
            )}
          </div>

          {/* Quick AI Assistant Trigger */}
          <button
            onClick={handleOpenAssistant}
            className="flex items-center gap-1.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-xs font-bold px-3.5 py-2 rounded-xl shadow-md shadow-indigo-500/20 hover:from-indigo-700 hover:to-purple-700 transition-all transform hover:scale-[1.02]"
            title="Open AI Shopping Concierge"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Ask AI Concierge</span>
          </button>

          {/* Wishlist */}
          <Link
            to="/wishlist"
            className={`p-2 text-slate-600 dark:text-slate-300 hover:text-rose-600 dark:hover:text-rose-400 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition-colors relative ${isActive('/wishlist') ? 'text-rose-600 bg-rose-50 dark:bg-rose-950/40' : ''}`}
            title="Wishlist"
          >
            <Heart className="w-5 h-5" />
          </Link>

          {/* Cart */}
          <Link
            to="/cart"
            className={`p-2 text-slate-600 dark:text-slate-300 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition-colors relative ${isActive('/cart') ? 'text-indigo-600 bg-indigo-50 dark:bg-indigo-950/40' : ''}`}
            title="Shopping Cart"
          >
            <ShoppingCart className="w-5 h-5" />
            {itemCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-indigo-600 text-white text-[10px] font-bold w-5 h-5 rounded-full flex items-center justify-center shadow-sm">
                {itemCount}
              </span>
            )}
          </Link>

          {/* User Account */}
          {user ? (
            <div className="relative group">
              <button className="flex items-center gap-1.5 p-1 text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl text-sm font-medium transition-colors">
                <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-600 to-purple-600 text-white font-bold flex items-center justify-center text-xs shadow-sm">
                  {user.username.slice(0, 2).toUpperCase()}
                </div>
                <span className="hidden md:inline text-xs font-semibold">{user.username}</span>
              </button>
              <div className="absolute right-0 top-full mt-1 w-52 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl shadow-xl py-1 hidden group-hover:block z-50 animate-in fade-in-50">
                <div className="px-4 py-2 border-b border-slate-100 dark:border-slate-700">
                  <p className="text-xs font-bold text-slate-800 dark:text-slate-100">{user.username}</p>
                  <p className="text-[11px] text-slate-500 dark:text-slate-400 truncate">{user.email}</p>
                </div>
                <Link to="/account" className="block px-4 py-2 text-xs text-slate-700 dark:text-slate-200 hover:bg-indigo-50 dark:hover:bg-slate-700 font-medium">
                  Customer 360 & Alerts
                </Link>
                <Link to="/orders" className="block px-4 py-2 text-xs text-slate-700 dark:text-slate-200 hover:bg-indigo-50 dark:hover:bg-slate-700">
                  My Orders & Tracking
                </Link>

                {isSeller && (
                  <Link to="/seller/dashboard" className="block px-4 py-2 text-xs text-blue-600 dark:text-blue-400 font-medium hover:bg-blue-50 dark:hover:bg-slate-700">
                    Seller Dashboard
                  </Link>
                )}
                {isAdmin && (
                  <Link to="/admin/dashboard" className="block px-4 py-2 text-xs text-indigo-600 dark:text-indigo-400 font-medium hover:bg-indigo-50 dark:hover:bg-slate-700">
                    Admin Command Center
                  </Link>
                )}
                <button
                  onClick={logout}
                  className="w-full text-left px-4 py-2 text-xs text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-slate-700 flex items-center gap-1.5"
                >
                  <LogOut className="w-3.5 h-3.5" /> Sign Out
                </button>
              </div>
            </div>
          ) : (
            <Link
              to="/login"
              className="text-xs font-bold text-indigo-600 dark:text-indigo-400 border border-indigo-600 dark:border-indigo-400 hover:bg-indigo-600 hover:text-white px-3.5 py-1.5 rounded-xl transition-all"
            >
              Sign In
            </Link>
          )}
        </div>
      </div>

      {/* Mobile Search Bar (Visible only on mobile) */}
      <div className="px-4 pb-2 sm:hidden">
        <form onSubmit={handleSearchSubmit} className="relative flex items-center">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search catalog or ask AI..."
            className="w-full bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-full py-2 pl-9 pr-12 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
          />
          <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 pointer-events-none" />
          <button
            type="button"
            onClick={() => setIsVisualSearchOpen(true)}
            className="absolute right-2 p-1 text-slate-500 hover:text-indigo-600"
          >
            <Camera className="w-4 h-4" />
          </button>
        </form>
      </div>

      {/* Category Navigation Bar */}
      <div className="bg-slate-50/80 dark:bg-slate-900/80 border-t border-slate-200/60 dark:border-slate-800 overflow-x-auto no-scrollbar">
        <div className="max-w-7xl mx-auto px-4 py-2 flex items-center gap-2 text-xs">
          <Link
            to="/products"
            className={`font-semibold px-3 py-1 rounded-full transition-all whitespace-nowrap ${
              location.pathname === '/products' && !location.search
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'text-slate-700 dark:text-slate-300 hover:text-indigo-600 hover:bg-white dark:hover:bg-slate-800'
            }`}
          >
            All Products
          </Link>
          {categories.map((cat) => (
            <Link
              key={cat.id}
              to={`/products?category_id=${cat.id}`}
              className={`font-medium px-3 py-1 rounded-full transition-all whitespace-nowrap ${
                location.search.includes(`category_id=${cat.id}`)
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-600 dark:text-slate-300 hover:text-indigo-600 hover:bg-white dark:hover:bg-slate-800'
              }`}
            >
              {cat.name}
            </Link>
          ))}
        </div>
      </div>

      {/* Mobile Drawer Overlay & Panel */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-50 flex md:hidden bg-slate-900/60 backdrop-blur-sm animate-in fade-in-50">
          <div className="w-4/5 max-w-sm bg-white dark:bg-slate-900 h-full shadow-2xl flex flex-col p-5 overflow-y-auto">
            <div className="flex items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold text-sm">
                  AI
                </div>
                <span className="font-bold text-base text-slate-900 dark:text-white">OmniCommerce</span>
              </div>
              <button
                onClick={() => setIsMobileMenuOpen(false)}
                className="p-1.5 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* AI Assistant Banner in Mobile Drawer */}
            <div className="mt-4 p-3 rounded-2xl bg-gradient-to-r from-indigo-600 to-purple-600 text-white space-y-2 shadow-md">
              <div className="flex items-center gap-2 text-xs font-bold">
                <Bot className="w-4 h-4" />
                <span>AI Shopping Concierge</span>
              </div>
              <p className="text-[11px] text-indigo-100 leading-tight">
                Ask naturally about products, specs, budget filters, or orders.
              </p>
              <button
                onClick={() => {
                  setIsMobileMenuOpen(false);
                  handleOpenAssistant();
                }}
                className="w-full py-1.5 bg-white text-indigo-600 text-xs font-bold rounded-xl shadow-sm hover:bg-indigo-50 transition-colors"
              >
                Launch AI Concierge
              </button>
            </div>

            {/* Mobile Nav Links */}
            <div className="mt-5 space-y-1 text-sm font-medium">
              <Link
                to="/"
                className={`block px-3 py-2.5 rounded-xl ${isActive('/') ? 'bg-indigo-50 text-indigo-600 font-bold dark:bg-slate-800' : 'text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800'}`}
              >
                Home
              </Link>
              <Link
                to="/products"
                className={`block px-3 py-2.5 rounded-xl ${isActive('/products') ? 'bg-indigo-50 text-indigo-600 font-bold dark:bg-slate-800' : 'text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800'}`}
              >
                Catalog & Products
              </Link>
              <button
                onClick={() => {
                  setIsMobileMenuOpen(false);
                  setIsVisualSearchOpen(true);
                }}
                className="w-full text-left flex items-center justify-between px-3 py-2.5 rounded-xl text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
              >
                <span>Visual Product Search</span>
                <Camera className="w-4 h-4 text-purple-600" />
              </button>
              <Link
                to="/cart"
                className={`flex items-center justify-between px-3 py-2.5 rounded-xl ${isActive('/cart') ? 'bg-indigo-50 text-indigo-600 font-bold dark:bg-slate-800' : 'text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800'}`}
              >
                <span>Cart</span>
                {itemCount > 0 && <span className="px-2 py-0.5 text-xs bg-indigo-600 text-white rounded-full">{itemCount}</span>}
              </Link>
              <Link
                to="/wishlist"
                className={`block px-3 py-2.5 rounded-xl ${isActive('/wishlist') ? 'bg-indigo-50 text-indigo-600 font-bold dark:bg-slate-800' : 'text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800'}`}
              >
                Wishlist
              </Link>
              <Link
                to="/orders"
                className={`block px-3 py-2.5 rounded-xl ${isActive('/orders') ? 'bg-indigo-50 text-indigo-600 font-bold dark:bg-slate-800' : 'text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800'}`}
              >
                Orders & Tracking
              </Link>
              <Link
                to="/account"
                className={`block px-3 py-2.5 rounded-xl ${isActive('/account') ? 'bg-indigo-50 text-indigo-600 font-bold dark:bg-slate-800' : 'text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800'}`}
              >
                Customer 360 Account
              </Link>

              {isSeller && (
                <Link
                  to="/seller/dashboard"
                  className="block px-3 py-2.5 rounded-xl text-blue-600 font-bold hover:bg-blue-50 dark:hover:bg-slate-800"
                >
                  Seller Dashboard
                </Link>
              )}
              {isAdmin && (
                <Link
                  to="/admin/dashboard"
                  className="block px-3 py-2.5 rounded-xl text-purple-600 font-bold hover:bg-purple-50 dark:hover:bg-slate-800"
                >
                  Admin Command Center
                </Link>
              )}
            </div>

            {/* Mobile Auth Actions */}
            <div className="mt-auto pt-4 border-t border-slate-200 dark:border-slate-800">
              {user ? (
                <button
                  onClick={logout}
                  className="w-full py-2.5 px-4 text-center rounded-xl bg-rose-50 text-rose-600 font-bold text-xs hover:bg-rose-100 dark:bg-rose-950/40 transition-colors flex items-center justify-center gap-2"
                >
                  <LogOut className="w-4 h-4" /> Sign Out ({user.username})
                </button>
              ) : (
                <Link
                  to="/login"
                  className="w-full py-2.5 px-4 block text-center rounded-xl bg-indigo-600 text-white font-bold text-xs hover:bg-indigo-700 transition-colors shadow-sm"
                >
                  Sign In / Register
                </Link>
              )}
            </div>
          </div>
          <div className="flex-1" onClick={() => setIsMobileMenuOpen(false)} />
        </div>
      )}

      {/* Visual Search Modal */}
      <VisualSearchModal isOpen={isVisualSearchOpen} onClose={() => setIsVisualSearchOpen(false)} />
    </header>
  );
};

