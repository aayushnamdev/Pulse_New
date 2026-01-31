import { motion } from 'framer-motion';
import { Insight } from '../lib/api';
import { formatTimeAgo, formatConfidence, getSentimentBadgeClass } from '../lib/utils';

interface HotTopicsCardProps {
  insights: Insight[];
  isLoading?: boolean;
}

export function HotTopicsCard({ insights, isLoading }: HotTopicsCardProps) {
  if (isLoading) {
    return (
      <div className="glass-panel p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="headline gradient-text">Hot Topics</h2>
          <div className="w-2 h-2 rounded-full bg-pulse-cyan animate-pulse" />
        </div>
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="skeleton h-32 rounded-lg" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="glass-panel p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <h2 className="headline gradient-text">Hot Topics</h2>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-pulse-cyan relative">
            <div className="absolute inset-0 rounded-full bg-pulse-cyan animate-ping" />
          </div>
          <span className="text-xs font-mono text-gray-400">LIVE</span>
        </div>
      </div>

      <div className="space-y-4">
        {insights.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <p className="font-mono text-sm">No insights available yet</p>
            <p className="text-xs mt-2">Check back soon for market intelligence</p>
          </div>
        ) : (
          insights.map((insight, index) => (
            <motion.div
              key={insight.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1, duration: 0.3 }}
              className="glass-panel-hover p-4 cursor-pointer group"
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`px-2 py-0.5 rounded-md text-xs font-medium ${getSentimentBadgeClass(insight.sentiment)}`}>
                      {insight.sentiment.toUpperCase()}
                    </span>
                    <span className="confidence-badge">
                      {formatConfidence(insight.confidence_score)}
                    </span>
                    {insight.urgency === 'immediate' && (
                      <span className="px-2 py-0.5 rounded-md text-xs font-medium bg-pulse-red/10 text-pulse-red border border-pulse-red/30">
                        URGENT
                      </span>
                    )}
                  </div>
                  <h3 className="text-base font-semibold text-gray-100 group-hover:text-pulse-cyan transition-colors">
                    {insight.theme}
                  </h3>
                </div>
              </div>

              {/* Related Assets */}
              {insight.related_assets && insight.related_assets.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-3">
                  {insight.related_assets.slice(0, 5).map((asset) => (
                    <span
                      key={asset}
                      className="font-mono text-xs px-2 py-1 rounded bg-pulse-navy/50 text-pulse-cyan border border-pulse-cyan/20 hover:border-pulse-cyan/40 transition-colors"
                    >
                      ${asset}
                    </span>
                  ))}
                  {insight.related_assets.length > 5 && (
                    <span className="font-mono text-xs px-2 py-1 text-gray-500">
                      +{insight.related_assets.length - 5} more
                    </span>
                  )}
                </div>
              )}

              {/* Evidence Preview */}
              {insight.evidence?.key_quotes && insight.evidence.key_quotes.length > 0 && (
                <div className="border-l-2 border-pulse-cyan/30 pl-3 mb-3">
                  <p className="text-sm text-gray-400 italic line-clamp-2">
                    "{insight.evidence.key_quotes[0]}"
                  </p>
                </div>
              )}

              {/* Footer */}
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-3 text-gray-500 font-mono">
                  <span>{insight.sources_agreeing?.length || 0} sources</span>
                  <span>•</span>
                  <span>{formatTimeAgo(insight.created_at)}</span>
                </div>
                <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                  <svg className="w-4 h-4 text-pulse-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </motion.div>
          ))
        )}
      </div>

      {insights.length > 0 && (
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="w-full mt-4 btn-secondary text-sm"
        >
          View All Insights
        </motion.button>
      )}
    </motion.div>
  );
}
