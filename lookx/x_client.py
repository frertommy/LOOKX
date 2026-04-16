from __future__ import annotations

import tweepy
import time


class XClient:
    """Wrapper around X API v2 via tweepy."""

    def __init__(self, bearer_token: str):
        self.client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    def search_and_collect(self, query: str, max_results: int = 100) -> tuple[list[dict], dict[int, list[dict]]]:
        """Search recent tweets and return both users and their tweets.

        Returns:
            (users, tweets_by_user_id) - users list and a dict mapping user_id -> tweets
        """
        users = {}
        tweets_by_user = {}

        try:
            response = self.client.search_recent_tweets(
                query=query,
                max_results=min(max_results, 100),
                tweet_fields=["author_id", "created_at", "text", "public_metrics", "entities"],
                user_fields=["id", "name", "username", "description", "public_metrics", "url", "verified"],
                expansions=["author_id"],
            )

            # Collect users
            if response.includes and "users" in response.includes:
                for user in response.includes["users"]:
                    if user.id not in users:
                        users[user.id] = self._user_to_dict(user)

            # Collect tweets mapped to their authors
            if response.data:
                for tweet in response.data:
                    uid = tweet.author_id
                    if uid not in tweets_by_user:
                        tweets_by_user[uid] = []
                    tweets_by_user[uid].append({
                        "id": tweet.id,
                        "text": tweet.text,
                        "created_at": str(tweet.created_at) if tweet.created_at else None,
                        "metrics": dict(tweet.public_metrics) if tweet.public_metrics else {},
                        "urls": self._extract_urls(tweet),
                    })

        except tweepy.TooManyRequests:
            print("    Rate limited. Waiting 60s...")
            time.sleep(60)
        except tweepy.errors.TwitterServerError:
            print("    X API server error. Skipping...")

        return list(users.values()), tweets_by_user

    def get_user_by_username(self, username: str) -> dict | None:
        """Look up a single user by username."""
        try:
            response = self.client.get_user(
                username=username,
                user_fields=["id", "name", "username", "description", "public_metrics", "url", "verified"],
            )
            if response.data:
                return self._user_to_dict(response.data)
        except tweepy.errors.NotFound:
            return None
        except tweepy.errors.HTTPException:
            return None
        return None

    def _user_to_dict(self, user) -> dict:
        metrics = dict(user.public_metrics) if user.public_metrics else {}
        return {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "bio": user.description or "",
            "url": user.url or "",
            "verified": getattr(user, "verified", False),
            "followers": metrics.get("followers_count", 0),
            "following": metrics.get("following_count", 0),
            "tweet_count": metrics.get("tweet_count", 0),
        }

    def _extract_urls(self, tweet) -> list[str]:
        urls = []
        if tweet.entities and "urls" in tweet.entities:
            for url_entity in tweet.entities["urls"]:
                expanded = url_entity.get("expanded_url", url_entity.get("url", ""))
                if expanded:
                    urls.append(expanded)
        return urls
