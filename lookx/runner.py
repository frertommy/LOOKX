#!/usr/bin/env python3
"""LOOKX runner - no API credits needed. Uses web search + public profile scraping."""
from __future__ import annotations

import json
import time
import sys
from datetime import datetime
from pathlib import Path

from lookx.vc_list import VC_FIRMS
from lookx.content_analyzer import TOPIC_KEYWORDS, BLOG_DOMAINS


def search_google(query: str, num: int = 20) -> str:
    """Raw Google search, returns HTML."""
    import urllib.request
    import urllib.parse

    encoded = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded}&num={num}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"    Search error: {e}")
        return ""


def extract_x_usernames(html: str) -> list[str]:
    """Pull X/Twitter usernames from Google search results HTML."""
    import re
    matches = re.findall(r'https?://(?:www\.)?(?:x|twitter)\.com/([A-Za-z0-9_]{1,15})(?=["\s&?/<])', html)
    skip = {"search", "explore", "home", "i", "intent", "hashtag", "settings",
            "login", "signup", "tos", "privacy", "about", "jobs", "help", "share"}
    seen = set()
    result = []
    for m in matches:
        lower = m.lower()
        if lower not in skip and lower not in seen and not m.startswith("_"):
            seen.add(lower)
            result.append(m)
    return result


def extract_snippets(html: str) -> list[str]:
    """Extract text snippets from Google results (contains bio/tweet previews)."""
    import re
    # Google wraps snippets in various div/span patterns
    snippets = []
    # Clean approach: grab all visible text chunks
    text_blocks = re.findall(r'>([^<]{40,500})<', html)
    for block in text_blocks:
        cleaned = block.strip()
        if cleaned and not cleaned.startswith(("http", "var ", "function", "{")):
            snippets.append(cleaned)
    return snippets


def analyze_text_for_topics(texts: list[str]) -> dict:
    """Score a collection of texts against our topic keywords."""
    topic_scores = {topic: 0 for topic in TOPIC_KEYWORDS}
    relevant_snippets = []

    combined = " ".join(texts).lower()

    for topic, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            count = combined.count(kw)
            if count > 0:
                topic_scores[topic] += count

    # Find snippets that match
    for text in texts:
        text_lower = text.lower()
        matched = []
        for topic, keywords in TOPIC_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                matched.append(topic)
        if matched:
            relevant_snippets.append({"text": text[:200], "topics": matched})

    # Check for blog links
    has_blog = any(domain in combined for domain in BLOG_DOMAINS)

    total_signal = sum(topic_scores.values())
    if has_blog:
        total_signal += 5

    return {
        "topic_scores": topic_scores,
        "relevant_snippets": relevant_snippets[:5],
        "has_blog": has_blog,
        "total_signal": total_signal,
        "top_topics": sorted(topic_scores.keys(), key=lambda t: topic_scores[t], reverse=True)[:3],
    }


def score_warmth(signal: int) -> tuple[str, int]:
    if signal >= 15:
        return "HOT", 1
    elif signal >= 8:
        return "WARM", 2
    elif signal >= 3:
        return "LUKEWARM", 3
    else:
        return "COLD", 4


def approach_angle(topic: str) -> str:
    angles = {
        "prediction_markets": "Lead with prediction markets thesis - market mechanics, liquidity, platforms like Polymarket/Kalshi.",
        "sports_betting": "Lead with sports/betting - market size ($150B+), regulation tailwinds, tech infrastructure.",
        "perps_derivatives": "Lead with DeFi derivatives - on-chain trading, perpetuals, protocol design.",
        "gambling_general": "Lead with gambling/gaming - regulatory landscape, expected value, platform economics.",
        "fintech_payments": "Lead with fintech - bridge from payments to prediction markets as next frontier.",
    }
    return angles.get(topic, "Lead with general prediction markets + sports betting convergence thesis.")


