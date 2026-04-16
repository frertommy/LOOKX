from __future__ import annotations

import json
import re
import time
import urllib.request
import urllib.error
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def search_firm_people_google(firm: str, num_results: int = 30) -> list[str]:
    """Find X usernames of people at a VC firm via Google search."""
    usernames = set()
    queries = [
        f'site:x.com "{firm}" (partner OR investor OR principal OR GP OR "managing director")',
        f'site:twitter.com "{firm}" (partner OR investor OR principal OR GP)',
    ]

    for q in queries:
        try:
            encoded = urllib.parse.quote(q)
            url = f"https://www.google.com/search?q={encoded}&num={num_results}"
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode("utf-8", errors="ignore")

            # Pull x.com and twitter.com profile URLs
            matches = re.findall(r'https?://(?:www\.)?(?:x|twitter)\.com/([A-Za-z0-9_]{1,15})(?=["\s&?/])', html)
            skip = {"search", "explore", "home", "i", "intent", "hashtag", "settings",
                    "login", "signup", "tos", "privacy", "about", "jobs", "help"}
            for m in matches:
                if m.lower() not in skip and not m.startswith("_"):
                    usernames.add(m)

            time.sleep(1)  # Don't hammer Google
        except Exception:
            pass

    return list(usernames)


def fetch_profile_via_syndication(username: str) -> dict | None:
    """Try X's syndication/embed endpoint for public profile + tweets."""
    try:
        url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{username}"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        def clean(text):
            return re.sub(r'<[^>]+>', '', text).strip()

        # Try to extract tweet text
        tweets = []
        for m in re.finditer(r'dir="auto"[^>]*>(.*?)</span>', html, re.DOTALL):
            text = clean(m.group(1))
            if len(text) > 20:
                tweets.append(text)

        # Try to extract name/bio from page
        name = username
        bio = ""
        title_match = re.search(r'<title>(.*?)</title>', html)
        if title_match:
            t = clean(title_match.group(1))
            if "on Twitter" in t or "on X" in t:
                name = t.split("(")[0].strip() or t.split(" on ")[0].strip()

        if tweets or name != username:
            return {
                "username": username,
                "name": name,
                "bio": bio,
                "tweets": list(set(tweets))[:30],
            }
    except Exception:
        pass
    return None


def fetch_profile_via_nitter(username: str, instance: str = "nitter.poast.org") -> dict | None:
    """Try nitter instance for profile + tweets."""
    try:
        url = f"https://{instance}/{username}"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        def clean(text):
            return re.sub(r'<[^>]+>', '', text).strip()

        # Name
        name = username
        name_match = re.search(r'class="profile-card-fullname"[^>]*>(.*?)</a>', html, re.DOTALL)
        if name_match:
            name = clean(name_match.group(1))

        # Bio
        bio = ""
        bio_match = re.search(r'class="profile-bio"[^>]*>(.*?)</p>', html, re.DOTALL)
        if bio_match:
            bio = clean(bio_match.group(1))

        # Followers
        followers = 0
        followers_match = re.search(r'class="profile-stat-num"[^>]*>([\d,.KkMm]+)', html)
        if followers_match:
            raw = followers_match.group(1).replace(",", "")
            if "K" in raw.upper():
                followers = int(float(raw.upper().replace("K", "")) * 1000)
            elif "M" in raw.upper():
                followers = int(float(raw.upper().replace("M", "")) * 1000000)
            else:
                try:
                    followers = int(raw)
                except ValueError:
                    pass

        # Tweets
        tweets = []
        for m in re.finditer(r'class="tweet-content[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL):
            text = clean(m.group(1))
            if len(text) > 15:
                tweets.append(text)

        # Extract URLs from tweets
        urls = re.findall(r'href="(https?://[^"]+)"', html)
        urls = [u for u in urls if instance not in u and "pic.twitter" not in u]

        return {
            "username": username,
            "name": name,
            "bio": bio,
            "followers": followers,
            "tweets": tweets[:30],
            "urls": urls[:20],
        }
    except Exception:
        return None


NITTER_INSTANCES = [
    "nitter.poast.org",
    "nitter.privacydev.net",
    "nitter.woodland.cafe",
]


def fetch_profile(username: str) -> dict | None:
    """Try multiple methods to get profile data."""
    # Try nitter instances first (most data)
    for instance in NITTER_INSTANCES:
        result = fetch_profile_via_nitter(username, instance)
        if result and (result.get("bio") or result.get("tweets")):
            return result
        time.sleep(0.3)

    # Fallback to syndication
    result = fetch_profile_via_syndication(username)
    if result:
        return result

    return None


def discover_and_fetch(firm: str) -> list[dict]:
    """Full pipeline for one firm: discover usernames, fetch profiles."""
    print(f"  Searching: {firm}...")
    usernames = search_firm_people_google(firm)
    print(f"    Found {len(usernames)} X profiles")

    profiles = []
    for username in usernames:
        profile = fetch_profile(username)
        if profile:
            profile["firm"] = firm
            profiles.append(profile)
        time.sleep(0.5)

    return profiles
