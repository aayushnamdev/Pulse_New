import axios from 'axios';

// API base URL - update this for production
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface Insight {
  id: string;
  theme: string;
  confidence_score: number;
  related_assets: string[];
  sentiment: 'bullish' | 'bearish' | 'neutral';
  urgency: 'immediate' | 'developing' | 'background';
  evidence: {
    key_quotes: string[];
    supporting_signal_ids: string[];
  };
  sources_agreeing: string[];
  created_at: string;
  expires_at?: string;
}

export interface Signal {
  id: string;
  title: string;
  body: string;
  source: string;
  source_id: string;
  source_url: string;
  subreddit: string;
  author_id: string;
  upvotes: number;
  engagement_metrics: {
    num_comments: number;
    upvote_ratio: number;
    velocity: number;
  };
  extracted_entities: {
    tickers: string[];
    companies: string[];
    keywords: string[];
  };
  sentiment_score: number;
  is_quality_signal: boolean;
  scraped_at: string;
  processed: boolean;
}

export interface DashboardStats {
  total_signals: number;
  total_insights: number;
  signals_24h: number;
  insights_24h: number;
  quality_signals: number;
  top_tickers: Array<{
    ticker: string;
    mention_count: number;
  }>;
  avg_confidence: number;
  sentiment_distribution: {
    bullish: number;
    bearish: number;
    neutral: number;
  };
  active_subreddits: Array<{
    subreddit: string;
    signal_count: number;
  }>;
  last_scrape: string;
  last_insight: string;
}

// API functions
export const fetchInsights = async (params?: {
  limit?: number;
  offset?: number;
  min_confidence?: number;
  sentiment?: string;
}) => {
  const response = await api.get<{
    insights: Insight[];
    total: number;
    limit: number;
    offset: number;
  }>('/insights', { params });
  return response.data;
};

export const fetchSignals = async (params?: {
  limit?: number;
  offset?: number;
  is_quality_signal?: boolean;
  subreddit?: string;
  hours?: number;
}) => {
  const response = await api.get<{
    signals: Signal[];
    total: number;
    limit: number;
    offset: number;
  }>('/signals', { params });
  return response.data;
};

export const fetchStats = async () => {
  const response = await api.get<DashboardStats>('/stats');
  return response.data;
};

export const fetchInsightsByAsset = async (symbol: string, params?: {
  limit?: number;
  offset?: number;
}) => {
  const response = await api.get<{
    insights: Insight[];
    asset: string;
    total: number;
  }>(`/insights/asset/${symbol}`, { params });
  return response.data;
};