def process_firm(firm: str) -> list[dict]:
    """Full pipeline for one firm: find people, analyze, score."""
    results = []

    # Search 1: Find people at this firm on X
    html1 = search_google(f'site:x.com "{firm}" (partner OR investor OR principal OR GP OR founder)')
    usernames = extract_x_usernames(html1)
    snippets1 = extract_snippets(html1)
    time.sleep(1.5)

    # Search 2: Find if anyone at this firm talks about betting/prediction markets
    html2 = search_google(f'"{firm}" ("prediction market" OR "sports betting" OR polymarket OR kalshi OR draftkings OR perps)')
    snippets2 = extract_snippets(html2)
    time.sleep(1.5)

    # Search 3: Find blog posts / articles from people at this firm about relevant topics
    html3 = search_google(f'"{firm}" (betting OR wagering OR "prediction market" OR gambling) (blog OR article OR substack OR medium)')
    snippets3 = extract_snippets(html3)
    more_usernames = extract_x_usernames(html2 + html3)
    time.sleep(1.5)

    all_usernames = list(dict.fromkeys(usernames + more_usernames))  # Dedupe, preserve order

    # Analyze the combined snippets for this firm
    all_snippets = snippets1 + snippets2 + snippets3
    firm_analysis = analyze_text_for_topics(all_snippets)

    # Build prospect entries for each person found
    for username in all_usernames[:15]:  # Cap at 15 per firm
        # Check if this specific username appears in relevant contexts
        person_texts = [s for s in all_snippets if username.lower() in s.lower()]
        if person_texts:
            person_analysis = analyze_text_for_topics(person_texts)
        else:
            person_analysis = {
                "topic_scores": {t: 0 for t in TOPIC_KEYWORDS},
                "relevant_snippets": [],
                "has_blog": False,
                "total_signal": 0,
                "top_topics": list(TOPIC_KEYWORDS.keys())[:3],
            }

        # Combine firm-level and person-level signals
        signal = person_analysis["total_signal"]
        # If the firm itself has strong signals, give person a small boost
        if firm_analysis["total_signal"] > 5:
            signal += 2

        warmth, priority = score_warmth(signal)
        best_topic = person_analysis["top_topics"][0] if person_analysis["top_topics"] else "prediction_markets"

        results.append({
            "username": username,
            "firm": firm,
            "profile_url": f"https://x.com/{username}",
            "warmth": warmth,
            "priority": priority,
            "signal_strength": signal,
            "best_topic": best_topic,
            "approach_angle": approach_angle(best_topic),
            "topic_breakdown": {k: v for k, v in person_analysis["topic_scores"].items() if v > 0},
            "relevant_snippets": person_analysis["relevant_snippets"],
            "has_blog": person_analysis["has_blog"],
            "firm_signal": firm_analysis["total_signal"],
        })

    return results


def main():
    firms = VC_FIRMS
    if len(sys.argv) > 1:
        # Allow passing specific firms as args
        firms = sys.argv[1:]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    print(f"\n{'='*60}")
    print(f"LOOKX - VC Prospect Scanner (no API credits needed)")
    print(f"{'='*60}")
    print(f"Scanning {len(firms)} firms...\n")

    all_prospects = []
    for i, firm in enumerate(firms, 1):
        print(f"[{i}/{len(firms)}] {firm}...")
        prospects = process_firm(firm)
        print(f"    Found {len(prospects)} people")
        all_prospects.extend(prospects)

    # Dedupe by username (person might appear under multiple firms)
    seen = {}
    for p in all_prospects:
        key = p["username"].lower()
        if key not in seen or p["signal_strength"] > seen[key]["signal_strength"]:
            seen[key] = p
    deduped = sorted(seen.values(), key=lambda p: (p["priority"], -p["signal_strength"]))

    # Save JSON
    json_path = str(output_dir / f"report_{timestamp}.json")
    with open(json_path, "w") as f:
        json.dump(deduped, f, indent=2)
    print(f"\nJSON saved to {json_path}")

    # Save text report
    txt_path = json_path.replace(".json", ".txt")
    with open(txt_path, "w") as f:
        f.write("=" * 80 + "\n")
        f.write("LOOKX - VC PROSPECT REPORT\n")
        f.write("=" * 80 + "\n\n")

        hot = [p for p in deduped if p["warmth"] == "HOT"]
        warm = [p for p in deduped if p["warmth"] == "WARM"]
        luke = [p for p in deduped if p["warmth"] == "LUKEWARM"]
        cold = [p for p in deduped if p["warmth"] == "COLD"]

        f.write(f"Total: {len(deduped)} | HOT: {len(hot)} | WARM: {len(warm)} | LUKEWARM: {len(luke)} | COLD: {len(cold)}\n\n")

        for i, p in enumerate(deduped, 1):
            f.write("-" * 80 + "\n")
            f.write(f"#{i} [{p['warmth']}] @{p['username']} @ {p['firm']}\n")
            f.write(f"   Profile: {p['profile_url']}\n")
            f.write(f"   Signal: {p['signal_strength']} | Best topic: {p['best_topic']}\n")
            if p["topic_breakdown"]:
                bd = ", ".join(f"{k}={v}" for k, v in p["topic_breakdown"].items())
                f.write(f"   Topics: {bd}\n")
            f.write(f"\n   APPROACH: {p['approach_angle']}\n")
            if p["relevant_snippets"]:
                f.write("   EVIDENCE:\n")
                for s in p["relevant_snippets"][:3]:
                    f.write(f"     - [{', '.join(s['topics'])}] {s['text'][:150]}\n")
            f.write("\n")

    print(f"Text report saved to {txt_path}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"Total: {len(deduped)} | HOT: {len(hot)} | WARM: {len(warm)} | LUKEWARM: {len(luke)} | COLD: {len(cold)}\n")

    for p in deduped[:20]:
        print(f"  [{p['warmth']:>8}] @{p['username']:<20} @ {p['firm']:<25} | {p['best_topic']}")
    if len(deduped) > 20:
        print(f"  ... and {len(deduped) - 20} more in report")
    print()


if __name__ == "__main__":
    main()
