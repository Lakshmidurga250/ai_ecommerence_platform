export interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  is_verified: boolean;
  roles: string[];
  profile?: {
    first_name?: string;
    last_name?: string;
    phone?: string;
    avatar_url?: string;
  };
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  image_url?: string;
}

export interface Brand {
  id: number;
  name: string;
  slug: string;
  logo_url?: string;
}

export interface ProductImage {
  id: number;
  image_url: string;
  alt_text?: string;
  is_primary: boolean;
}

export interface Product {
  id: number;
  seller_id: number;
  category_id: number;
  brand_id?: number;
  sku: string;
  name: string;
  slug: string;
  short_description?: string;
  description: string;
  price: number;
  compare_at_price?: number;
  discount_percent: number;
  stock: number;
  is_active: boolean;
  is_featured: boolean;
  rating: number;
  review_count: number;
  sales_count: number;
  attributes: Record<string, any>;
  category?: Category;
  brand?: Brand;
  images: ProductImage[];
  created_at?: string;
  updated_at?: string;
}


export interface CartItem {
  id: number;
  product_id: number;
  variant_id?: number;
  quantity: number;
  price_at_addition: number;
  product?: Product;
}

export interface Cart {
  id: number;
  user_id: number;
  items: CartItem[];
  subtotal: number;
  tax_amount: number;
  discount_amount: number;
  shipping_fee: number;
  total_amount: number;
  coupon_code?: string;
}

export interface OrderItem {
  id: number;
  product_id: number;
  product_name: string;
  sku: string;
  unit_price: number;
  quantity: number;
  subtotal: number;
  tax_amount: number;
  total: number;
  status: string;
}

export interface ShipmentEvent {
  id: number;
  status: string;
  location: string;
  description?: string;
  event_time: string;
}

export interface Shipment {
  id: number;
  carrier_name: string;
  tracking_number: string;
  status: string;
  estimated_delivery?: string;
  events: ShipmentEvent[];
}

export interface Order {
  id: number;
  order_number: string;
  customer_id: number;
  status: string;
  subtotal: number;
  discount_amount: number;
  tax_amount: number;
  shipping_fee: number;
  total_amount: number;
  coupon_code?: string;
  items: OrderItem[];
  shipment?: Shipment;
  created_at: string;
}

export interface RecommendationItem {
  product: Product;
  score: number;
  explanation: string;
  model_type: string;
}

export interface ParsedSearchIntent {
  raw_query: string;
  cleaned_query: string;
  extracted_category?: string;
  extracted_brand?: string;
  extracted_color?: string;
  max_price?: number;
  min_rating?: number;
  is_semantic_intent: boolean;
}

export interface ShoppingAssistantResponse {
  assistant_reply: string;
  parsed_intent?: ParsedSearchIntent;
  grounded_products: Product[];
  confidence_score: number;
  reasoning: string;
  session_id?: string;
  intent?: string;
  action_pills?: Array<{ label: string; action: string; payload?: any }>;
  comparison_table?: {
    products?: Array<any>;
    comparison_rows?: Array<{ feature: string; values: string[] }>;
    winner?: { product_id: number; name: string; verdict: string };
    headers?: string[];
    rows?: Array<Record<string, any>>;
  };
  cart_result?: any;
  order_result?: any;
  bundle?: any;
  extracted_requirements?: {
    category?: string;
    category_name?: string;
    brand?: string;
    min_budget?: number;
    max_budget?: number;
    use_case?: string;
    requirements?: string[];
  };
  evaluation?: any;
}


// V2 Expansion Types
export interface VisualMatch {
  product_id: number;
  product_name: string;
  category: string;
  price: number;
  image_url: string;
  similarity_score: number;
  color_match_confidence: number;
  reasoning: string;
}

export interface VisualSearchResult {
  query_type: string;
  matched_count: number;
  execution_ms: number;
  matches: VisualMatch[];
}

export interface AspectScore {
  aspect: string;
  sentiment_score: number;
  sentiment_label: string;
  sample_mentions: string[];
}

export interface ReviewIntelligenceSummary {
  product_id: number;
  total_reviews_analyzed: number;
  average_rating: number;
  verified_purchase_ratio: number;
  aspect_breakdown: Record<string, AspectScore>;
  top_pros: string[];
  top_cons: string[];
  authenticity_score: number;
  suspicious_review_count: number;
  consensus_summary: string;
}

export interface RetentionRecommendation {
  action: string;
  channel: string;
  urgency: string;
  reason: string;
}

