import React, { useState, useEffect } from 'react';
import { User, Bell, MapPin, Package, Shield, Award, Sparkles, Trash2, ArrowRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import { Link } from 'react-router-dom';
import { Customer360Card } from '../components/Customer360Card';

export const CustomerAccountPage: React.FC = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState<'profile' | 'orders' | 'alerts' | 'addresses'>('profile');
  const [orders, setOrders] = useState<any[]>([]);
  const [priceAlerts, setPriceAlerts] = useState<any[]>([]);
  const [addresses, setAddresses] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadAccountData();
  }, []);

  const loadAccountData = async () => {
    setLoading(true);
    try {
      const [ordersData, alertsData, addressesData] = await Promise.all([
        api.getMyOrders().catch(() => []),
        api.getUserPriceAlerts().catch(() => []),
        api.getAddresses().catch(() => [])
      ]);
      setOrders(ordersData || []);
      setPriceAlerts(alertsData || []);
      setAddresses(addressesData || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-10 w-full">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-800 rounded-3xl p-8 text-white shadow-xl mb-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="flex items-center gap-5">
          <div className="w-20 h-20 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 flex items-center justify-center text-white text-3xl font-black shadow-inner">
            {user?.profile?.first_name ? user.profile.first_name[0].toUpperCase() : (user?.username ? user.username[0].toUpperCase() : 'C')}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl sm:text-3xl font-black">
                {user?.profile?.first_name ? `${user.profile.first_name} ${user.profile?.last_name || ''}` : user?.username}
              </h1>
              <span className="flex items-center gap-1 bg-amber-400/20 border border-amber-300/40 text-amber-200 text-xs font-bold px-2.5 py-0.5 rounded-full">

                <Award className="w-3.5 h-3.5 text-amber-300" />
                VIP Platinum Member
              </span>
            </div>
            <p className="text-blue-100 text-sm mt-1">{user?.email}</p>
            <p className="text-xs text-blue-200/80 mt-0.5">Customer ID: #{user?.id || 1001}</p>
          </div>
        </div>

        <div className="flex items-center gap-3 bg-white/10 backdrop-blur-md px-5 py-3.5 rounded-2xl border border-white/20">
          <Sparkles className="w-5 h-5 text-amber-300" />
          <div>
            <p className="text-xs text-blue-100">Reward Tier Status</p>
            <p className="text-sm font-bold text-white">350 Points Earned • Free Express Shipping</p>
          </div>
        </div>
      </div>

      {/* Main Container */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        {/* Navigation Sidebar */}
        <aside className="space-y-2">
          <button
            onClick={() => setActiveTab('profile')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-bold text-sm transition-all ${
              activeTab === 'profile'
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
            }`}
          >
            <User className="w-4 h-4" /> Account Profile
          </button>

          <button
            onClick={() => setActiveTab('orders')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-bold text-sm transition-all ${
              activeTab === 'orders'
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
            }`}
          >
            <Package className="w-4 h-4" /> My Orders ({orders.length})
          </button>

          <button
            onClick={() => setActiveTab('alerts')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-bold text-sm transition-all ${
              activeTab === 'alerts'
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
            }`}
          >
            <Bell className="w-4 h-4" /> Price & Stock Alerts ({priceAlerts.length})
          </button>

          <button
            onClick={() => setActiveTab('addresses')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-bold text-sm transition-all ${
              activeTab === 'addresses'
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
            }`}
          >
            <MapPin className="w-4 h-4" /> Address Book ({addresses.length})
          </button>
        </aside>

        {/* Content Area */}
        <div className="md:col-span-3 bg-white dark:bg-slate-900 rounded-2xl p-6 sm:p-8 border border-slate-200 dark:border-slate-800 shadow-sm">
          {/* PROFILE TAB */}
          {activeTab === 'profile' && (
            <div>
              <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-6">Account Overview</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
                  <p className="text-xs text-slate-400 font-semibold uppercase">Email Address</p>
                  <p className="text-base font-bold text-slate-900 dark:text-white mt-1">{user?.email}</p>
                </div>
                <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
                  <p className="text-xs text-slate-400 font-semibold uppercase">Phone Number</p>
                  <p className="text-base font-bold text-slate-900 dark:text-white mt-1">{user?.profile?.phone || '+1 (555) 234-5678'}</p>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
                  <p className="text-xs text-slate-400 font-semibold uppercase">Account Security</p>
                  <p className="text-base font-bold text-emerald-600 dark:text-emerald-400 mt-1 flex items-center gap-1.5">
                    <Shield className="w-4 h-4" /> 256-bit Encrypted Session Active
                  </p>
                </div>
                <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
                  <p className="text-xs text-slate-400 font-semibold uppercase">Platform Guarantee</p>
                  <p className="text-base font-bold text-slate-900 dark:text-white mt-1">30-Day Hassle Free Returns</p>
                </div>
              </div>

              {/* AI Customer 360 & Loyalty Panel */}
              <Customer360Card />
            </div>
          )}

          {/* ORDERS TAB */}
          {activeTab === 'orders' && (
            <div>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-slate-900 dark:text-white">Recent Orders & Shipments</h2>
                <Link to="/orders" className="text-xs font-semibold text-blue-600 hover:underline">
                  View Full History
                </Link>
              </div>

              {orders.length === 0 ? (
                <div className="py-12 text-center text-slate-400">
                  <Package className="w-10 h-10 mx-auto text-slate-300 mb-2" />
                  <p className="font-semibold text-sm">No orders placed yet</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {orders.map((ord) => (
                    <div key={ord.id} className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/40 flex items-center justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-sm text-slate-900 dark:text-white">Order #{ord.order_number}</span>
                          <span className="text-xs px-2 py-0.5 rounded-full font-bold bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300">
                            {ord.status}
                          </span>
                        </div>
                        <p className="text-xs text-slate-400 mt-1">Placed on {new Date(ord.created_at).toLocaleDateString()}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-base font-black text-slate-900 dark:text-white">${ord.total_amount?.toFixed(2)}</p>
                        <Link to={`/orders`} className="text-xs font-semibold text-blue-600 hover:underline flex items-center gap-1 justify-end mt-1">
                          Track Shipment <ArrowRight className="w-3 h-3" />
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* ALERTS TAB */}
          {activeTab === 'alerts' && (
            <div>
              <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-6">Active Price & Stock Alerts</h2>
              {priceAlerts.length === 0 ? (
                <div className="py-12 text-center text-slate-400">
                  <Bell className="w-10 h-10 mx-auto text-slate-300 mb-2" />
                  <p className="font-semibold text-sm">No active alerts set</p>
                  <p className="text-xs text-slate-400 mt-1">
                    Click "Set Price Alert" on any product page to be notified when prices drop!
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {priceAlerts.map((alert) => (
                    <div key={alert.id} className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 flex items-center justify-between">
                      <div>
                        <p className="font-bold text-sm text-slate-900 dark:text-white">Product #{alert.product_id}</p>
                        <p className="text-xs text-emerald-600 font-medium">Alert Target Price: ${alert.target_price?.toFixed(2)}</p>
                      </div>
                      <span className="text-xs font-bold text-blue-600 bg-blue-50 dark:bg-blue-950/60 px-2.5 py-1 rounded-lg">
                        Monitoring
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* ADDRESSES TAB */}
          {activeTab === 'addresses' && (
            <div>
              <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-6">Shipping Address Book</h2>
              {addresses.length === 0 ? (
                <div className="py-12 text-center text-slate-400">
                  <MapPin className="w-10 h-10 mx-auto text-slate-300 mb-2" />
                  <p className="font-semibold text-sm">No addresses saved yet</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {addresses.map((addr) => (
                    <div key={addr.id} className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50">
                      <p className="font-bold text-sm text-slate-900 dark:text-white">{addr.recipient_name}</p>
                      <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">{addr.street_address}</p>
                      <p className="text-xs text-slate-600 dark:text-slate-400">{addr.city}, {addr.state} {addr.postal_code}</p>
                      <p className="text-xs text-slate-500 mt-1">{addr.phone_number}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
