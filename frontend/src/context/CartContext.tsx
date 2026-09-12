import React, { createContext, useContext, useState, useEffect } from 'react';
import { Cart } from '../types';
import { api } from '../services/api';
import { useAuth } from './AuthContext';

interface CartContextType {
  cart: Cart | null;
  itemCount: number;
  loading: boolean;
  addToCart: (productId: number, quantity?: number) => Promise<void>;
  addItem: (productId: number, quantity?: number) => Promise<void>;
  updateQuantity: (itemId: number, quantity: number) => Promise<void>;
  removeItem: (itemId: number) => Promise<void>;
  applyCoupon: (code: string) => Promise<void>;
  refreshCart: () => Promise<void>;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(false);

  const refreshCart = async () => {
    if (!user) {
      setCart(null);
      return;
    }
    try {
      setLoading(true);
      const data = await api.getCart();
      setCart(data);
    } catch (e) {
      console.error("Failed to load cart", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshCart();
  }, [user]);

  const addToCart = async (productId: number, quantity: number = 1) => {
    if (!user) {
      alert("Please sign in to add items to your cart");
      return;
    }
    const updated = await api.addToCart(productId, quantity);
    setCart(updated);
    api.recordBehaviorEvent('CART_ADD', productId, { quantity });
  };

  const applyCoupon = async (code: string) => {
    const updated = await api.getCart(code);
    setCart(updated);
  };

  const updateQuantity = async (itemId: number, quantity: number) => {
    const updated = await api.updateCartItem(itemId, quantity);
    setCart(updated);
  };

  const removeItem = async (itemId: number) => {
    const updated = await api.removeCartItem(itemId);
    setCart(updated);
  };

  const itemCount = cart?.items?.reduce((sum, item) => sum + item.quantity, 0) || 0;

  return (
    <CartContext.Provider value={{ cart, itemCount, loading, addToCart, addItem: addToCart, updateQuantity, removeItem, applyCoupon, refreshCart }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within a CartProvider');
  return context;
};
