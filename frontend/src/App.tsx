import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { fetchInsights, fetchSignals, fetchStats } from './lib/api';
import { HotTopicsCard } from './components/HotTopicsCard';
import { LiveFeed } from './components/LiveFeed';
import { AssetWatchlist } from './components/AssetWatchlist';
import { SentimentRadar } from './components/SentimentRadar';
import { StatsOverview } from './components/StatsOverview';

function App() {
  // Fetch insights
  const { data: insightsData, isLoading: insightsLoading } = useQuery({
    queryKey: ['insights'],
    queryFn: () => fetchInsights({ limit: 5, min_confidence: 0.7 }),
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  // Fetch signals
  const { data: signalsData, isLoading: signalsLoading } = useQuery({
    queryKey: ['signals'],
    queryFn: () => fetchSignals({ limit: 10, hours: 24 }),
    refetchInterval: 30000,
  });

  // Fetch stats
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['stats'],
    queryFn: fetchStats,
    refetchInterval: 60000, // Refresh every minute
  });

  return (
    <div className="min-h-screen p-4 md:p-6 lg:p-8">
      {/* Header */}
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex items-center justify-between mb-2">
          <div>
            <h1 className="text-4xl md:text-5xl font-bold gradient-text text-shadow-glow mb-2">
              PULSE
            </h1>
            <p className="text-gray-400 font-mono text-sm">
              Market Intelligence • Real-time Reddit Signals
            </p>
          </div>
          <div className="text-right">
            <div className="inline-flex items-center gap-2 px-4 py-2 glass-panel">
              <div className="w-2 h-2 rounded-full bg-pulse-green relative">
                <div className="absolute inset-0 rounded-full bg-pulse-green animate-ping" />
              </div>
              <span className="font-mono text-xs text-gray-400">SYSTEM OPERATIONAL</span>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Stats Overview */}
      <StatsOverview stats={stats || null} isLoading={statsLoading} />

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Hot Topics (spans 2 columns on large screens) */}
        <div className="lg:col-span-2 space-y-6">
          <HotTopicsCard
            insights={insightsData?.insights || []}
            isLoading={insightsLoading}
          />
          <LiveFeed
            signals={signalsData?.signals || []}
            isLoading={signalsLoading}
          />
        </div>

        {/* Right Column - Watchlist & Sentiment */}
        <div className="space-y-6">
          <AssetWatchlist
            topTickers={stats?.top_tickers || []}
          />
          <SentimentRadar
            sentimentDistribution={stats?.sentiment_distribution || { bullish: 0, bearish: 0, neutral: 0 }}
            isLoading={statsLoading}
          />
        </div>
      </div>

      {/* Footer */}
      <motion.footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="mt-12 text-center"
      >
        <div className="glass-panel inline-block px-6 py-3">
          <p className="text-xs font-mono text-gray-500">
            Powered by{' '}
            <span className="text-pulse-cyan">Claude Sonnet 4.5</span>
            {' • '}
            <span className="text-pulse-amber">GPT-4o-mini</span>
            {' • '}
            Data from {stats?.active_subreddits.length || 0} subreddits
          </p>
        </div>
      </motion.footer>
    </div>
  );
}

export default App;
