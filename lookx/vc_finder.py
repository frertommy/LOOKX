from lookx.x_client import XClient

# Search queries to find VC people on X
# We search for tweets containing VC-related terms to discover users
VC_SEARCH_QUERIES = [
    '"venture capital" -is:retweet',
    '"venture partner" -is:retweet',
    '"general partner" fund -is:retweet',
    '"managing partner" venture -is:retweet',
    '"principal" venture fund -is:retweet',
    '"seed investor" -is:retweet',
    '"angel investor" -is:retweet',
    '"investment partner" -is:retweet',
]

# Keywords that should appear in a VC person's bio
VC_BIO_KEYWORDS = [
    "vc", "venture", "investor", "partner", "fund", "capital",
    "seed", "series a", "series b", "portfolio", "angel",
    "investment", "backed", "fintech", "web3", "crypto",
    "a16z", "sequoia", "paradigm", "polychain", "multicoin",
    "framework ventures", "dragonfly", "pantera",
]


def is_vc_bio(bio: str) -> bool:
    """Check if a user's bio suggests they're in VC."""
    bio_lower = bio.lower()
    return any(kw in bio_lower for kw in VC_BIO_KEYWORDS)


def find_vcs(
    client: XClient,
    max_followers: int = 15000,
    min_followers: int = 100,
    max_results_per_query: int = 100,
) -> list[dict]:
    """Find VC people on X with relatively low follower counts.

    Args:
        client: XClient instance
        max_followers: Upper bound on followers (the "under the radar" filter)
        min_followers: Lower bound (filter out empty/bot accounts)
        max_results_per_query: How many results to pull per search query

    Returns:
        List of user dicts that pass the VC + follower filters
    """
    all_users: dict[int, dict] = {}

    for query in VC_SEARCH_QUERIES:
        print(f"  Searching: {query[:50]}...")
        users = client.search_users_by_bio(query, max_results=max_results_per_query)
        for user in users:
            if user["id"] not in all_users:
                all_users[user["id"]] = user

    # Filter: must look like a VC person + have the right follower range
    results = []
    for user in all_users.values():
        if not is_vc_bio(user["bio"]):
            continue
        if user["followers"] < min_followers or user["followers"] > max_followers:
            continue
        results.append(user)

    # Sort by followers ascending (most "under the radar" first)
    results.sort(key=lambda u: u["followers"])
    return results
