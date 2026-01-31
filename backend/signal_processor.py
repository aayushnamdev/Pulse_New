"""
PULSE Intelligence Layer - Signal Processor
===========================================
Transforms raw Reddit signals into actionable market insights using multi-AI analysis.

Architecture:
- SmartQueue: Fetches unprocessed signals sorted by velocity
- TickerExtractor: 3-layer hybrid extraction (regex, dictionary, Gemini)
- SentimentScorer: Batch sentiment analysis (GPT-4o-mini)
- ClaudeSynthesizer: Insight synthesis (Claude Sonnet 4.5)
- Orchestrator: Full pipeline execution

Usage:
    processor = SignalProcessor()
    result = await processor.run(batch_size=30, dry_run=False)
"""

import os
import re
import json
import asyncio
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
import logging

# AI clients
from anthropic import Anthropic
from openai import OpenAI

# Database service
from database_service import DatabaseService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SmartQueue:
    """
    Manages signal queue from raw_signals table.
    Fetches unprocessed signals sorted by engagement velocity.
    """

    def __init__(self, db_service: DatabaseService):
        self.db = db_service

    def fetch_unprocessed_signals(self, limit: int = 30) -> List[Dict]:
        """
        Query Supabase for unprocessed signals sorted by velocity.

        Query:
            SELECT * FROM raw_signals
            WHERE processed = FALSE
            ORDER BY (engagement_metrics->>'velocity')::float DESC NULLS LAST
            LIMIT {limit}

        Args:
            limit: Maximum number of signals to fetch

        Returns:
            List of signal dictionaries with all columns
        """
        try:
            logger.info(f"Fetching up to {limit} unprocessed signals...")

            # Query with velocity sorting
            response = (
                self.db.client
                .table('raw_signals')
                .select('*')
                .eq('processed', False)
                .order('engagement_metrics->velocity', desc=True)
                .limit(limit)
                .execute()
            )

            signals = response.data
            logger.info(f"✅ Fetched {len(signals)} unprocessed signals")

            return signals

        except Exception as e:
            logger.error(f"❌ Error fetching signals: {str(e)}")
            return []

    def mark_as_processed(
        self,
        signal_ids: List[str],
        extracted_entities: Dict[str, Dict],
        sentiment_scores: Dict[str, float]
    ) -> bool:
        """
        Mark signals as processed and update extracted_entities + sentiment_score.

        Args:
            signal_ids: List of signal UUIDs to mark as processed
            extracted_entities: Dict mapping signal_id -> {tickers, companies, keywords}
            sentiment_scores: Dict mapping signal_id -> sentiment_score

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Marking {len(signal_ids)} signals as processed...")

            for signal_id in signal_ids:
                entities = extracted_entities.get(signal_id, {})
                sentiment = sentiment_scores.get(signal_id, 0.0)

                self.db.client.table('raw_signals').update({
                    'processed': True,
                    'extracted_entities': entities,
                    'sentiment_score': sentiment
                }).eq('id', signal_id).execute()

            logger.info("✅ Successfully marked signals as processed")
            return True

        except Exception as e:
            logger.error(f"❌ Error marking signals as processed: {str(e)}")
            return False


class TickerExtractor:
    """
    2-layer hybrid ticker extraction (Gemini removed due to deprecation).

    Layer 1: Regex for $TICKER patterns
    Layer 2: Dictionary lookup from asset_mapping.json
    """

    def __init__(self, asset_mapping_path: str = 'asset_mapping.json'):
        # Load asset mapping dictionary
        with open(asset_mapping_path, 'r') as f:
            self.asset_mapping = json.load(f)

        # Regex patterns
        self.ticker_pattern = re.compile(r'\$([A-Z]{1,5})\b')
        self.company_pattern = re.compile(
            r'\b(' + '|'.join(re.escape(k) for k in self.asset_mapping.keys()) + r')\b',
            re.IGNORECASE
        )

    def extract_tickers(self, content: str) -> Dict[str, List[str]]:
        """
        Extract tickers using 2-layer hybrid approach (Gemini removed).

        Args:
            content: Post title + body text

        Returns:
            {
                "tickers": ["NVDA", "TSLA"],
                "companies": ["Nvidia", "Tesla"],
                "keywords": []
            }
        """
        # Layer 1: Regex for $TICKER
        regex_tickers = self._extract_regex_tickers(content)

        # Layer 2: Dictionary lookup
        dict_tickers, dict_companies = self._extract_dictionary_tickers(content)

        # Merge and deduplicate
        all_tickers = list(set(regex_tickers + dict_tickers))
        all_companies = list(set(dict_companies))

        return {
            'tickers': all_tickers,
            'companies': all_companies,
            'keywords': []  # Keywords removed with Gemini layer
        }

    def _extract_regex_tickers(self, content: str) -> List[str]:
        """Layer 1: Extract $TICKER patterns."""
        matches = self.ticker_pattern.findall(content)
        return list(set(matches))

    def _extract_dictionary_tickers(self, content: str) -> tuple[List[str], List[str]]:
        """Layer 2: Dictionary lookup for company names."""
        content_lower = content.lower()
        found_tickers = []
        found_companies = []

        for company, ticker in self.asset_mapping.items():
            if company in content_lower:
                found_tickers.append(ticker)
                found_companies.append(company.title())

        return list(set(found_tickers)), list(set(found_companies))



class SentimentScorer:
    """
    Batch sentiment scoring using GPT-4o-mini.
    Processes signals in batches for efficiency.
    """

    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)

    def score_batch_sentiment(
        self,
        signals: List[Dict],
        batch_size: int = 15
    ) -> Dict[str, float]:
        """
        Score sentiment for a batch of signals using GPT-4o-mini.

        Args:
            signals: List of signal dictionaries with 'id', 'title', 'body'
            batch_size: Number of signals to process per API call

        Returns:
            Dict mapping signal_id -> sentiment_score (-1.0 to 1.0)
        """
        all_scores = {}

        # Process in batches
        for i in range(0, len(signals), batch_size):
            batch = signals[i:i + batch_size]
            batch_scores = self._score_batch(batch)
            all_scores.update(batch_scores)

        return all_scores

    def _score_batch(self, batch: List[Dict]) -> Dict[str, float]:
        """Score a single batch of signals."""
        try:
            # Prepare batch data
            batch_data = []
            for signal in batch:
                content = f"{signal.get('title', '')} {signal.get('body', '')}"[:1000]
                batch_data.append({
                    'id': signal['id'],
                    'content': content
                })

            # Create prompt
            prompt = f"""Analyze the sentiment of these financial discussions.
