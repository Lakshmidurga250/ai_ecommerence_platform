import { 
  User, Product, Category, Brand, Cart, Order, RecommendationItem, ShoppingAssistantResponse, ParsedSearchIntent,
  VisualSearchResult, ReviewIntelligenceSummary, Customer360Profile, ABCXYZMatrixItem, WarehouseTransferItem,
  PricingRecommendation, FraudAlertItem, FraudStatistics, DeliveryRouteEstimate, MLModelItem, MLDriftItem,
  ABExperimentItem, ABExperimentAnalytics, LoyaltyProfile,
  OutfitBundle, TieredBundlesResponse, PromotionOptimizationResponse, NextBestAction, ProductQualityScore,
  CrossSellResponse, UpsellResponse, FunnelAnalytics, FinancialDashboard, ReturnsDashboard
} from '../types';


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

  async getBrands(): Promise<Brand[]> {
    const res = await fetch(`${API_BASE}/categories/brands`, {
      headers: getHeaders(),
    });
    return handleResponse<Brand[]>(res);
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

  async chatAssistant(message: string, sessionId?: string, context?: any): Promise<ShoppingAssistantResponse> {
    const res = await fetch(`${API_BASE}/ai/assistant/chat`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ user_message: message, session_id: sessionId, context }),
    });
    return handleResponse<ShoppingAssistantResponse>(res);
  },

  async sendShoppingAgentFeedback(sessionId: string, isPositive: boolean, turnIndex: number = 0): Promise<any> {
    const res = await fetch(`${API_BASE}/ai/shopping-agent/feedback`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ session_id: sessionId, is_positive: isPositive, turn_index: turnIndex }),
    });
    return handleResponse<any>(res);
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
  },

  // AI Commerce V2: Visual Search
  async visualSearch(payload: { image_url?: string; image_base64?: string; top_k?: number; category_hint?: string }): Promise<VisualSearchResult> {
    const res = await fetch(`${API_BASE}/search/visual`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(payload),
    });
    return handleResponse<VisualSearchResult>(res);
  },

  // AI Commerce V2: Review Intelligence
  async getReviewIntelligence(productId: number): Promise<ReviewIntelligenceSummary> {
    const res = await fetch(`${API_BASE}/reviews/product/${productId}/intelligence-summary`, {
      headers: getHeaders(),
    });
    return handleResponse<ReviewIntelligenceSummary>(res);
  },

  // AI Commerce V2: Customer 360 & Churn
  async getMyCustomer360(): Promise<Customer360Profile> {
    const res = await fetch(`${API_BASE}/customer-intelligence/me/360`, {
      headers: getHeaders(),
    });
    return handleResponse<Customer360Profile>(res);
  },

  async getUserCustomer360(userId: number): Promise<Customer360Profile> {
    const res = await fetch(`${API_BASE}/customer-intelligence/users/${userId}/360`, {
      headers: getHeaders(),
    });
    return handleResponse<Customer360Profile>(res);
  },

  // AI Commerce V2: Inventory & ABC/XYZ Intelligence
  async getInventoryMatrix(params?: { min_revenue?: number; abc_filter?: string; xyz_filter?: string }): Promise<ABCXYZMatrixItem[]> {
    const query = new URLSearchParams(params as any || {}).toString();
    const res = await fetch(`${API_BASE}/inventory-intelligence/matrix${query ? '?' + query : ''}`, {
      headers: getHeaders(),
    });
    return handleResponse<ABCXYZMatrixItem[]>(res);
  },

  async getWarehouseTransfers(): Promise<WarehouseTransferItem[]> {
    const res = await fetch(`${API_BASE}/inventory-intelligence/transfers`, {
      headers: getHeaders(),
    });
    return handleResponse<WarehouseTransferItem[]>(res);
  },

  async getMultiHorizonForecast(productId: number): Promise<any> {
    const res = await fetch(`${API_BASE}/inventory-intelligence/multi-horizon-forecast/${productId}`, {
      headers: getHeaders(),
    });
    return handleResponse<any>(res);
  },

  // AI Commerce V2: Dynamic Pricing
  async getSellerPricingRecommendations(params?: { strategy?: string }): Promise<PricingRecommendation[]> {
    const query = new URLSearchParams(params as any || {}).toString();
    const res = await fetch(`${API_BASE}/marketplace/pricing-recommendations${query ? '?' + query : ''}`, {
      headers: getHeaders(),
    });
    return handleResponse<PricingRecommendation[]>(res);
  },

  async getProductPricingRecommendation(productId: number): Promise<PricingRecommendation> {
    const res = await fetch(`${API_BASE}/marketplace/pricing-recommendations/product/${productId}`, {
      headers: getHeaders(),
    });
    return handleResponse<PricingRecommendation>(res);
  },

  // AI Commerce V2: Fraud Intelligence Center
  async getFraudAlerts(params?: { status?: string; min_risk?: number }): Promise<FraudAlertItem[]> {
    const query = new URLSearchParams(params as any || {}).toString();
    const res = await fetch(`${API_BASE}/fraud/alerts${query ? '?' + query : ''}`, {
      headers: getHeaders(),
    });
    return handleResponse<FraudAlertItem[]>(res);
  },

  async resolveFraudAlert(alertId: number, resolution: 'APPROVED' | 'BLOCKED', notes?: string): Promise<any> {
    const res = await fetch(`${API_BASE}/fraud/alerts/${alertId}/resolve`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ resolution, notes }),
    });
    return handleResponse<any>(res);
  },

  async getFraudStatistics(): Promise<FraudStatistics> {
    const res = await fetch(`${API_BASE}/fraud/statistics`, {
      headers: getHeaders(),
    });
    return handleResponse<FraudStatistics>(res);
  },

  // AI Commerce V2: Smart Logistics & Returns
  async estimateDeliveryRoute(productId: number, destinationPincode: string): Promise<DeliveryRouteEstimate> {
    const res = await fetch(`${API_BASE}/logistics/estimate-delivery`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ product_id: productId, destination_pincode: destinationPincode }),
    });
    return handleResponse<DeliveryRouteEstimate>(res);
  },

  async getReturnAnalytics(): Promise<any> {
    const res = await fetch(`${API_BASE}/logistics/return-analytics`, {
      headers: getHeaders(),
    });
    return handleResponse<any>(res);
  },

  // AI Commerce V2: Unified Event Tracking
  async trackEvent(eventType: string, data?: { product_id?: number; category_id?: number; page_url?: string; metadata?: Record<string, any> }): Promise<any> {
    const res = await fetch(`${API_BASE}/events/track`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        event_type: eventType,
        product_id: data?.product_id,
        category_id: data?.category_id,
        page_url: data?.page_url,
        metadata: data?.metadata || {},
      }),
    });
    return handleResponse<any>(res);
  },

  // AI Commerce V2: MLOps Platform
  async getMLOpsModels(): Promise<MLModelItem[]> {
    const res = await fetch(`${API_BASE}/mlops/models`, {
      headers: getHeaders(),
    });
    return handleResponse<MLModelItem[]>(res);
  },

  async getMLOpsDrift(): Promise<MLDriftItem[]> {
    const res = await fetch(`${API_BASE}/mlops/drift`, {
      headers: getHeaders(),
    });
    return handleResponse<MLDriftItem[]>(res);
  },

  async promoteMLOpsModel(modelId: string, targetStage: string): Promise<any> {
    const res = await fetch(`${API_BASE}/mlops/models/${modelId}/promote`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ target_stage: targetStage }),
    });
    return handleResponse<any>(res);
  },

  // AI Commerce V2: A/B Testing
  async getExperiments(): Promise<ABExperimentItem[]> {
    const res = await fetch(`${API_BASE}/experiments/`, {
      headers: getHeaders(),
    });
    return handleResponse<ABExperimentItem[]>(res);
  },

  async getExperimentAnalytics(experimentId: number): Promise<ABExperimentAnalytics> {
    const res = await fetch(`${API_BASE}/experiments/${experimentId}/analytics`, {
      headers: getHeaders(),
    });
    return handleResponse<ABExperimentAnalytics>(res);
  },

  async logExperimentEvent(experimentId: number, variant: string, eventType: string, value?: number): Promise<any> {
    const res = await fetch(`${API_BASE}/experiments/events`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        experiment_id: experimentId,
        variant_name: variant,
        event_type: eventType,
        metric_value: value || 1.0,
      }),
    });
    return handleResponse<any>(res);
  },

  // AI Commerce V2: Loyalty & Rewards
  async getMyLoyaltyProfile(): Promise<LoyaltyProfile> {
    const res = await fetch(`${API_BASE}/loyalty/me`, {
      headers: getHeaders(),
    });
    return handleResponse<LoyaltyProfile>(res);
  },

  async redeemLoyaltyPoints(points: number): Promise<any> {
    const res = await fetch(`${API_BASE}/loyalty/redeem`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ points }),
    });
    return handleResponse<any>(res);
  },

  // AI Commerce V2: Recommendations Multi-Stage Pipeline
  async getRecommendationPipeline(userId?: number, productId?: number, limit: number = 10): Promise<any> {
    let url = `${API_BASE}/ai/recommendations/pipeline?limit=${limit}`;
    if (userId) url += `&user_id=${userId}`;
    if (productId) url += `&product_id=${productId}`;
    const res = await fetch(url, { headers: getHeaders() });
    return handleResponse<any>(res);
  },

  async getSessionRecommendations(productIds: number[], limit: number = 6): Promise<any> {
    const query = productIds.map(id => `product_ids=${id}`).join('&');
    const res = await fetch(`${API_BASE}/ai/recommendations/session?${query}&limit=${limit}`, {
      headers: getHeaders(),
    });
    return handleResponse<any>(res);
  },

  // V3 Advanced AI Recommendations & Bundles
  async getProductOutfit(productId: number, bundleSize: number = 3, discountPct: number = 12.0): Promise<OutfitBundle> {
    const res = await fetch(`${API_BASE}/recommendations-v3/outfit/${productId}?bundle_size=${bundleSize}&discount_pct=${discountPct}`, {
      headers: getHeaders(),
    });
    return handleResponse<OutfitBundle>(res);
  },

  async getTieredBundles(productId: number): Promise<TieredBundlesResponse> {
    const res = await fetch(`${API_BASE}/recommendations-v3/bundles/${productId}`, {
      headers: getHeaders(),
    });
    return handleResponse<TieredBundlesResponse>(res);
  },

  async getPersonalizedRanking(userId?: number, categorySlug?: string, limit: number = 20): Promise<any> {
    const res = await fetch(`${API_BASE}/recommendations-v3/personalized-ranking`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ user_id: userId, category_slug: categorySlug, limit }),
    });
    return handleResponse<any>(res);
  },

  async getCrossSells(productId: number, limit: number = 3): Promise<CrossSellResponse> {
    const res = await fetch(`${API_BASE}/recommendations-v3/cross-sell/${productId}?limit=${limit}`, {
      headers: getHeaders(),
    });
    return handleResponse<CrossSellResponse>(res);
  },

  async getUpsells(productId: number, limit: number = 3): Promise<UpsellResponse> {
    const res = await fetch(`${API_BASE}/recommendations-v3/upsell/${productId}?limit=${limit}`, {
      headers: getHeaders(),
    });
    return handleResponse<UpsellResponse>(res);
  },

  // V3 Commerce Intelligence
  async optimizePromotion(productId: number, targetObjective: string = 'MAX_PROFIT'): Promise<PromotionOptimizationResponse> {
    const res = await fetch(`${API_BASE}/commerce/promotion-optimize`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ product_id: productId, target_objective: targetObjective }),
    });
    return handleResponse<PromotionOptimizationResponse>(res);
  },

  async getNextBestAction(userId: number): Promise<NextBestAction> {
    const res = await fetch(`${API_BASE}/commerce/next-best-action/${userId}`, {
      headers: getHeaders(),
    });
    return handleResponse<NextBestAction>(res);
  },

  async getProductQualityScore(productId: number): Promise<ProductQualityScore> {
    const res = await fetch(`${API_BASE}/commerce/product-quality/${productId}`, {
      headers: getHeaders(),
    });
    return handleResponse<ProductQualityScore>(res);
  },

  async checkReviewQuality(comment: string, rating: number, isVerified: boolean = true): Promise<any> {
    const res = await fetch(`${API_BASE}/commerce/review-quality-check`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ comment, rating, is_verified_purchase: isVerified }),
    });
    return handleResponse<any>(res);
  },

  async getReturnsDashboard(): Promise<ReturnsDashboard> {
    const res = await fetch(`${API_BASE}/commerce/returns-dashboard`, {
      headers: getHeaders(),
    });
    return handleResponse<ReturnsDashboard>(res);
  },

  // V3 Analytics & Architecture
  async getFunnelAnalytics(): Promise<FunnelAnalytics> {
    const res = await fetch(`${API_BASE}/analytics-v3/funnel`, {
      headers: getHeaders(),
    });
    return handleResponse<FunnelAnalytics>(res);
  },

  async getFinancialDashboard(): Promise<FinancialDashboard> {
    const res = await fetch(`${API_BASE}/analytics-v3/financial-dashboard`, {
      headers: getHeaders(),
    });
    return handleResponse<FinancialDashboard>(res);
  },

  async getDataWarehouseSummary(): Promise<any> {
    const res = await fetch(`${API_BASE}/analytics-v3/data-warehouse/summary`, {
      headers: getHeaders(),
    });
    return handleResponse<any>(res);
  },

  async calculateLogisticsRoute(originHub: string = 'DEL', destinationHub: string = 'BLR'): Promise<any> {
    const res = await fetch(`${API_BASE}/analytics-v3/logistics/route`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ origin_hub: originHub, destination_hub: destinationHub }),
    });
    return handleResponse<any>(res);
  },

  async getProductKnowledgeGraph(productId: number): Promise<any> {
    const res = await fetch(`${API_BASE}/analytics-v3/knowledge-graph/product/${productId}`, {
      headers: getHeaders(),
    });
    return handleResponse<any>(res);
  },

  async executeSemanticSearch(query: string, limit: number = 10): Promise<any> {
    const res = await fetch(`${API_BASE}/analytics-v3/semantic-search`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ query, limit }),
    });
    return handleResponse<any>(res);
  }
};


// Base URL fallback for static asset resolution
