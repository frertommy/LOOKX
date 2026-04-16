import re
from lookx.x_client import XClient

# Topic categories and their keywords
TOPIC_KEYWORDS = {
    "prediction_markets": [
        "prediction market", "polymarket", "kalshi", "manifold",
        "predictit", "metaculus", "augur", "event contract",
        "binary outcome", "prediction exchange", "forecasting market",
    ],
    "sports_betting": [
        "sports betting", "sportsbook", "fanduel", "draftkings",
        "bet365", "bovada", "sports wagering", "parlay",
        "point spread", "over under", "moneyline", "prop bet",
        "sports gambling", "betting odds", "daily fantasy",
    ],
    "perps_derivatives": [
        "perpetual", "perps", "derivatives", "futures",
        "options trading", "leverage trading", "dydx",
        "gmx", "synthetix", "perpetual protocol", "drift",
        "hyperliquid", "vertex", "margin trading",
    ],
    "gambling_general": [
        "gambling", "wagering", "casino", "odds",
        "house edge", "expected value", "risk reward",
        "gaming regulation", "igaming", "online gambling",
    ],
    "fintech_payments": [
        "fintech", "payments", "neobank", "digital payments",
        "payment processing", "stripe", "square",
    ],
}

# Blog/article domains that signal written thought leadership
BLOG_DOMAINS = [
    "medium.com", "substack.com", "mirror.xyz", "paragraph.xyz",
    "ghost.io", "wordpress.com", "blogspot.com", "notion.so",
    "beehiiv.com", "linkedin.com/pulse", "github.io",
]


def analyze_user_content(client: XClient, user: dict, max_tweets: int = 50) -> dict:
    """Analyze a user's tweets for relevant topic signals.

    Returns an analysis dict with:
    - topic_scores: how many hits per topic category
    - relevant_tweets: tweets that matched keywords
    - blog_links: any links to blog/article platforms
    - total_signal_strength: overall relevance score
    """
    tweets = client.get_user_tweets(user["id"], max_results=max_tweets)

    topic_scores = {topic: 0 for topic in TOPIC_KEYWORDS}
    relevant_tweets = []
    blog_links = []
    all_urls = []

    for tweet in tweets:
        text_lower = tweet["text"].lower()
        matched_topics = []

        for topic, keywords in TOPIC_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    topic_scores[topic] += 1
                    if topic not in matched_topics:
                        matched_topics.append(topic)

        if matched_topics:
            relevant_tweets.append({
                "text": tweet["text"][:280],
                "topics": matched_topics,
                "metrics": tweet["metrics"],
                "date": tweet["created_at"],
            })

        # Collect URLs, check for blog links
        for url in tweet.get("urls", []):
            all_urls.append(url)
            url_lower = url.lower()
            if any(domain in url_lower for domain in BLOG_DOMAINS):
                blog_links.append(url)

    # Also check the user's bio for topic signals
    bio_lower = user["bio"].lower()
    bio_topics = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            if kw in bio_lower:
                topic_scores[topic] += 3  # Bio mentions are strong signals
                if topic not in bio_topics:
                    bio_topics.append(topic)

    # Calculate overall signal strength
    total_signal = sum(topic_scores.values())
    # Bonus for having a blog/substack
    if blog_links:
        total_signal += len(blog_links) * 2

    # Check if bio links to a blog
    user_url_lower = user.get("url", "").lower()
    has_blog = any(domain in user_url_lower for domain in BLOG_DOMAINS)
    if has_blog:
        total_signal += 5
        blog_links.insert(0, user["url"])

    return {
        "user": user,
        "topic_scores": topic_scores,
        "top_topics": sorted(topic_scores.keys(), key=lambda t: topic_scores[t], reverse=True)[:3],
        "relevant_tweets": relevant_tweets[:10],  # Top 10 most relevant
        "blog_links": list(set(blog_links)),
        "has_blog": has_blog or len(blog_links) > 0,
        "total_urls": len(all_urls),
        "total_signal": total_signal,
        "bio_topics": bio_topics,
    }


def batch_analyze(client: XClient, users: list[dict], max_tweets: int = 50) -> list[dict]:
    """Analyze a batch of users and return sorted by signal strength."""
    results = []
    for i, user in enumerate(users):
        print(f"  Analyzing {i+1}/{len(users)}: @{user['username']} ({user['followers']} followers)...")
        analysis = analyze_user_content(client, user, max_tweets=max_tweets)
        if analysis["total_signal"] > 0:
            results.append(analysis)

    results.sort(key=lambda r: r["total_signal"], reverse=True)
    return results
