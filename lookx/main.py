#!/usr/bin/env python3
"""LOOKX - Find under-the-radar VCs interested in prediction markets & sports betting."""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from lookx.x_client import XClient
from lookx.vc_finder import find_vcs, find_vcs_by_firm
from lookx.vc_list import VC_FIRMS
from lookx.content_analyzer import batch_analyze
from lookx.approach_gen import generate_approach, generate_report


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="LOOKX - VC prospecting via X")
    parser.add_argument("--mode", choices=["firms", "broad"], default="firms",
                        help="'firms' = search by VC firm list (default), 'broad' = discover VCs broadly")
    parser.add_argument("--max-followers", type=int, default=50000,
                        help="Max follower count (default: 50000)")
    parser.add_argument("--min-followers", type=int, default=50,
                        help="Min follower count (default: 50)")
    parser.add_argument("--max-tweets", type=int, default=50,
                        help="Max tweets to analyze per user (default: 50)")
    parser.add_argument("--firms", type=str, nargs="*", default=None,
                        help="Specific firms to search (default: full list)")
    parser.add_argument("--output", type=str, default=None,
                        help="Output file path (default: output/report_<timestamp>.json)")
    parser.add_argument("--text-report", action="store_true",
                        help="Also generate a text report")
    args = parser.parse_args()

    bearer_token = os.getenv("X_BEARER_TOKEN")
    if not bearer_token:
        print("Error: X_BEARER_TOKEN not set. Copy .env.example to .env and add your token.")
        sys.exit(1)

    client = XClient(bearer_token)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Step 1: Find VCs
    if args.mode == "firms":
        firms = args.firms if args.firms else VC_FIRMS
        print(f"\n[1/3] Searching for people at {len(firms)} VC firms on X...")
        vcs = find_vcs_by_firm(
            client,
            firms=firms,
            max_followers=args.max_followers,
            min_followers=args.min_followers,
        )
    else:
        print("\n[1/3] Broad discovery — searching for VCs on X...")
        vcs = find_vcs(
            client,
            max_followers=args.max_followers,
            min_followers=args.min_followers,
        )

    print(f"  Found {len(vcs)} prospects with {args.min_followers}-{args.max_followers:,} followers\n")

    if not vcs:
        print("No prospects found. Try adjusting --max-followers or --min-followers.")
        sys.exit(0)

    # Step 2: Analyze content
    print("[2/3] Analyzing content for betting/sports/prediction market signals...")
    analyses = batch_analyze(client, vcs, max_tweets=args.max_tweets)
    print(f"  {len(analyses)} prospects have relevant signals\n")

    # Step 3: Generate approaches (even for zero-signal users, include them as COLD)
    print("[3/3] Generating approach strategies...")
    # Include all users, not just signal matches — cold outreach is still useful
    all_analyses = analyses
    # Add zero-signal users back as cold leads
    analyzed_ids = {a["user"]["id"] for a in analyses}
    for user in vcs:
        if user["id"] not in analyzed_ids:
            all_analyses.append({
                "user": user,
                "topic_scores": {t: 0 for t in ["prediction_markets", "sports_betting", "perps_derivatives", "gambling_general", "fintech_payments"]},
                "top_topics": [],
                "relevant_tweets": [],
                "blog_links": [],
                "has_blog": False,
                "total_urls": 0,
                "total_signal": 0,
                "bio_topics": [],
            })

    approaches = [generate_approach(a) for a in all_analyses]
    approaches.sort(key=lambda a: (a["priority"], -a["signal_strength"]))

    # Save JSON output
    output_path = args.output or str(output_dir / f"report_{timestamp}.json")
    with open(output_path, "w") as f:
        json.dump(approaches, f, indent=2, default=str)
    print(f"\n  JSON report saved to {output_path}")

    # Save text report (always generate it)
    text_path = output_path.replace(".json", ".txt")
    report = generate_report(approaches)
    with open(text_path, "w") as f:
        f.write(report)
    print(f"  Text report saved to {text_path}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"LOOKX RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Total prospects: {len(approaches)}")
    hot = [a for a in approaches if a["warmth"] == "HOT"]
    warm = [a for a in approaches if a["warmth"] == "WARM"]
    luke = [a for a in approaches if a["warmth"] == "LUKEWARM"]
    cold = [a for a in approaches if a["warmth"] == "COLD"]
    print(f"  HOT: {len(hot)} | WARM: {len(warm)} | LUKEWARM: {len(luke)} | COLD: {len(cold)}")
    print()

    for a in approaches[:15]:
        firm_tag = f" @ {a['firm']}" if a.get("firm") and a["firm"] != "Unknown" else ""
        print(f"  [{a['warmth']:>8}] @{a['username']:<20} {a['followers']:>6,} followers{firm_tag} | {a['best_topic']}")
    if len(approaches) > 15:
        print(f"  ... and {len(approaches) - 15} more (see full report)")
    print()


if __name__ == "__main__":
    main()
