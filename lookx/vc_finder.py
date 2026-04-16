from lookx.x_client import XClient
from lookx.vc_list import VC_FIRMS, get_search_terms

# Generic VC search queries (used in broad discovery mode)
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

# Role keywords — we want people, not firm accounts
ROLE_KEYWORDS = [
    "partner", "principal", "associate", "investor", "analyst",
    "director", "vp", "head of", "managing", "general partner",
    "venture partner", "founder", "gp", "lp",
]


def is_vc_bio(bio: str) -> bool:
    """Check if a user's bio suggests they're in VC."""
    bio_lower = bio.lower()
    return any(kw in bio_lower for kw in VC_BIO_KEYWORDS)


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

    # If bio has role keywords, likely a person
    if any(role in bio_lower for role in ROLE_KEYWORDS):
        return True

    # If name has spaces and isn't all caps, probably a person
    name = user["name"]
    if " " in name and not name.isupper() and len(name.split()) <= 4:
        return True

    # Firm accounts tend to match the firm name closely
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
) -> list[dict]:
    """Find individual people at specific VC firms on X.

    Searches tweets mentioning each firm to discover people who work there,
    then filters by bio + follower count.

    Args:
        client: XClient instance
        firms: List of firm names (defaults to VC_FIRMS)
        max_followers: Upper bound on followers
        min_followers: Lower bound (filter out empty/bot accounts)
        max_results_per_query: Results per search query

    Returns:
        List of user dicts with firm attribution
    """
    if firms is None:
        firms = VC_FIRMS

    all_users: dict[int, dict] = {}

    for firm in firms:
        search_terms = get_search_terms(firm)
        # Use the primary name for the search query
        query = f'"{firm}" -is:retweet'
        print(f"  Searching: {firm}...")

        users = client.search_users_by_bio(query, max_results=max_results_per_query)
        for user in users:
            if user["id"] not in all_users:
                # Check if this person's bio actually mentions the firm
                if bio_mentions_firm(user["bio"], firm):
                    user["firm"] = firm
                    all_users[user["id"]] = user
                # Also keep if they tweeted about it (weaker signal)
                elif user["id"] not in all_users:
                    user["firm"] = firm
                    user["firm_signal"] = "tweet_mention"
                    all_users[user["id"]] = user

    # Filter: right follower range + looks like a person (not a firm account)
    results = []
    for user in all_users.values():
        if user["followers"] < min_followers or user["followers"] > max_followers:
            continue
        if not looks_like_person(user):
            continue
        results.append(user)

    results.sort(key=lambda u: u["followers"])
    return results


def find_vcs(
    client: XClient,
    max_followers: int = 15000,
    min_followers: int = 100,
    max_results_per_query: int = 100,
) -> list[dict]:
    """Broad discovery mode — find VCs without a seed list."""
    all_users: dict[int, dict] = {}

    for query in VC_SEARCH_QUERIES:
        print(f"  Searching: {query[:50]}...")
        users = client.search_users_by_bio(query, max_results=max_results_per_query)
        for user in users:
            if user["id"] not in all_users:
                all_users[user["id"]] = user

    results = []
    for user in all_users.values():
        if not is_vc_bio(user["bio"]):
            continue
        if user["followers"] < min_followers or user["followers"] > max_followers:
            continue
        results.append(user)

    results.sort(key=lambda u: u["followers"])
    return results
