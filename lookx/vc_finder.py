from __future__ import annotations

from lookx.x_client import XClient
from lookx.vc_list import VC_FIRMS, get_search_terms

# Role keywords — we want people, not firm accounts
ROLE_KEYWORDS = [
    "partner", "principal", "associate", "investor", "analyst",
    "director", "vp", "head of", "managing", "general partner",
    "venture partner", "founder", "gp", "lp",
]


def bio_mentions_firm(bio: str, firm: str) -> bool:
    """Check if a user's bio mentions a specific firm."""
    bio_lower = bio.lower()
    for term in get_search_terms(firm):
        if term in bio_lower:
            return True
    return False


def looks_like_person(user: dict) -> bool:
    """Heuristic: is this a person account vs a firm/brand account."""
    bio_lower = user["bio"].lower()
    username_lower = user["username"].lower()

    if any(role in bio_lower for role in ROLE_KEYWORDS):
        return True

    name = user["name"]
    if " " in name and not name.isupper() and len(name.split()) <= 4:
        return True

    for firm in VC_FIRMS:
        firm_lower = firm.lower().replace(" ", "")
        if username_lower.replace("_", "") == firm_lower:
            return False

    return True


def find_vcs_by_firm(
    client: XClient,
    firms: list[str] | None = None,
    max_followers: int = 50000,
    min_followers: int = 50,
    max_results_per_query: int = 100,
) -> tuple[list[dict], dict[int, list[dict]]]:
    """Find individual people at specific VC firms on X.

    Returns:
        (users, all_tweets) - filtered user list and all tweets collected during search
    """
    if firms is None:
        firms = VC_FIRMS

    all_users: dict[int, dict] = {}
    all_tweets: dict[int, list[dict]] = {}

    for firm in firms:
        query = f'"{firm}" -is:retweet'
        print(f"  Searching: {firm}...")

        users, tweets_by_user = client.search_and_collect(query, max_results=max_results_per_query)

        # Merge tweets
        for uid, tweets in tweets_by_user.items():
            if uid not in all_tweets:
                all_tweets[uid] = []
            all_tweets[uid].extend(tweets)

        for user in users:
            if user["id"] not in all_users:
                if bio_mentions_firm(user["bio"], firm):
                    user["firm"] = firm
                    all_users[user["id"]] = user
                else:
                    user["firm"] = firm
                    user["firm_signal"] = "tweet_mention"
                    all_users[user["id"]] = user

    # Filter: right follower range + looks like a person
    results = []
    for user in all_users.values():
        if user["followers"] < min_followers or user["followers"] > max_followers:
            continue
        if not looks_like_person(user):
            continue
        results.append(user)

    results.sort(key=lambda u: u["followers"])
    return results, all_tweets
