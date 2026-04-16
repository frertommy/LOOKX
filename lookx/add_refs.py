#!/usr/bin/env python3
"""Find the best matching tweet/article link for each prospect's message reference."""
from __future__ import annotations

import json
import re
from pathlib import Path

# Keywords to match each prospect's reference to a specific tweet
MATCH_HINTS = {
    "eightyhi": ["prediction market", "5c", "useful", "good for the world"],
    "Nostroah": ["golf", "prediction market", "sport", "pricing"],
    "joeykrug": ["polymarket", "odds", "trading", "augur", "prediction"],
    "NTmoney": ["sport", "prediction", "100x", "vegas", "polymarket"],
    "arjunblj": ["multi-agent", "gambling", "hypergambling", "prediction"],
    "guywuolletjr": ["vending machine", "perps", "prediction market", "killer"],
    "veradittakit": ["novig", "sport", "prediction", "reshap", "dad"],
    "fawzitani": ["consumer", "financial product", "gaming", "entertainment"],
    "RealOmeedMalik": ["polymarket", "free expression", "financial innovation"],
    "prayanks": ["pred", "sport", "exchange", "transparent"],
    "danrobinson": ["pm-amm", "amm", "prediction", "distribution market"],
    "shayonsengupta": ["exchange", "superior", "sports betting", "mechanism"],
    "_Dave__White_": ["perpetual", "power", "distribution", "derivative"],
    "HadickM": ["derivative", "smartest", "crypto derivative", "cftc"],
    "tomhschmidt": ["polymarket", "election", "global", "$1.7b", "hungarian"],
    "mickymalka": ["token", "everything", "ribbit", "5c"],
    "GigiLevy": ["888", "gambling", "gaming", "playtika"],
    "mhiggins": ["action network", "sport", "betting", "invest"],
    "cegapereira": ["prediction market", "integrity", "insider", "polymarket"],
    "tomloverro": ["kalshi", "everything exchange", "event"],
    "ahall_research": ["prediction market", "ai judge", "scale", "crypto"],
    "waynekimmel": ["sport", "#sportstechvc", "asset class"],
    "kagisobond": ["real money", "gaming", "sport"],
    "zxocw": ["doomscroll", "fund manager", "information market"],
    "thechrisbuskirk": ["polymarket", "1789", "capital"],
    "FranklinBi": ["chaos", "leveraged", "prediction", "streaker", "super bowl"],
    "0xMasonH": ["megapot", "fomo3d", "invested", "patrick"],
    "_kinjalbshah": ["polymarket", "blockchain capital"],
    "im_manderson": ["synthetix", "hashletes", "nfl", "decentralized"],
    "GuptaRK22": ["sport", "basketball", "glue guys", "nba"],
    "PeteVlastelica": ["esport", "activision", "draftkings", "gaming"],
    "deepenparikh": ["ravens", "sport", "gaming", "kelvin"],
    "chadstender": ["sport", "web3", "media"],
    "santiagoroel": ["polymarket", "nft", "defi"],
    "EvgenyGaevoy": ["market mak", "liquidity", "wintermute"],
    "ColeVanNice1": ["dodger", "draftkings", "sport"],
    "vasu": ["nba", "draft lottery", "basketball", "courtside"],
    "mattyryze": ["solana", "crypto", "ai", "digital asset"],
}

# Some references are to articles/blogs, not tweets
ARTICLE_REFS = {
    "eightyhi": "https://fiftycentdollars.substack.com/",
    "_alekslarsen": "https://medium.com/@alekslarsen",
    "veradittakit": "https://veradiverdict.com",
    "tomloverro": "https://tomloverro.com",
    "ahall_research": None,  # a16z research — find via tweets
    "waynekimmel": None,
    "GigiLevy": None,
}


def find_best_tweet(username: str, tweets: list[dict], hints: list[str]) -> dict | None:
    """Find the tweet that best matches the reference hints."""
    if not tweets:
        return None

    best = None
    best_score = 0

    for tweet in tweets:
        text_lower = tweet["text"].lower()
        score = sum(1 for h in hints if h.lower() in text_lower)
        # Boost tweets with more engagement
        likes = tweet.get("metrics", {}).get("like_count", 0)
        if likes > 10:
            score += 1
        if score > best_score:
            best_score = score
            best = tweet

    return best if best_score > 0 else None


def main():
    tweets_data = json.loads(Path("output/tweets.json").read_text())
    outreach = json.loads(Path("output/outreach.json").read_text())

    for prospect in outreach:
        username = prospect["username"]
        user_tweets = tweets_data.get(username, {}).get("tweets", [])
        hints = MATCH_HINTS.get(username, [])

        # Try to find a matching tweet
        best_tweet = find_best_tweet(username, user_tweets, hints)

        if best_tweet and best_tweet.get("id"):
            tweet_url = f"https://x.com/{username}/status/{best_tweet['id']}"
            prospect["ref_url"] = tweet_url
            prospect["ref_type"] = "tweet"
            prospect["ref_text"] = best_tweet["text"][:200]
        elif username in ARTICLE_REFS and ARTICLE_REFS[username]:
            prospect["ref_url"] = ARTICLE_REFS[username]
            prospect["ref_type"] = "article"
            prospect["ref_text"] = prospect.get("tweet_ref", "")
        else:
            # Fallback: link to their profile
            prospect["ref_url"] = prospect["profile_url"]
            prospect["ref_type"] = "profile"
            prospect["ref_text"] = prospect.get("tweet_ref", "")

    # Sort by followers ascending (lowest first)
    outreach.sort(key=lambda p: p.get("followers", 0) or 999999)

    Path("output/outreach.json").write_text(json.dumps(outreach, indent=2))

    # Print summary
    tweet_refs = sum(1 for p in outreach if p.get("ref_type") == "tweet")
    article_refs = sum(1 for p in outreach if p.get("ref_type") == "article")
    profile_refs = sum(1 for p in outreach if p.get("ref_type") == "profile")
    print(f"Updated {len(outreach)} prospects with reference links")
    print(f"  Tweet links: {tweet_refs}")
    print(f"  Article links: {article_refs}")
    print(f"  Profile fallbacks: {profile_refs}")
    print(f"Sorted by followers (lowest first)")


if __name__ == "__main__":
    main()
