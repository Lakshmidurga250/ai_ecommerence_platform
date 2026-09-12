import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';
import { api } from '../services/api';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (credentialsOrEmail: any, password?: string) => Promise<void>;
  register: (userData: any) => Promise<void>;
  logout: () => void;
  isAdmin: boolean;
  isSeller: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      api.getMe()
        .then(setUser)
        .catch(() => {
          localStorage.removeItem('access_token');
          setUser(null);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (credentialsOrEmail: any, password?: string) => {
    const creds = typeof credentialsOrEmail === 'string'
      ? { email_or_username: credentialsOrEmail, password: password || '' }
      : credentialsOrEmail;
    await api.login(creds);
    const currentUser = await api.getMe();
    setUser(currentUser);
  };

  const register = async (userData: any) => {
    await api.register(userData);
    await login({ email_or_username: userData.email, password: userData.password });
  };

  const logout = () => {
    api.logout();
    setUser(null);
  };

  const roles = user?.roles || [];
  const isAdmin = roles.includes('ADMIN');
  const isSeller = roles.includes('SELLER') || isAdmin;

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, isAdmin, isSeller }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
