"""Generate approach strategies based on content analysis."""


def generate_approach(analysis: dict) -> dict:
    """Generate a personalized outreach approach for a VC prospect.

    Takes the content analysis and produces:
    - approach_angle: best topic to lead with
    - warmth_level: cold/warm/hot based on signal strength
    - talking_points: specific things to reference
    - channel: recommended outreach channel
    - priority: 1-5 ranking
    """
    user = analysis["user"]
    topic_scores = analysis["topic_scores"]
    signal = analysis["total_signal"]

    # Determine warmth level
    if signal >= 15:
        warmth = "HOT"
        priority = 1
    elif signal >= 8:
        warmth = "WARM"
        priority = 2
    elif signal >= 3:
        warmth = "LUKEWARM"
        priority = 3
    else:
        warmth = "COLD"
        priority = 4

    # Find the best angle to lead with
    best_topic = analysis["top_topics"][0] if analysis["top_topics"] else "general"
    angle = _topic_to_angle(best_topic)

    # Build talking points from their actual content
    talking_points = []

    # Reference their tweets
    for tweet in analysis["relevant_tweets"][:3]:
        snippet = tweet["text"][:100]
        topics = ", ".join(tweet["topics"])
        talking_points.append(f"Referenced their tweet about {topics}: \"{snippet}...\"")

    # Reference their blog if they have one
    if analysis["has_blog"]:
        talking_points.append("They write long-form content - reference their articles for deeper engagement")
        for link in analysis["blog_links"][:2]:
            talking_points.append(f"  Blog/article: {link}")

    # Bio-based talking points
    if analysis["bio_topics"]:
        topics_str = ", ".join(analysis["bio_topics"])
        talking_points.append(f"Bio explicitly mentions: {topics_str}")

    # Determine channel
    if analysis["has_blog"]:
        channel = "Comment on their blog first, then DM on X"
    elif user["followers"] < 2000:
        channel = "Direct DM on X (low followers = likely reads DMs)"
    elif user["followers"] < 5000:
        channel = "Reply to their tweets first to build familiarity, then DM"
    else:
        channel = "Engage with their content publicly first, then warm DM"

    return {
        "username": user["username"],
        "name": user["name"],
        "followers": user["followers"],
        "bio": user["bio"],
        "profile_url": f"https://x.com/{user['username']}",
        "warmth": warmth,
        "priority": priority,
        "approach_angle": angle,
        "best_topic": best_topic,
        "talking_points": talking_points,
        "channel": channel,
        "signal_strength": signal,
        "has_blog": analysis["has_blog"],
        "blog_links": analysis["blog_links"],
        "topic_breakdown": {k: v for k, v in topic_scores.items() if v > 0},
    }


def _topic_to_angle(topic: str) -> str:
    angles = {
        "prediction_markets": "Lead with prediction markets thesis - they're clearly interested in this space. Talk about market mechanics, liquidity, or specific platforms.",
        "sports_betting": "Lead with sports/betting angle - discuss market size, regulation tailwinds, or tech infrastructure for betting platforms.",
        "perps_derivatives": "Lead with DeFi derivatives angle - they follow perps/derivatives. Talk about on-chain trading, liquidity mechanisms, or protocol design.",
        "gambling_general": "Lead with gambling/gaming angle - discuss regulatory landscape, expected value frameworks, or platform economics.",
        "fintech_payments": "Lead with fintech angle - bridge from payments/fintech to prediction markets as the next frontier.",
    }
    return angles.get(topic, "Lead with general thesis about prediction markets and sports betting convergence.")


def generate_report(approaches: list[dict]) -> str:
    """Generate a formatted text report of all prospects."""
    lines = []
    lines.append("=" * 80)
    lines.append("LOOKX - VC PROSPECT REPORT")
    lines.append("=" * 80)
    lines.append(f"\nTotal prospects found: {len(approaches)}")
    lines.append(f"HOT: {sum(1 for a in approaches if a['warmth'] == 'HOT')}")
    lines.append(f"WARM: {sum(1 for a in approaches if a['warmth'] == 'WARM')}")
    lines.append(f"LUKEWARM: {sum(1 for a in approaches if a['warmth'] == 'LUKEWARM')}")
    lines.append(f"COLD: {sum(1 for a in approaches if a['warmth'] == 'COLD')}")
    lines.append("")

    for i, a in enumerate(approaches, 1):
        lines.append("-" * 80)
        lines.append(f"#{i} [{a['warmth']}] @{a['username']} - {a['name']}")
        lines.append(f"   Followers: {a['followers']:,} | Signal: {a['signal_strength']}")
        lines.append(f"   Profile: {a['profile_url']}")
        lines.append(f"   Bio: {a['bio'][:120]}")
        lines.append(f"   Best topic: {a['best_topic']}")
        if a["topic_breakdown"]:
            breakdown = ", ".join(f"{k}={v}" for k, v in a["topic_breakdown"].items())
            lines.append(f"   Topic hits: {breakdown}")
        lines.append(f"\n   APPROACH: {a['approach_angle']}")
        lines.append(f"   CHANNEL: {a['channel']}")
        if a["has_blog"]:
            lines.append(f"   BLOG: Yes - {', '.join(a['blog_links'][:2])}")
        if a["talking_points"]:
            lines.append("   TALKING POINTS:")
            for tp in a["talking_points"]:
                lines.append(f"     - {tp}")
        lines.append("")

    return "\n".join(lines)