For each signal, return a sentiment score from -1.0 (very bearish) to 1.0 (very bullish).

Signals:
{json.dumps(batch_data, indent=2)}

Return ONLY a JSON object mapping signal IDs to sentiment scores:
{{"signal_id_1": 0.65, "signal_id_2": -0.32, ...}}

Consider:
- Positive: bullish language, excitement, growth mentions
- Negative: bearish language, concern, losses
- Neutral: factual statements, questions

Return ONLY the JSON object, no other text."""

            # Call GPT-4o-mini
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a financial sentiment analysis expert. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            result_text = response.choices[0].message.content.strip()

            # Remove markdown code blocks if present
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]
                result_text = result_text.strip()

            scores = json.loads(result_text)
            logger.info(f"✅ Scored sentiment for {len(scores)} signals")

            return scores

        except Exception as e:
            logger.error(f"❌ Sentiment scoring failed: {str(e)}")
            # Return neutral scores as fallback
            return {signal['id']: 0.0 for signal in batch}


class ClaudeSynthesizer:
    """
    Synthesizes insights from processed signals using Claude Sonnet 4.5.
    Identifies emerging themes, confidence levels, and urgency.
    """

    def __init__(self, anthropic_api_key: str):
        self.client = Anthropic(api_key=anthropic_api_key)

    def synthesize_insights(self, signals: List[Dict]) -> List[Dict]:
        """
        Use Claude Sonnet to synthesize emerging themes from signals.

        Args:
            signals: List of processed signals with extracted_entities and sentiment_score

        Returns:
            List of insight dictionaries ready for database insertion
        """
        try:
            # Prepare synthesis input
            synthesis_input = self._prepare_synthesis_input(signals)

            # Call Claude
            logger.info("Calling Claude for insight synthesis...")
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": self._get_synthesis_prompt(synthesis_input)
                    }
                ]
            )

            result_text = response.content[0].text.strip()

            # Parse Claude's response
            insights = self._parse_synthesis_response(result_text, signals)

            logger.info(f"✅ Generated {len(insights)} insights")
            return insights

        except Exception as e:
            logger.error(f"❌ Claude synthesis failed: {str(e)}")
            return []

    def _prepare_synthesis_input(self, signals: List[Dict]) -> str:
        """Prepare signals for Claude synthesis."""
        synthesis_data = []

        for signal in signals:
            entities = signal.get('extracted_entities', {})
            sentiment = signal.get('sentiment_score', 0.0)

            synthesis_data.append({
                'id': signal['id'],
                'title': signal.get('title', ''),
                'body': signal.get('body', '')[:500],
                'tickers': entities.get('tickers', []),
                'companies': entities.get('companies', []),
                'keywords': entities.get('keywords', []),
                'sentiment': sentiment,
                'upvotes': signal.get('upvotes', 0),
                'subreddit': signal.get('subreddit', '')
            })

        return json.dumps(synthesis_data, indent=2)

    def _get_synthesis_prompt(self, synthesis_input: str) -> str:
        """Get Claude synthesis prompt."""
        return f"""You are a financial intelligence analyst synthesizing market insights from Reddit discussions.