export interface Customer360Profile {
  user_id: number;
  customer_tier: string;
  summary: {
    first_name: string;
    last_name: string;
    email: string;
    member_since: string;
    days_active: number;
  };
  rfm: {
    recency_days: number;
    frequency_orders: number;
    monetary_spend: number;
    aov: number;
    rfm_segment: string;
  };
  predictive_metrics: {
    predicted_clv: number;
    churn_probability: number;
    churn_risk_level: string;
    next_expected_purchase_days: number;
  };
  preferences: {
    favorite_categories: string[];
    favorite_brands: string[];
    price_sensitivity: string;
  };
  retention_recommendations: RetentionRecommendation[];
}

export interface ABCXYZMatrixItem {
  product_id: number;
  sku: string;
  name: string;
  category: string;
  abc_class: string;
  xyz_class: string;
  matrix_tag: string;
  total_revenue: number;
  avg_monthly_demand: number;
  demand_cv: number;
  current_stock: number;
  days_of_inventory: number;
  stockout_risk_score: number;
  recommended_action: string;
}

export interface WarehouseTransferItem {
  transfer_id: string;
  product_id: number;
  product_name: string;
  source_warehouse_id: number;
  source_warehouse_name: string;
  target_warehouse_id: number;
  target_warehouse_name: string;
  transfer_quantity: number;
  reason: string;
  estimated_savings: number;
}

export interface PricingRecommendation {
  recommendation_id: number;
  product_id: number;
  product_name: string;
  current_price: number;
  recommended_price: number;
  price_delta: number;
  price_delta_pct: number;
  strategy: string;
  elasticity: number;
  expected_demand_lift_pct: number;
  expected_revenue_shift_pct: number;
  rationale: string;
}

export interface FraudAlertItem {
  alert_id: number;
  order_id: number;
  customer_id: number;
  customer_name: string;
  order_amount: number;
  risk_score: number;
  risk_level: string;
  status: string;
  flagged_factors: string[];
  created_at: string;
}

export interface FraudStatistics {
  total_evaluated_orders: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  blocked_order_count: number;
  resolved_alerts_count: number;
  fraud_prevention_rate_pct: number;
}

export interface DeliveryRouteEstimate {
  product_id: number;
  destination_pincode: string;
  warehouse_id: number;
  warehouse_name: string;
  distance_km: number;
  estimated_transit_days: number;
  estimated_delivery_date: string;
  carrier: string;
  shipping_fee: number;
  carbon_kg: number;
}

export interface MLModelItem {
  model_id: string;
  model_name: string;
  version: string;
  stage: string;
  algorithm: string;
  training_date: string;
  accuracy_metric: { name: string; value: number };
  latency_ms: number;
  is_active: boolean;
}

export interface MLDriftItem {
  drift_id: number;
  model_name: string;
  drift_metric: string;
  baseline_value: number;
  current_value: number;
  drift_detected: boolean;
  p_value: number;
  timestamp: string;
}

export interface ABExperimentVariant {
  variant_name: string;
  participants: number;
  conversions: number;
  conversion_rate: number;
  lift_pct: number;
  is_winner: boolean;
}

export interface ABExperimentItem {
  experiment_id: number;
  name: string;
  description: string;
  status: string;
  variants: string[];
  traffic_split: Record<string, number>;
  start_time: string;
  end_time?: string;
}

export interface ABExperimentAnalytics {
  experiment_id: number;
  name: string;
  total_participants: number;
  variants: ABExperimentVariant[];
}

export interface LoyaltyProfile {
  account_id: number;
  user_id: number;
  current_points: number;
  lifetime_points: number;
  tier: string;
  points_expiring_soon: number;
  recent_transactions: Array<{
    id: number;
    transaction_type: string;
    points: number;
    description: string;
    created_at: string;
  }>;
}

// V3 Interfaces: 15 Master AI Features & Deep Architecture
export interface OutfitItem {
  id: number;
  name: string;
  slug: string;
  brand: string;
  price: number;
  rating: number;
  image_url: string;
  is_focal: boolean;
  role: string;
  compatibility_score: number;
}

export interface OutfitBundle {
  bundle_id: string;
  theme_title: string;
  focal_product_id: number;
  category: string;
  items_count: number;
  items: OutfitItem[];
  original_total_price: number;
  bundle_discount_pct: number;
  bundle_price: number;
  total_savings: number;
  currency: string;
  tier_name?: string;
  badge?: string;
  one_click_add_payload: {
    product_ids: number[];
    discount_code: string;
  };
}

