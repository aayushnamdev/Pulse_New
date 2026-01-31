import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useQuery } from '@tanstack/react-query';
import { fetchInsightsByAsset } from '../lib/api';
import { formatNumber, getSentimentBadgeClass } from '../lib/utils';

interface AssetWatchlistProps {
  topTickers: Array<{ ticker: string; mention_count: number }>;
}

export function AssetWatchlist({ topTickers }: AssetWatchlistProps) {
  const [selectedAsset, setSelectedAsset] = useState<string | null>(null);
  const [watchlist, setWatchlist] = useState<string[]>(['NVDA', 'TSLA', 'AMD']);

  const { data: assetInsights, isLoading } = useQuery({
    queryKey: ['asset-insights', selectedAsset],
    queryFn: () => fetchInsightsByAsset(selectedAsset!, { limit: 3 }),
    enabled: !!selectedAsset,
  });

  const addToWatchlist = (ticker: string) => {
    if (!watchlist.includes(ticker)) {
      setWatchlist([...watchlist, ticker]);
    }
  };

  const removeFromWatchlist = (ticker: string) => {
    setWatchlist(watchlist.filter((t) => t !== ticker));
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="glass-panel p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <h2 className="headline">Asset Watchlist</h2>
        <span className="text-xs font-mono text-gray-400">{watchlist.length} tracked</span>
      </div>

      {/* Watchlist Items */}
      <div className="space-y-3 mb-6">
        <AnimatePresence>
          {watchlist.map((ticker, index) => {
            const tickerData = topTickers.find((t) => t.ticker === ticker);
            const isSelected = selectedAsset === ticker;

            return (
              <motion.div
                key={ticker}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ delay: index * 0.05 }}
                className={`glass-panel-hover p-4 cursor-pointer ${
                  isSelected ? 'border-pulse-cyan/60' : ''
                }`}
                onClick={() => setSelectedAsset(isSelected ? null : ticker)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-pulse-cyan/20 to-pulse-amber/20 flex items-center justify-center border border-pulse-cyan/30">
                      <span className="font-mono font-bold text-sm text-pulse-cyan">
                        ${ticker}
                      </span>
                    </div>
                    <div>
                      <div className="font-semibold text-sm text-gray-100">{ticker}</div>
                      {tickerData && (
                        <div className="text-xs font-mono text-gray-500">
                          {formatNumber(tickerData.mention_count)} mentions
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {isSelected && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="w-2 h-2 rounded-full bg-pulse-cyan"
                      />
                    )}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        removeFromWatchlist(ticker);
                      }}
                      className="text-gray-600 hover:text-pulse-red transition-colors"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                </div>

                {/* Expanded insights */}
                <AnimatePresence>
                  {isSelected && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3 }}
                      className="overflow-hidden"
                    >
                      <div className="mt-4 pt-4 border-t border-gray-800">
                        {isLoading ? (
                          <div className="space-y-2">
                            <div className="skeleton h-16 rounded" />
                            <div className="skeleton h-16 rounded" />
                          </div>
                        ) : assetInsights && assetInsights.insights.length > 0 ? (
                          <div className="space-y-3">
                            <div className="text-xs font-mono text-gray-500 mb-2">
                              {assetInsights.insights.length} related insights
                            </div>
                            {assetInsights.insights.map((insight) => (
                              <div
                                key={insight.id}
                                className="text-sm p-3 rounded-lg bg-pulse-navy/30 border border-gray-800"
                              >
                                <div className="flex items-start gap-2 mb-2">
                                  <span className={`px-2 py-0.5 rounded text-xs ${getSentimentBadgeClass(insight.sentiment)}`}>
                                    {insight.sentiment}
                                  </span>
                                  <span className="confidence-badge text-xs">
                                    {(insight.confidence_score * 100).toFixed(0)}%
                                  </span>
                                </div>
                                <p className="text-gray-300 line-clamp-2">{insight.theme}</p>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <div className="text-center py-4 text-gray-600 text-sm">
                            No insights found for ${ticker}
                          </div>
                        )}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>

      {/* Add from top tickers */}
      {topTickers.length > 0 && (
        <div>
          <div className="text-xs font-mono text-gray-500 mb-3">Trending Tickers</div>
          <div className="flex flex-wrap gap-2">
            {topTickers
              .filter((t) => !watchlist.includes(t.ticker))
              .slice(0, 6)
              .map((ticker) => (
                <motion.button
                  key={ticker.ticker}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => addToWatchlist(ticker.ticker)}
                  className="font-mono text-xs px-3 py-1.5 rounded-lg bg-pulse-navy/50 text-gray-400 border border-gray-700 hover:border-pulse-cyan/40 hover:text-pulse-cyan transition-all"
                >
                  ${ticker.ticker}
                  <span className="ml-1.5 text-gray-600">
                    {formatNumber(ticker.mention_count)}
                  </span>
                </motion.button>
              ))}
          </div>
        </div>
      )}
    </motion.div>
  );
}