# Input Signals
{synthesis_input}

# Task
Identify 2-5 emerging market themes from these signals. For each theme:

1. **Theme**: Clear, actionable market narrative (max 100 words)
2. **Confidence Score**: 0-1 scale
   - 0.9+: Multiple independent sources strongly agree
   - 0.7-0.9: Single strong signal or moderate multi-source agreement
   - 0.5-0.7: Emerging pattern, needs monitoring
3. **Related Assets**: Tickers that would be impacted
4. **Sentiment**: bullish, bearish, or neutral
5. **Urgency**: immediate (actionable now), developing (watch closely), background (long-term trend)
6. **Sources Agreeing**: Which subreddits/signal IDs support this
7. **Evidence**: Key quotes or data points

# Output Format
Return ONLY a JSON array of insights:

```json
[
  {{
    "theme": "Nvidia supply constraints driving price concerns across semiconductor sector",
    "confidence_score": 0.85,
    "related_assets": ["NVDA", "AMD", "INTC"],
    "sentiment": "bearish",
    "urgency": "developing",
    "sources_agreeing": ["wallstreetbets", "stocks"],
    "evidence": {{
      "key_quotes": ["GPU shortage affecting data centers", "NVDA earnings miss expected"],
      "supporting_signal_ids": ["id1", "id2"]
    }}
  }}
]
```

Focus on themes with confidence > 0.5. Filter out noise and contradictory signals."""

    def _parse_synthesis_response(self, response_text: str, signals: List[Dict]) -> List[Dict]:
        """Parse Claude's response into database-ready insights."""
        try:
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            insights_raw = json.loads(response_text)

            # Transform to database schema
            insights = []
            for insight in insights_raw:
                # Extract signal IDs from evidence
                signal_ids = []
                if 'evidence' in insight and 'supporting_signal_ids' in insight['evidence']:
                    signal_ids = insight['evidence']['supporting_signal_ids']

                # Set expiration (24 hours for immediate, 7 days for others)
                expires_at = None
                if insight.get('urgency') == 'immediate':
                    expires_at = (datetime.now() + timedelta(hours=24)).isoformat()
                elif insight.get('urgency') == 'developing':
                    expires_at = (datetime.now() + timedelta(days=7)).isoformat()

                insights.append({
                    'theme': insight['theme'],
                    'confidence_score': insight['confidence_score'],
                    'sources_agreeing': insight.get('sources_agreeing', []),
                    'related_assets': insight.get('related_assets', []),
                    'sentiment': insight.get('sentiment', 'neutral'),
                    'urgency': insight.get('urgency', 'background'),
                    'evidence': insight.get('evidence', {}),
                    'signal_ids': signal_ids,
                    'expires_at': expires_at
                })

            return insights

        except Exception as e:
            logger.error(f"Failed to parse Claude response: {str(e)}")
            return []


