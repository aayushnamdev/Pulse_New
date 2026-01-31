import { motion } from 'framer-motion';
import { DashboardStats } from '../lib/api';
import { formatNumber, formatTimeAgo } from '../lib/utils';

interface StatsOverviewProps {
  stats: DashboardStats | null;
  isLoading?: boolean;
}

export function StatsOverview({ stats, isLoading }: StatsOverviewProps) {
  if (isLoading || !stats) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="skeleton h-24 rounded-xl" />
        ))}
      </div>
    );
  }

  const statCards = [
    {
      label: 'Total Signals',
      value: formatNumber(stats.total_signals),
      subValue: `+${stats.signals_24h} today`,
      icon: (
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
        </svg>
      ),
      color: 'text-pulse-cyan',
      bg: 'bg-pulse-cyan/10',
    },
    {
      label: 'Insights Generated',
      value: formatNumber(stats.total_insights),
      subValue: `${(stats.avg_confidence * 100).toFixed(0)}% avg confidence`,
      icon: (
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
          <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
        </svg>
      ),
      color: 'text-pulse-amber',
      bg: 'bg-pulse-amber/10',
    },
    {
      label: 'Quality Signals',
      value: formatNumber(stats.quality_signals),
      subValue: `${((stats.quality_signals / stats.total_signals) * 100).toFixed(1)}% filtered`,
      icon: (
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
        </svg>
      ),
      color: 'text-pulse-green',
      bg: 'bg-pulse-green/10',
    },
    {
      label: 'Active Subreddits',
      value: stats.active_subreddits.length.toString(),
      subValue: stats.last_scrape ? `Last: ${formatTimeAgo(stats.last_scrape)}` : 'No data',
      icon: (
        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z" />
        </svg>
      ),
      color: 'text-gray-400',
      bg: 'bg-gray-500/10',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {statCards.map((stat, index) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1, duration: 0.3 }}
          className="stat-card group cursor-pointer hover:border-pulse-cyan/40 transition-all"
        >
          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs font-mono text-gray-500 mb-1">{stat.label}</p>
              <p className={`text-2xl font-bold font-mono ${stat.color} group-hover:text-shadow-glow transition-all`}>
                {stat.value}
              </p>
              <p className="text-xs font-mono text-gray-600 mt-1">{stat.subValue}</p>
            </div>
            <div className={`${stat.bg} ${stat.color} p-2 rounded-lg group-hover:scale-110 transition-transform`}>
              {stat.icon}
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
