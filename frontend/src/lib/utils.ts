import { type ClassValue, clsx } from 'clsx';

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

export function formatTimeAgo(date: string): string {
  const now = new Date();
  const past = new Date(date);
  const diffMs = now.getTime() - past.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  return `${diffDays}d ago`;
}

export function formatNumber(num: number): string {
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M`;
  }
  if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`;
  }
  return num.toString();
}

export function getSentimentColor(sentiment: string): string {
  switch (sentiment) {
    case 'bullish':
      return 'text-pulse-green';
    case 'bearish':
      return 'text-pulse-red';
    default:
      return 'text-gray-400';
  }
}

export function getSentimentBadgeClass(sentiment: string): string {
  switch (sentiment) {
    case 'bullish':
      return 'sentiment-bullish';
    case 'bearish':
      return 'sentiment-bearish';
    default:
      return 'sentiment-neutral';
  }
}

export function getUrgencyColor(urgency: string): string {
  switch (urgency) {
    case 'immediate':
      return 'text-pulse-red';
    case 'developing':
      return 'text-pulse-amber';
    default:
      return 'text-gray-400';
  }
}

export function formatConfidence(confidence: number): string {
  return `${(confidence * 100).toFixed(0)}%`;
}