export interface TieredBundlesResponse {
  focal_product: {
    id: number;
    name: string;
    price: number;
    category: string;
  };
  tiered_bundles: OutfitBundle[];
}

export interface PromotionSimulation {
  discount_pct: number;
  discounted_price: number;
  margin_per_unit: number;
  margin_percentage: number;
  volume_lift_pct: number;
  predicted_quantity: number;
  projected_revenue: number;
  projected_profit: number;
  breakeven_lift_pct: number;
  is_profitable: boolean;
}

export interface PromotionOptimizationResponse {
  product_id: number;
  product_name: string;
  category: string;
  current_price: number;
  estimated_unit_cost: number;
  baseline_weekly_sales: number;
  elasticity_coefficient: number;
  target_objective: string;
  recommended_promotion: {
    optimal_discount_pct: number;
    promotional_price: number;
    expected_volume_lift: string;
    expected_weekly_revenue: number;
    expected_weekly_profit: number;
    profit_lift_pct: number;
    recommendation_summary: string;
  };
  all_tier_simulations: PromotionSimulation[];
}

export interface NextBestAction {
  user_id: number;
  action_type: string;
  priority: string;
  confidence: number;
  headline: string;
  description: string;
  cta_label: string;
  target_route: string;
  context: Record<string, any>;
}

export interface ProductQualityScore {
  product_id: number;
  product_name: string;
  category: string;
  composite_quality_score: number;
  quality_badge: string;
  quality_label: string;
  badge_color: string;
  breakdown: {
    bayesian_rating_score: number;
    review_sentiment_score: number;
    reliability_score: number;
    verified_purchase_score: number;
  };
  metrics: {
    raw_rating: number;
    bayesian_rating: number;
    review_count: number;
    verified_ratio: number;
    estimated_return_rate: string;
  };
}

export interface CrossSellItem {
  id: number;
  name: string;
  slug: string;
  price: number;
  rating: number;
  image_url: string;
  brand: string;
  category: string;
  co_occurrence_lift: number;
  confidence_score: number;
  combo_price_with_focal: number;
  recommendation_pitch: string;
}

export interface CrossSellResponse {
  focal_product: {
    id: number;
    name: string;
    price: number;
    category: string;
  };
  cross_sell_items: CrossSellItem[];
}

export interface UpsellItem {
  id: number;
  name: string;
  slug: string;
  price: number;
  rating: number;
  image_url: string;
  brand: string;
  price_delta: number;
  price_delta_pct: string;
  value_prop_score: number;
  key_advantages: string[];
}

export interface UpsellResponse {
  focal_product: {
    id: number;
    name: string;
    price: number;
    rating: number;
    category: string;
  };
  upsell_alternatives: UpsellItem[];
}

export interface FunnelStep {
  stage_key: string;
  label: string;
  visitor_count: number;
  step_conversion_pct: string;
  dropoff_pct: string;
  overall_conversion_pct: string;
}

export interface FunnelAnalytics {
  funnel_summary: {
    total_unique_visitors: number;
    total_completed_orders: number;
    overall_conversion_rate: string;
    primary_bottleneck: string;
    max_stage_dropoff: string;
  };
  funnel_steps: FunnelStep[];
  ai_optimization_recommendations: Array<{
    stage: string;
    issue: string;
    action: string;
  }>;
}

export interface FinancialDashboard {
  financial_kpis: {
    gross_merchandise_value_gmv: number;
    order_volume: number;
    average_order_value_aov: number;
    platform_net_take_rate: string;
    gross_commission_earned: number;
    net_platform_profit: number;
    seller_payout_liability: number;
  };
  cost_breakdown: {
    payment_gateway_processing_fees: number;
    logistics_fulfillment_expenses: number;
    returns_and_refunds_provision: number;
  };
  revenue_forecast_multi_horizon: {
    horizon_30d_projected_gmv: number;
    horizon_60d_projected_gmv: number;
    horizon_90d_projected_gmv: number;
    confidence_interval: string;
    projected_mom_growth: string;
  };
  payment_methods_performance: Array<{
    method: string;
    share_pct: string;
    success_rate: string;
  }>;
}

export interface ReturnsDashboard {
  returns_kpis: {
    total_return_requests: number;
    overall_platform_return_rate: string;
    total_refund_value_inr: number;
    reverse_logistics_cost_inr: number;
    average_turnaround_days: number;
    fraudulent_abuse_rate: string;
  };
  top_return_reasons: Array<{
    reason: string;
    percentage: string;
    primary_category: string;
  }>;
  category_return_rates: Array<{
    category: string;
    return_rate: string;
    risk_tier: string;
  }>;
}


