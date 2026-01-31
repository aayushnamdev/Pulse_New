import { motion, AnimatePresence } from 'framer-motion';
import { Signal } from '../lib/api';
import { formatTimeAgo, formatNumber } from '../lib/utils';

interface LiveFeedProps {
  signals: Signal[];
  isLoading?: boolean;
}

export function LiveFeed({ signals, isLoading }: LiveFeedProps) {
  if (isLoading) {
    return (
      <div className="glass-panel p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="headline">Live Signal Feed</h2>
        </div>
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="skeleton h-24 rounded-lg" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.1 }}
      className="glass-panel p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <h2 className="headline">Live Signal Feed</h2>
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-pulse-cyan">{signals.length} signals</span>
        </div>
      </div>

      <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
        <AnimatePresence mode="popLayout">
          {signals.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p className="font-mono text-sm">No signals detected</p>
              <p className="text-xs mt-2">Waiting for market activity...</p>
            </div>
          ) : (
            signals.map((signal, index) => (
              <motion.div
                key={signal.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ delay: index * 0.05, duration: 0.3 }}
                className="glass-panel-hover p-4 cursor-pointer group"
              >
                {/* Header */}
                <div className="flex items-start justify-between mb-2">
                  <div className="flex-1 min-w-0">
                    <h3 className="text-sm font-semibold text-gray-100 group-hover:text-pulse-cyan transition-colors line-clamp-2 mb-2">
                      {signal.title}
                    </h3>
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="font-mono text-xs px-2 py-0.5 rounded bg-pulse-navy/50 text-gray-400 border border-gray-700">
                        r/{signal.subreddit}
                      </span>
                      {signal.is_quality_signal && (
                        <span className="font-mono text-xs px-2 py-0.5 rounded bg-pulse-green/10 text-pulse-green border border-pulse-green/30">
                          QUALITY
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Tickers */}
                {signal.extracted_entities?.tickers && signal.extracted_entities.tickers.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mb-3">
                    {signal.extracted_entities.tickers.slice(0, 4).map((ticker) => (
                      <span
                        key={ticker}
                        className="font-mono text-xs px-2 py-0.5 rounded bg-pulse-cyan/10 text-pulse-cyan border border-pulse-cyan/30"
                      >
                        ${ticker}
                      </span>
                    ))}
                    {signal.extracted_entities.tickers.length > 4 && (
                      <span className="font-mono text-xs px-2 py-0.5 text-gray-500">
                        +{signal.extracted_entities.tickers.length - 4}
                      </span>
                    )}
                  </div>
                )}

                {/* Metrics */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4 text-xs font-mono text-gray-500">
                    <div className="flex items-center gap-1">
                      <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
                      </svg>
                      <span className="text-pulse-cyan">{formatNumber(signal.upvotes)}</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
                      </svg>
                      <span>{formatNumber(signal.engagement_metrics?.num_comments || 0)}</span>
                    </div>
                    {signal.engagement_metrics?.velocity && (
                      <div className="flex items-center gap-1">
                        <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clipRule="evenodd" />
                        </svg>
                        <span className="text-pulse-amber">{signal.engagement_metrics.velocity.toFixed(0)}/h</span>
                      </div>
                    )}
                  </div>
                  <span className="text-xs font-mono text-gray-600">
                    {formatTimeAgo(signal.scraped_at)}
                  </span>
                </div>

                {/* Sentiment indicator */}
                {signal.sentiment_score !== undefined && signal.sentiment_score !== null && (
                  <div className="mt-3 pt-3 border-t border-gray-800">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-mono text-gray-500">Sentiment</span>
                      <div className="flex items-center gap-2">
                        <div className="w-24 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${((signal.sentiment_score + 1) / 2) * 100}%` }}
                            transition={{ delay: index * 0.05 + 0.3, duration: 0.5 }}
                            className={`h-full ${
                              signal.sentiment_score > 0.2
                                ? 'bg-pulse-green'
                                : signal.sentiment_score < -0.2
                                ? 'bg-pulse-red'
                                : 'bg-gray-500'
                            }`}
                          />
                        </div>
                        <span className={`font-mono ${
                          signal.sentiment_score > 0.2
                            ? 'text-pulse-green'
                            : signal.sentiment_score < -0.2
                            ? 'text-pulse-red'
                            : 'text-gray-500'
                        }`}>
                          {signal.sentiment_score.toFixed(2)}
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}
