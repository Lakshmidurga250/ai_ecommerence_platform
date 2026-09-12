import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Bot, Sparkles } from 'lucide-react';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { AIChatAssistantModal } from './components/AIChatAssistantModal';

// Pages
import { HomePage } from './pages/HomePage';
import { ProductListPage } from './pages/ProductListPage';
import { ProductDetailPage } from './pages/ProductDetailPage';
import { CartPage } from './pages/CartPage';
import { CheckoutPage } from './pages/CheckoutPage';
import { OrdersPage } from './pages/OrdersPage';
import { WishlistPage } from './pages/WishlistPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { SellerDashboardPage } from './pages/SellerDashboardPage';
import { AdminDashboardPage } from './pages/AdminDashboardPage';

export const App: React.FC = () => {
  const [isAIChatOpen, setIsAIChatOpen] = useState<boolean>(false);

  return (
    <AuthProvider>
      <CartProvider>
        <Router>
          <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 antialiased selection:bg-indigo-500 selection:text-white">
            <Navbar onOpenAIChat={() => setIsAIChatOpen(true)} />

            <main className="flex-1 flex flex-col">
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/products" element={<ProductListPage />} />
                <Route path="/product/:slug" element={<ProductDetailPage />} />
                <Route path="/cart" element={<CartPage />} />
                <Route path="/checkout" element={<CheckoutPage />} />
                <Route path="/orders" element={<OrdersPage />} />
                <Route path="/wishlist" element={<WishlistPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/seller/dashboard" element={<SellerDashboardPage />} />
                <Route path="/admin/dashboard" element={<AdminDashboardPage />} />
                {/* Fallback route */}
                <Route path="*" element={<HomePage />} />
              </Routes>
            </main>

            {/* Global Floating AI Shopping Concierge Trigger Button */}
            <div className="fixed bottom-6 right-6 z-40">
              <button
                onClick={() => setIsAIChatOpen(true)}
                className="group flex items-center gap-2.5 px-4 py-3 bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 bg-[length:200%_auto] hover:bg-right text-white rounded-full shadow-2xl shadow-indigo-600/40 hover:scale-105 transition-all duration-300 border border-white/20"
                title="Open AI Shopping Concierge"
              >
                <div className="relative">
                  <Bot className="w-5 h-5 text-white animate-bounce" />
                  <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-indigo-600" />
                </div>
                <span className="text-xs font-bold tracking-wide hidden sm:inline">Ask AI Concierge</span>
                <Sparkles className="w-3.5 h-3.5 text-purple-200" />
              </button>
            </div>

            {/* AI Chat Modal Dialog */}
            <AIChatAssistantModal isOpen={isAIChatOpen} onClose={() => setIsAIChatOpen(false)} />

            <Footer />
          </div>
        </Router>
      </CartProvider>
    </AuthProvider>
  );
};
