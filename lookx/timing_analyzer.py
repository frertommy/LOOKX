#!/usr/bin/env python3
"""Analyze each prospect's tweet timing to find optimal DM windows."""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path


DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def analyze_timing(tweets: list[dict]) -> dict:
    """Find the best days and hours to DM this person based on tweet activity."""
    if not tweets:
        return {
            "best_day": None,
            "best_hour_utc": None,
            "best_hour_et": None,
            "activity_by_hour": {},
            "activity_by_day": {},
            "total_analyzed": 0,
        }

    hours_utc = defaultdict(int)
    days = defaultdict(int)
    day_hour = defaultdict(int)

    for t in tweets:
        date_str = t.get("date")
        if not date_str:
            continue
        try:
            dt = datetime.fromisoformat(date_str.replace("+00:00", "+00:00"))
            hour = dt.hour
            day = dt.strftime("%A")
            hours_utc[hour] += 1
            days[day] += 1
            day_hour[f"{day}_{hour}"] += 1
        except (ValueError, AttributeError):
            continue

    if not hours_utc:
        return {
            "best_day": None,
            "best_hour_utc": None,
            "best_hour_et": None,
            "activity_by_hour": {},
            "activity_by_day": {},
            "total_analyzed": 0,
        }

    best_hour = max(hours_utc, key=hours_utc.get)
    best_day = max(days, key=days.get)
    best_day_hour_key = max(day_hour, key=day_hour.get)
    best_day_name, best_day_hour = best_day_hour_key.split("_")
    best_day_hour = int(best_day_hour)

    # Convert to ET (UTC-4, assuming EDT)
    best_hour_et = (best_hour - 4) % 24
    best_day_hour_et = (best_day_hour - 4) % 24

    return {
        "best_day": best_day,
        "best_hour_utc": best_hour,
        "best_hour_et": best_hour_et,
        "best_combo_day": best_day_name,
        "best_combo_hour_utc": best_day_hour,
        "best_combo_hour_et": best_day_hour_et,
        "best_combo_count": day_hour[best_day_hour_key],
        "total_analyzed": len(tweets),
    }


def format_time(hour: int) -> str:
    """Convert 24h hour to readable 12h format."""
    if hour == 0:
        return "12AM"
    elif hour < 12:
        return f"{hour}AM"
    elif hour == 12:
        return "12PM"
    else:
        return f"{hour - 12}PM"


def main():
    tweets_data = json.loads(Path("output/tweets.json").read_text())
    outreach = json.loads(Path("output/outreach.json").read_text())

    for prospect in outreach:
        username = prospect["username"]
        tweets = tweets_data.get(username, {}).get("tweets", [])
        timing = analyze_timing(tweets)

        if timing["best_day"]:
            day = timing.get("best_combo_day", timing["best_day"])
            hour_et = timing.get("best_combo_hour_et", timing["best_hour_et"])
            hour_utc = timing.get("best_combo_hour_utc", timing["best_hour_utc"])
            prospect["best_time"] = f"{day} {format_time(hour_et)} ET"
            prospect["best_time_utc"] = f"{day} {format_time(hour_utc)} UTC"
            prospect["timing_sample"] = timing["total_analyzed"]
        else:
            prospect["best_time"] = None
            prospect["best_time_utc"] = None
            prospect["timing_sample"] = 0

    Path("output/outreach.json").write_text(json.dumps(outreach, indent=2))

    with_timing = sum(1 for p in outreach if p.get("best_time"))
    print(f"Added timing data to {with_timing}/{len(outreach)} prospects")

    # Print samples
    for p in outreach[:5]:
        print(f"  @{p['username']}: {p.get('best_time', 'N/A')} (from {p.get('timing_sample', 0)} tweets)")


if __name__ == "__main__":
    main()
