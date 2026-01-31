# PULSE Dashboard

Production-grade React + TypeScript dashboard for PULSE market intelligence platform.

## Design Aesthetic

**Terminal Luxe** - High-end trading terminal meets editorial design
- Deep navy base with electric cyan accents
- JetBrains Mono for data, Inter for headlines
- Glassmorphism panels with subtle animations
- Real-time data streams with pulse effects

## Features

- **Hot Topics**: Top market insights with confidence scores and sentiment
- **Live Signal Feed**: Real-time Reddit signals with engagement metrics
- **Asset Watchlist**: Track specific tickers with related insights
- **Sentiment Radar**: Visual sentiment distribution across insights
- **Stats Overview**: Dashboard metrics and KPIs

## Tech Stack

- **React 19** + **TypeScript**
- **Vite** - Fast build tooling
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **TanStack Query** - Data fetching & caching
- **Recharts** - Data visualization
- **Axios** - HTTP client

## Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

For production, update to your deployed API URL.

## API Endpoints

The frontend connects to the PULSE FastAPI backend:

- `GET /api/insights` - Market insights
- `GET /api/signals` - Reddit signals
- `GET /api/stats` - Dashboard statistics

## Deployment

### Vercel (Recommended)

```bash
npm run build
vercel --prod
```

Environment variables to set in Vercel:
- `VITE_API_URL` - Your production API URL

### Railway

Railway will auto-detect the Vite configuration and deploy.

## Component Structure

```
src/
├── components/
│   ├── HotTopicsCard.tsx      # Top insights display
│   ├── LiveFeed.tsx            # Real-time signal stream
│   ├── AssetWatchlist.tsx      # Ticker tracking
│   ├── SentimentRadar.tsx      # Sentiment visualization
│   └── StatsOverview.tsx       # KPI cards
├── lib/
│   ├── api.ts                  # API client & types
│   └── utils.ts                # Helper functions
├── App.tsx                     # Main app component
├── main.tsx                    # App entry point
└── index.css                   # Global styles
```

## Design System

### Colors

- **Navy**: `#0a1628` - Background
- **Cyan**: `#00d9ff` - Primary accent
- **Amber**: `#ffa337` - Secondary accent
- **Green**: `#2ed573` - Bullish
- **Red**: `#ff4757` - Bearish

### Components

- `.glass-panel` - Glassmorphic card
- `.sentiment-{bullish|bearish|neutral}` - Sentiment badges
- `.confidence-badge` - Confidence score display
- `.btn-primary` - Primary button
- `.gradient-text` - Cyan to amber gradient

## Performance

- Auto-refreshing data every 30 seconds
- React Query caching for optimal performance
- Lazy loading with Framer Motion
- Optimized bundle size with Vite

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

Part of the PULSE project
