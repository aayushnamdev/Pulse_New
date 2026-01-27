"""
PULSE - Relevance Filter Configuration (v2)
==========================================
Filters out low-quality posts like "should I buy", "rate my portfolio", etc.
based on keywords and flairs per subreddit.
"""

# Subreddit-specific filtering rules
RELEVANCE_CONFIG = {
    "investing": {
        "enabled": True,
        "exclude_keywords": [
            "should i buy",
            "should i sell",
            "rate my portfolio",
            "what should i do",
            "inherited",
            "windfall",
            "help me decide"
        ]
    },

    "stocks": {
        "enabled": True,
        "exclude_keywords": [
            "should i buy",
            "should i sell",
            "rate my portfolio",
            "what stock should",
            "help me decide"
        ]
    },

    "technology": {
        "enabled": True,
        "exclude_keywords": [
            "which should i buy",
            "best phone",
            "best laptop",
            "what should i get",
            "recommend",
            "vs for me",
            "is this worth it for me"
        ],
        "exclude_flairs": ["AskTechnology", "Review"]
    },

    "hardware": {
        "enabled": True,
        "exclude_keywords": [
            "build help",
            "help me build",
            "which gpu",
            "upgrade my",
            "bottleneck",
            "my pc won't",
            "won't boot"
        ],
        "exclude_flairs": ["Build Help", "Troubleshooting"]
    },

    "energy": {
        "enabled": True,
        "exclude_keywords": [
            "save the planet",
            "climate denial",
            "political rant"
        ]
    },

    "semiconductors": {
        "enabled": True,
        "exclude_keywords": [
            "career",
            "job",
            "resume",
            "theoretical",
            "homework"
        ]
    },

    "economics": {
        "enabled": True,
        "exclude_keywords": [
            "eli5",
            "debate",
            "theory",
            "opinion"
        ]
    }
}

# Global exclusion patterns that apply to all subreddits
GLOBAL_EXCLUDE_PATTERNS = [
    "should i buy",
    "should i sell",
    "what should i buy",
    "help me choose",
    "rate my",
    "my build",
    "is this worth it for me",
    "recommend me",
    "what laptop should i",
    "what phone should i",
    "which should i get",
    "weekly earnings thread"
]


def is_relevant(post: dict) -> bool:
    """
    Check if a post is relevant based on content and subreddit-specific rules.

    Args:
        post: Dictionary containing post data with keys:
              - title: Post title
              - content: Post body text
              - subreddit: Name of the subreddit
              - flair: Post flair (optional)

    Returns:
        True if post is relevant (should be kept), False if should be filtered out
    """
    # Combine title and content for keyword matching
    text = f"{str(post.get('title', ''))} {str(post.get('content', ''))}".lower()
    subreddit = str(post.get("subreddit", "")).lower()
    flair = str(post.get("flair", "")).strip()

    # Check global exclusion patterns first
    for pattern in GLOBAL_EXCLUDE_PATTERNS:
        if pattern in text:
            return False

    # Check subreddit-specific exclusions
    if subreddit in RELEVANCE_CONFIG:
        config = RELEVANCE_CONFIG[subreddit]

        # Skip if filtering is not enabled for this subreddit
        if not config.get("enabled", True):
            return True

        # Check excluded keywords
        for pattern in config.get("exclude_keywords", []):
            if pattern in text:
                return False

        # Check excluded flairs
        excluded_flairs = config.get("exclude_flairs", [])
        if flair and excluded_flairs:
            for excluded_flair in excluded_flairs:
                if excluded_flair.lower() == flair.lower():
                    return False

    # Post passed all filters
    return True


def get_filter_stats(posts: list) -> dict:
    """
    Get statistics on how many posts were filtered and why.

    Args:
        posts: List of post dictionaries

    Returns:
        Dictionary with filtering statistics
    """
    total = len(posts)
    relevant = sum(1 for post in posts if is_relevant(post))
    filtered = total - relevant

    return {
        "total_posts": total,
        "relevant_posts": relevant,
        "filtered_posts": filtered,
        "filter_rate": round((filtered / total * 100), 2) if total > 0 else 0
    }
