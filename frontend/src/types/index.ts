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
  parsed_intent: ParsedSearchIntent;
  grounded_products: Product[];
  confidence_score: number;
  reasoning: string;
}
