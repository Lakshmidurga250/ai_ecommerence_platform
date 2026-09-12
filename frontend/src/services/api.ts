import { User, Product, Category, Cart, Order, RecommendationItem, ShoppingAssistantResponse, ParsedSearchIntent } from '../types';

const API_BASE = '/api/v1';

function getHeaders(): HeadersInit {
  const token = localStorage.getItem('access_token');
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    const message = errorData?.error?.message || errorData?.detail || `Request failed with status ${res.status}`;
    throw new Error(message);
  }
  if (res.status === 204) {
    return {} as T;
  }
  return res.json();
}

export const api = {
  // Auth
  async login(credentials: { email_or_username: string; password: string }) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    });
    const data = await handleResponse<{ access_token: string; refresh_token: string }>(res);
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    return data;
  },

  async register(userData: any) {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });
    return handleResponse<User>(res);
  },

  async getMe(): Promise<User> {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: getHeaders(),
    });
    return handleResponse<User>(res);
  },

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  // Products
  async getProducts(params?: Record<string, any>): Promise<Product[]> {
    const query = new URLSearchParams(params || {}).toString();
    const res = await fetch(`${API_BASE}/products/${query ? '?' + query : ''}`, {
      headers: getHeaders(),
    });
    return handleResponse<Product[]>(res);
  },

  async getProductBySlug(slug: string): Promise<Product> {
    const res = await fetch(`${API_BASE}/products/slug/${slug}`, {
      headers: getHeaders(),
    });
    return handleResponse<Product>(res);
  },

  async getCategories(): Promise<Category[]> {
    const res = await fetch(`${API_BASE}/categories/`, {
      headers: getHeaders(),
    });
    return handleResponse<Category[]>(res);
  },

  // Search
  async searchProducts(q: string): Promise<Product[]> {
    const res = await fetch(`${API_BASE}/search/?q=${encodeURIComponent(q)}`, {
      headers: getHeaders(),
    });
    return handleResponse<Product[]>(res);
  },

  async getSearchSuggestions(prefix: string): Promise<string[]> {
    if (prefix.length < 2) return [];
    const res = await fetch(`${API_BASE}/search/suggestions?prefix=${encodeURIComponent(prefix)}`, {
      headers: getHeaders(),
    });
    return handleResponse<string[]>(res);
  },

  // Cart
  async getCart(couponCode?: string): Promise<Cart> {
    const url = couponCode ? `${API_BASE}/cart/?coupon_code=${encodeURIComponent(couponCode)}` : `${API_BASE}/cart/`;
    const res = await fetch(url, {
      headers: getHeaders(),
    });
    return handleResponse<Cart>(res);
  },

  async addToCart(productId: number, quantity: number = 1): Promise<Cart> {
    const res = await fetch(`${API_BASE}/cart/items`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ product_id: productId, quantity }),
    });
    return handleResponse<Cart>(res);
  },

  async updateCartItem(itemId: number, quantity: number): Promise<Cart> {
    const res = await fetch(`${API_BASE}/cart/items/${itemId}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify({ quantity }),
    });
    return handleResponse<Cart>(res);
  },

  async removeCartItem(itemId: number): Promise<Cart> {
    const res = await fetch(`${API_BASE}/cart/items/${itemId}`, {
      method: 'DELETE',
      headers: getHeaders(),
    });
    return handleResponse<Cart>(res);
  },

  // Orders & Checkout
  async checkout(payload: { shipping_address_id: number; payment_method: string; coupon_code?: string }): Promise<Order> {
    const res = await fetch(`${API_BASE}/orders/checkout`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(payload),
    });
    return handleResponse<Order>(res);
  },

  async getMyOrders(): Promise<Order[]> {
    const res = await fetch(`${API_BASE}/orders/`, {
      headers: getHeaders(),
    });
    return handleResponse<Order[]>(res);
  },

  async getAddresses(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/users/addresses`, {
      headers: getHeaders(),
    });
    return handleResponse<any[]>(res);
  },

  // AI & Recommendations
  async getRecommendations(strategy: string = 'HYBRID', productId?: number): Promise<RecommendationItem[]> {
    let url = `${API_BASE}/ai/recommendations?strategy=${strategy}`;
    if (productId) url += `&product_id=${productId}`;
    const res = await fetch(url, {
      headers: getHeaders(),
    });
    const data = await handleResponse<{ recommendations: RecommendationItem[] }>(res);
    return data.recommendations || [];
  },

  async parseSearchIntent(query: string): Promise<ParsedSearchIntent> {
    const res = await fetch(`${API_BASE}/ai/search/parse-intent?query_text=${encodeURIComponent(query)}`, {
      method: 'POST',
      headers: getHeaders(),
    });
    return handleResponse<ParsedSearchIntent>(res);
  },

  async chatAssistant(message: string): Promise<ShoppingAssistantResponse> {
    const res = await fetch(`${API_BASE}/ai/assistant/chat`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ user_message: message }),
    });
    return handleResponse<ShoppingAssistantResponse>(res);
  },

  // Analytics & Admin
  async getAdminOverview(): Promise<any> {
    const res = await fetch(`${API_BASE}/analytics/overview`, {
      headers: getHeaders(),
    });
    return handleResponse<any>(res);
  },

  async getSellerAnalytics(): Promise<any> {
    const res = await fetch(`${API_BASE}/sellers/analytics`, {
      headers: getHeaders(),
    });
    return handleResponse<any>(res);
  },

  async recordBehaviorEvent(eventType: string, productId?: number, metadata?: Record<string, any>) {
    fetch(`${API_BASE}/analytics/event`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ event_type: eventType, product_id: productId, metadata: metadata || {} }),
    }).catch(() => {});
  },

  // Catalog Expansion: Bundles, Q&A, Reviews, Alerts
  async getProductBundles(productId: number) {
    const res = await fetch(`${API_BASE}/catalog/products/${productId}/bundles`, { headers: getHeaders() });
    return handleResponse<any[]>(res);
  },

  async getProductQnA(productId: number) {
    const res = await fetch(`${API_BASE}/catalog/products/${productId}/questions`, { headers: getHeaders() });
    return handleResponse<any[]>(res);
  },

  async askProductQuestion(productId: number, questionText: string) {
    const res = await fetch(`${API_BASE}/catalog/products/${productId}/questions`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ question_text: questionText })
    });
    return handleResponse<any>(res);
  },

  async voteReviewHelpfulness(reviewId: number, isHelpful: boolean) {
    const res = await fetch(`${API_BASE}/catalog/reviews/${reviewId}/vote`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ is_helpful: isHelpful })
    });
    return handleResponse<any>(res);
  },

  async recordRecentlyViewed(productId: number) {
    fetch(`${API_BASE}/catalog/recently-viewed/${productId}`, {
      method: 'POST',
      headers: getHeaders()
    }).catch(() => {});
  },

  async getRecentlyViewed(limit: number = 10) {
    const res = await fetch(`${API_BASE}/catalog/recently-viewed?limit=${limit}`, { headers: getHeaders() });
    return handleResponse<any[]>(res);
  },

  async createPriceAlert(productId: number, targetPrice: number, alertType: string = 'PRICE_DROP') {
    const res = await fetch(`${API_BASE}/catalog/price-alerts`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ product_id: productId, target_price: targetPrice, alert_type: alertType })
    });
    return handleResponse<any>(res);
  },

  async getUserPriceAlerts() {
    const res = await fetch(`${API_BASE}/catalog/price-alerts`, { headers: getHeaders() });
    return handleResponse<any[]>(res);
  },

  // Multi-Vendor Marketplace & Orchestration
  async getSellerScorecard() {
    const res = await fetch(`${API_BASE}/marketplace/scorecard`, { headers: getHeaders() });
    return handleResponse<any>(res);
  },

  async requestSellerPayout(amount: number, notes?: string) {
    const res = await fetch(`${API_BASE}/marketplace/payouts/request`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ amount, notes })
    });
    return handleResponse<any>(res);
  },

  async getSellerPayouts() {
    const res = await fetch(`${API_BASE}/marketplace/payouts`, { headers: getHeaders() });
    return handleResponse<any[]>(res);
  },

  async checkReturnEligibility(orderId: number, orderItemId: number) {
    const res = await fetch(`${API_BASE}/marketplace/orders/${orderId}/items/${orderItemId}/return-eligibility`, {
      headers: getHeaders()
    });
    return handleResponse<any>(res);
  },

  async aiSupportChat(message: string, context?: any) {
    const res = await fetch(`${API_BASE}/marketplace/ai-support/chat`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ message, context: context || {} })
    });
    return handleResponse<any>(res);
  },

  async getFacetedSearch(query: string, categoryId?: number, brandId?: number) {
    let url = `${API_BASE}/search/faceted?query=${encodeURIComponent(query)}`;
    if (categoryId) url += `&category_id=${categoryId}`;
    if (brandId) url += `&brand_id=${brandId}`;
    const res = await fetch(url, { headers: getHeaders() });
    return handleResponse<any>(res);
  }
};