class SignalProcessor:
    """
    Main orchestrator for the intelligence layer.
    Coordinates SmartQueue, TickerExtractor, SentimentScorer, and ClaudeSynthesizer.
    """

    def __init__(self):
        # Load environment variables
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

        # Validate API keys (Gemini removed)
        if not all([self.openai_api_key, self.anthropic_api_key]):
            raise ValueError("Missing required API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY). Check .env file.")

        # Initialize components
        self.db = DatabaseService()
        self.queue = SmartQueue(self.db)
        self.ticker_extractor = TickerExtractor(
            asset_mapping_path='asset_mapping.json'
        )
        self.sentiment_scorer = SentimentScorer(openai_api_key=self.openai_api_key)
        self.synthesizer = ClaudeSynthesizer(anthropic_api_key=self.anthropic_api_key)

        # Configuration
        self.batch_size = int(os.getenv('SIGNAL_PROCESSOR_BATCH_SIZE', 30))
        self.sentiment_batch_size = int(os.getenv('SENTIMENT_BATCH_SIZE', 15))

    async def run(self, batch_size: Optional[int] = None, dry_run: bool = False) -> Dict:
        """
        Execute the full signal processing pipeline.

        Steps:
        1. Fetch unprocessed signals (velocity DESC)
        2. Extract tickers (3-layer hybrid)
        3. Score sentiment (GPT-4o-mini batches)
        4. Synthesize insights (Claude)
        5. Update raw_signals (extracted_entities, sentiment_score, processed=TRUE)
        6. Insert insights into insights table

        Args:
            batch_size: Number of signals to process (default: from env or 30)
            dry_run: If True, don't save to database (for testing)

        Returns:
            Dict with processing statistics
        """
        logger.info("=" * 60)
        logger.info("PULSE Intelligence Layer - Signal Processing Pipeline")
        logger.info("=" * 60)

        batch_size = batch_size or self.batch_size

        try:
            # Step 1: Fetch unprocessed signals
            logger.info(f"\n[1/5] Fetching up to {batch_size} unprocessed signals...")
            signals = self.queue.fetch_unprocessed_signals(limit=batch_size)

            if not signals:
                logger.warning("No unprocessed signals found.")
                return {'processed_count': 0, 'insights_count': 0, 'tickers_count': 0}

            logger.info(f"Processing {len(signals)} signals...")

            # Step 2: Extract tickers (3-layer hybrid)
            logger.info("\n[2/5] Extracting tickers and entities...")
            extracted_entities = {}

            for signal in signals:
                content = f"{signal.get('title', '')} {signal.get('body', '')}"
                entities = self.ticker_extractor.extract_tickers(content)
                extracted_entities[signal['id']] = entities

            total_tickers = len(set(
                ticker
                for entities in extracted_entities.values()
                for ticker in entities.get('tickers', [])
            ))
            logger.info(f"✅ Extracted {total_tickers} unique tickers")

            # Step 3: Score sentiment (GPT-4o-mini)
            logger.info("\n[3/5] Scoring sentiment with GPT-4o-mini...")
            sentiment_scores = self.sentiment_scorer.score_batch_sentiment(
                signals,
                batch_size=self.sentiment_batch_size
            )

            # Update signals with extracted data
            for signal in signals:
                signal['extracted_entities'] = extracted_entities.get(signal['id'], {})
                signal['sentiment_score'] = sentiment_scores.get(signal['id'], 0.0)

            # Step 4: Synthesize insights (Claude)
            logger.info("\n[4/5] Synthesizing insights with Claude Sonnet...")
            insights = self.synthesizer.synthesize_insights(signals)

            # Step 5 & 6: Save to database
            if not dry_run:
                logger.info("\n[5/5] Saving to database...")

                # Mark signals as processed
                signal_ids = [s['id'] for s in signals]
                self.queue.mark_as_processed(signal_ids, extracted_entities, sentiment_scores)

                # Insert insights
                if insights:
                    self.db.client.table('insights').insert(insights).execute()
                    logger.info(f"✅ Inserted {len(insights)} insights")
            else:
                logger.info("\n[5/5] DRY RUN - Skipping database writes")

            # Summary
            logger.info("\n" + "=" * 60)
            logger.info("PROCESSING COMPLETE")
            logger.info("=" * 60)
            logger.info(f"Signals processed: {len(signals)}")
            logger.info(f"Unique tickers extracted: {total_tickers}")
            logger.info(f"Insights generated: {len(insights)}")
            logger.info(f"Database writes: {'COMPLETED' if not dry_run else 'SKIPPED (dry run)'}")

            return {
                'processed_count': len(signals),
                'insights_count': len(insights),
                'tickers_count': total_tickers,
                'extracted_entities': extracted_entities,
                'sentiment_scores': sentiment_scores,
                'insights': insights
            }

        except Exception as e:
            logger.error(f"\n❌ Pipeline failed: {str(e)}", exc_info=True)
            raise
