import tweepy
import time


class XClient:
    """Wrapper around X API v2 via tweepy."""

    def __init__(self, bearer_token: str):
        self.client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    def search_users_by_bio(self, query: str, max_results: int = 100) -> list[dict]:
        """Search recent tweets to discover users matching a bio/profile query.

        X API v2 doesn't have a direct user search by bio endpoint,
        so we search tweets from users whose profiles match VC keywords,
        then deduplicate by user.
        """
        users = {}
        try:
            # Search tweets authored by people with VC-related bios
            # We use -is:retweet to get original content
            response = self.client.search_recent_tweets(
                query=query,
                max_results=min(max_results, 100),
                tweet_fields=["author_id", "created_at", "text"],
                user_fields=["id", "name", "username", "description", "public_metrics", "url", "verified"],
                expansions=["author_id"],
            )

            if response.includes and "users" in response.includes:
                for user in response.includes["users"]:
                    if user.id not in users:
                        users[user.id] = self._user_to_dict(user)

        except tweepy.TooManyRequests:
            print("Rate limited. Waiting...")
            time.sleep(60)
        except tweepy.errors.TwitterServerError:
            print("X API server error. Retrying...")
            time.sleep(5)

        return list(users.values())

    def get_user_tweets(self, user_id: int, max_results: int = 50) -> list[dict]:
        """Get recent tweets from a specific user."""
        tweets = []
        try:
            response = self.client.get_users_tweets(
                id=user_id,
                max_results=min(max_results, 100),
                tweet_fields=["created_at", "text", "public_metrics", "entities"],
                exclude=["retweets"],
            )
            if response.data:
                for tweet in response.data:
                    tweets.append({
                        "id": tweet.id,
                        "text": tweet.text,
                        "created_at": str(tweet.created_at) if tweet.created_at else None,
                        "metrics": dict(tweet.public_metrics) if tweet.public_metrics else {},
                        "urls": self._extract_urls(tweet),
                    })
        except tweepy.TooManyRequests:
            print(f"Rate limited fetching tweets for user {user_id}. Waiting...")
            time.sleep(60)
        except tweepy.errors.TwitterServerError:
            pass

        return tweets

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
        return None

    def get_users_by_ids(self, user_ids: list[int]) -> list[dict]:
        """Look up multiple users by ID."""
        users = []
        # API allows 100 users per request
        for i in range(0, len(user_ids), 100):
            batch = user_ids[i : i + 100]
            try:
                response = self.client.get_users(
                    ids=batch,
                    user_fields=["id", "name", "username", "description", "public_metrics", "url", "verified"],
                )
                if response.data:
                    users.extend(self._user_to_dict(u) for u in response.data)
            except tweepy.TooManyRequests:
                time.sleep(60)
        return users

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
