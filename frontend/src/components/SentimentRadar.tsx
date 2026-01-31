import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

interface SentimentRadarProps {
  sentimentDistribution: {
    bullish: number;
    bearish: number;
    neutral: number;
  };
  isLoading?: boolean;
}

export function SentimentRadar({ sentimentDistribution, isLoading }: SentimentRadarProps) {
  const data = [
    { name: 'Bullish', value: sentimentDistribution.bullish, color: '#2ed573' },
    { name: 'Bearish', value: sentimentDistribution.bearish, color: '#ff4757' },
    { name: 'Neutral', value: sentimentDistribution.neutral, color: '#6b7280' },
  ];

  const total = data.reduce((sum, item) => sum + item.value, 0);

  if (isLoading) {
    return (
      <div className="glass-panel p-6">
        <h2 className="headline mb-6">Sentiment Radar</h2>
        <div className="skeleton h-64 rounded-lg" />
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      className="glass-panel p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <h2 className="headline">Sentiment Radar</h2>
        <span className="text-xs font-mono text-gray-400">{total} insights</span>
      </div>

      {total === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p className="font-mono text-sm">No sentiment data</p>
        </div>
      ) : (
        <>
          {/* Chart */}
          <div className="relative h-64 mb-6">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={2}
                  dataKey="value"
                  animationBegin={0}
                  animationDuration={800}
                >
                  {data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      const data = payload[0].payload;
                      return (
                        <div className="glass-panel px-3 py-2">
                          <p className="text-xs font-mono text-gray-400">{data.name}</p>
                          <p className="text-sm font-semibold" style={{ color: data.color }}>
                            {data.value} ({((data.value / total) * 100).toFixed(1)}%)
                          </p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
              </PieChart>
            </ResponsiveContainer>

            {/* Center label */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className="text-center">
                <div className="text-2xl font-bold font-mono gradient-text">
                  {total}
                </div>
                <div className="text-xs font-mono text-gray-500">Total</div>
              </div>
            </div>
          </div>

          {/* Legend */}
          <div className="space-y-3">
            {data.map((item, index) => {
              const percentage = total > 0 ? (item.value / total) * 100 : 0;
              return (
                <motion.div
                  key={item.name}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.5 + index * 0.1 }}
                  className="flex items-center justify-between"
                >
                  <div className="flex items-center gap-3 flex-1">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: item.color }}
                    />
                    <span className="text-sm font-medium text-gray-300">{item.name}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="w-32 h-2 bg-gray-800 rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${percentage}%` }}
                        transition={{ delay: 0.5 + index * 0.1, duration: 0.5 }}
                        className="h-full rounded-full"
                        style={{ backgroundColor: item.color }}
                      />
                    </div>
                    <div className="w-16 text-right">
                      <span className="font-mono text-sm font-semibold" style={{ color: item.color }}>
                        {item.value}
                      </span>
                      <span className="font-mono text-xs text-gray-600 ml-1">
                        {percentage.toFixed(0)}%
                      </span>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>

          {/* Market mood */}
          <div className="mt-6 pt-6 border-t border-gray-800">
            <div className="text-xs font-mono text-gray-500 mb-2">Market Mood</div>
            <div className="text-lg font-bold">
              {sentimentDistribution.bullish > sentimentDistribution.bearish + sentimentDistribution.neutral ? (
                <span className="text-pulse-green">🚀 Strong Bullish</span>
              ) : sentimentDistribution.bearish > sentimentDistribution.bullish + sentimentDistribution.neutral ? (
                <span className="text-pulse-red">⚠️ Strong Bearish</span>
              ) : sentimentDistribution.bullish > sentimentDistribution.bearish ? (
                <span className="text-pulse-green">📈 Slightly Bullish</span>
              ) : sentimentDistribution.bearish > sentimentDistribution.bullish ? (
                <span className="text-pulse-red">📉 Slightly Bearish</span>
              ) : (
                <span className="text-gray-400">⚖️ Neutral</span>
              )}
            </div>
          </div>
        </>
      )}
    </motion.div>
  );
}
