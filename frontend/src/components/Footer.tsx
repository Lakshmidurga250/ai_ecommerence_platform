import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Cpu, RefreshCw, Truck } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-900 text-slate-300 pt-12 pb-8 border-t border-slate-800">
      {/* Value Propositions */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12 border-b border-slate-800">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="flex items-start gap-3.5">
            <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center flex-shrink-0">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-white">AI-Powered Shopping</h4>
              <p className="text-xs text-slate-400 mt-1">Multi-level collaborative and neural recommendation models tailored to your taste.</p>
            </div>
          </div>
          <div className="flex items-start gap-3.5">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center flex-shrink-0">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-white">Verified Multi-Vendor</h4>
              <p className="text-xs text-slate-400 mt-1">Direct from vetted brands and approved suppliers with genuine warranties.</p>
            </div>
          </div>
          <div className="flex items-start gap-3.5">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center flex-shrink-0">
              <Truck className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-white">Fast Carrier Logistics</h4>
              <p className="text-xs text-slate-400 mt-1">Multi-warehouse automated allocation with live carrier tracking updates.</p>
            </div>
          </div>
          <div className="flex items-start gap-3.5">
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center flex-shrink-0">
              <RefreshCw className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-white">Hassle-Free Returns</h4>
              <p className="text-xs text-slate-400 mt-1">Automated eligibility evaluation and instant refund simulations.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Footer Links */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 grid grid-cols-2 md:grid-cols-4 gap-8 text-xs">
        <div>
          <h5 className="text-white font-bold mb-3 tracking-wider uppercase text-[11px]">Marketplace</h5>
          <ul className="space-y-2">
            <li><Link to="/products" className="hover:text-white transition-colors">All Products</Link></li>
            <li><Link to="/products?sort_by=popular" className="hover:text-white transition-colors">Trending Items</Link></li>
            <li><Link to="/products?category_id=1" className="hover:text-white transition-colors">Laptops & Computing</Link></li>
            <li><Link to="/products?category_id=4" className="hover:text-white transition-colors">Footwear & Running</Link></li>
          </ul>
        </div>
        <div>
          <h5 className="text-white font-bold mb-3 tracking-wider uppercase text-[11px]">AI Technologies</h5>
          <ul className="space-y-2 text-slate-400">
            <li>Hybrid Collaborative Filtering</li>
            <li>Time-Series Demand Forecasting</li>
            <li>Isolation Forest Fraud Anomaly</li>
            <li>K-Means RFM Customer Segmentation</li>
            <li>NLP Lexical Sentiment Analysis</li>
          </ul>
        </div>
        <div>
          <h5 className="text-white font-bold mb-3 tracking-wider uppercase text-[11px]">Portals</h5>
          <ul className="space-y-2">
            <li><Link to="/orders" className="hover:text-white transition-colors">Customer Orders</Link></li>
            <li><Link to="/wishlist" className="hover:text-white transition-colors">Saved Wishlist</Link></li>
            <li><Link to="/seller/dashboard" className="hover:text-white transition-colors">Seller Center</Link></li>
            <li><Link to="/admin/dashboard" className="hover:text-white transition-colors">Admin Console</Link></li>
          </ul>
        </div>
        <div>
          <h5 className="text-white font-bold mb-3 tracking-wider uppercase text-[11px]">Engineering Architecture</h5>
          <p className="text-slate-400 leading-relaxed">
            Built as an enterprise-grade AI e-commerce platform using React, TypeScript, Vite, Tailwind CSS, FastAPI, PostgreSQL, and Scikit-Learn.
          </p>
        </div>
      </div>

      {/* Copyright */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 border-t border-slate-800 text-center text-xs text-slate-500">
        <p>&copy; 2026 AI E-Commerce & Recommendation Platform. Educational & Portfolio Project.</p>
      </div>
    </footer>
  );
};
