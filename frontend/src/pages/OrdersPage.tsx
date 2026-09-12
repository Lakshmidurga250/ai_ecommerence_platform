import React, { useState, useEffect } from 'react';
import { Package, Truck, Calendar, DollarSign, ChevronRight, ExternalLink } from 'lucide-react';
import { Order } from '../types';
import { api } from '../services/api';
import { Link } from 'react-router-dom';

export const OrdersPage: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const data = await api.getMyOrders();
        setOrders(data);
      } catch (err) {
        console.error('Failed to load customer orders:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  const getStatusBadge = (status: string) => {
    switch (status.toUpperCase()) {
      case 'DELIVERED':
      case 'COMPLETED':
        return 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 border-emerald-200';
      case 'PROCESSING':
      case 'CONFIRMED':
        return 'bg-indigo-50 text-indigo-700 dark:bg-indigo-950/40 dark:text-indigo-400 border-indigo-200';
      case 'SHIPPED':
        return 'bg-blue-50 text-blue-700 dark:bg-blue-950/40 dark:text-blue-400 border-blue-200';
      case 'CANCELLED':
        return 'bg-rose-50 text-rose-700 dark:bg-rose-950/40 dark:text-rose-400 border-rose-200';
      default:
        return 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border-slate-200';
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 w-full">
      <div className="flex items-center justify-between pb-6 mb-8 border-b border-slate-200 dark:border-slate-800">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white">
            Order History &amp; Tracking
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
            Track your deliveries, receipts, and order statuses in real-time
          </p>
        </div>
      </div>

      {loading ? (
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-44 bg-slate-100 dark:bg-slate-800 rounded-3xl animate-pulse" />
          ))}
        </div>
      ) : orders.length === 0 ? (
        <div className="p-16 text-center rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
          <Package className="w-12 h-12 mx-auto text-slate-400 mb-3" />
          <h3 className="text-base font-bold text-slate-800 dark:text-slate-200">No Orders Found</h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            You haven't placed any marketplace orders yet.
          </p>
          <Link
            to="/products"
            className="inline-block mt-4 px-6 py-2.5 bg-indigo-600 text-white rounded-xl text-xs font-bold shadow-md"
          >
            Start Browsing
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {orders.map((order) => (
            <div
              key={order.id}
              className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden"
            >
              {/* Card Header */}
              <div className="p-5 sm:p-6 bg-slate-50/60 dark:bg-slate-800/40 border-b border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-4">
                <div className="flex flex-wrap items-center gap-4 sm:gap-8 text-xs">
                  <div>
                    <span className="text-slate-400 block mb-0.5">Order Number</span>
                    <span className="font-mono font-bold text-slate-900 dark:text-white">
                      {order.order_number}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-400 block mb-0.5">Order Date</span>
                    <span className="font-medium text-slate-700 dark:text-slate-300">
                      {new Date(order.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-400 block mb-0.5">Total Paid</span>
                    <span className="font-bold text-slate-900 dark:text-white">
                      ${Number(order.total_amount).toFixed(2)}
                    </span>
                  </div>
                </div>

                <span
                  className={`px-3 py-1 rounded-full text-xs font-bold border ${getStatusBadge(
                    order.status
                  )}`}
                >
                  {order.status}
                </span>
              </div>

              {/* Items List */}
              <div className="p-5 sm:p-6 divide-y divide-slate-100 dark:divide-slate-800">
                {order.items?.map((item) => (
                  <div key={item.id} className="py-3 first:pt-0 last:pb-0 flex items-center justify-between text-xs">
                    <div>
                      <h4 className="font-bold text-slate-800 dark:text-slate-200">
                        {item.product_name}
                      </h4>
                      <p className="text-slate-400 mt-0.5">
                        Qty: {item.quantity} × ${Number(item.unit_price).toFixed(2)}
                      </p>
                    </div>
                    <span className="font-bold text-slate-900 dark:text-white">
                      ${Number(item.total).toFixed(2)}
                    </span>
                  </div>
                ))}
              </div>

              {/* Shipment Details if present */}
              {order.shipment && (
                <div className="p-5 bg-indigo-50/40 dark:bg-indigo-950/20 border-t border-slate-200 dark:border-slate-800 text-xs">
                  <div className="flex items-center gap-2 font-bold text-indigo-900 dark:text-indigo-300 mb-2">
                    <Truck className="w-4 h-4 text-indigo-600" />
                    <span>
                      Tracking: {order.shipment.carrier_name} — {order.shipment.tracking_number}
                    </span>
                  </div>

                  {order.shipment.events && order.shipment.events.length > 0 && (
                    <div className="space-y-1.5 mt-2 pl-6 border-l-2 border-indigo-300 dark:border-indigo-700">
                      {order.shipment.events.map((evt) => (
                        <div key={evt.id} className="text-[11px] text-slate-600 dark:text-slate-400">
                          <span className="font-semibold text-slate-800 dark:text-slate-200">
                            {evt.status}
                          </span>{' '}
                          at {evt.location} — {evt.description || ''}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
