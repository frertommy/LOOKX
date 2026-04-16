#!/usr/bin/env python3
"""Fetch tweets for NEW prospects only (30 tweets each to control cost)."""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
import tweepy


def main():
    load_dotenv()
    token = os.getenv("X_BEARER_TOKEN")
    if not token:
        print("Error: X_BEARER_TOKEN not set")
        sys.exit(1)

    client = tweepy.Client(bearer_token=token, wait_on_rate_limit=True)

    # Load new prospects
    new_prospects = json.loads(Path("output/new_prospects.json").read_text())
    usernames = [p["username"] for p in new_prospects]

    # Load existing tweets data and merge
    out_path = Path("output/tweets.json")
    if out_path.exists():
        data = json.loads(out_path.read_text())
    else:
        data = {}

    total_tweets_read = 0
    total_cost = 0.0
    MAX_TWEETS = 30  # Limit per user for cost control

    for i, username in enumerate(usernames):
        existing = data.get(username, {})
        existing_tweets = existing.get("tweets", [])
        if existing_tweets and "id" in existing_tweets[0]:
            print(f"  [{i+1}/{len(usernames)}] @{username} — already fetched, skipping")
            continue

        print(f"  [{i+1}/{len(usernames)}] @{username}...", end=" ", flush=True)

        try:
            user_resp = client.get_user(
                username=username,
                user_fields=["id", "name", "username", "description", "public_metrics", "url"],
            )
            if not user_resp.data:
                print("NOT FOUND")
                data[username] = {"error": "user not found", "tweets": []}
                _save(out_path, data)
                continue
            total_cost += 0.01

            user = user_resp.data
            metrics = dict(user.public_metrics) if user.public_metrics else {}

            tweets_resp = client.get_users_tweets(
                id=user.id,
                max_results=MAX_TWEETS,
                tweet_fields=["created_at", "text", "public_metrics", "entities"],
                exclude=["retweets"],
            )

            tweets = []
            if tweets_resp.data:
                for t in tweets_resp.data:
                    urls = []
                    if t.entities and "urls" in t.entities:
                        for u in t.entities["urls"]:
                            urls.append(u.get("expanded_url", u.get("url", "")))
                    tweets.append({
                        "id": str(t.id),
                        "text": t.text,
                        "date": str(t.created_at) if t.created_at else None,
                        "metrics": dict(t.public_metrics) if t.public_metrics else {},
                        "urls": urls,
                    })
                total_tweets_read += len(tweets)
                total_cost += len(tweets) * 0.005

            data[username] = {
                "name": user.name,
                "username": user.username,
                "bio": user.description or "",
                "url": user.url or "",
                "followers": metrics.get("followers_count", 0),
                "following": metrics.get("following_count", 0),
                "tweet_count": metrics.get("tweet_count", 0),
                "tweets": tweets,
            }

            print(f"{len(tweets)} tweets, {metrics.get('followers_count', 0):,} followers (running cost: ${total_cost:.2f})")
            _save(out_path, data)

        except tweepy.errors.NotFound:
            print("NOT FOUND")
            data[username] = {"error": "user not found", "tweets": []}
            _save(out_path, data)
        except tweepy.errors.Unauthorized:
            print("SUSPENDED/PROTECTED")
            data[username] = {"error": "unauthorized", "tweets": []}
            _save(out_path, data)
        except tweepy.errors.HTTPException as e:
            print(f"API ERROR: {e}")
            _save(out_path, data)
            if "402" in str(e):
                print(f"\n  OUT OF CREDITS after {total_tweets_read} tweets (${total_cost:.2f})")
                sys.exit(1)

        time.sleep(0.5)

    print(f"\nDone! {total_tweets_read} tweets for new prospects")
    print(f"Estimated cost: ${total_cost:.2f}")


def _save(path: Path, data: dict):
    path.write_text(json.dumps(data, indent=2, default=str))


if __name__ == "__main__":
    main()
