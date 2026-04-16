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
from lookx.vc_finder import find_vcs
from lookx.content_analyzer import batch_analyze
from lookx.approach_gen import generate_approach, generate_report


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="LOOKX - VC prospecting via X")
    parser.add_argument("--max-followers", type=int, default=15000, help="Max follower count (default: 15000)")
    parser.add_argument("--min-followers", type=int, default=100, help="Min follower count (default: 100)")
    parser.add_argument("--max-tweets", type=int, default=50, help="Max tweets to analyze per user (default: 50)")
    parser.add_argument("--output", type=str, default=None, help="Output file path (default: output/report_<timestamp>.json)")
    parser.add_argument("--text-report", action="store_true", help="Also generate a text report")
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
    print("\n[1/3] Searching for under-the-radar VCs on X...")
    vcs = find_vcs(
        client,
        max_followers=args.max_followers,
        min_followers=args.min_followers,
    )
    print(f"  Found {len(vcs)} VC prospects with {args.min_followers}-{args.max_followers} followers\n")

    if not vcs:
        print("No prospects found. Try adjusting --max-followers or --min-followers.")
        sys.exit(0)

    # Step 2: Analyze content
    print("[2/3] Analyzing content for betting/sports/prediction market signals...")
    analyses = batch_analyze(client, vcs, max_tweets=args.max_tweets)
    print(f"  {len(analyses)} prospects have relevant signals\n")

    if not analyses:
        print("No prospects with relevant signals found.")
        sys.exit(0)

    # Step 3: Generate approaches
    print("[3/3] Generating approach strategies...")
    approaches = [generate_approach(a) for a in analyses]
    approaches.sort(key=lambda a: (a["priority"], -a["signal_strength"]))

    # Save JSON output
    output_path = args.output or str(output_dir / f"report_{timestamp}.json")
    with open(output_path, "w") as f:
        json.dump(approaches, f, indent=2, default=str)
    print(f"\n  JSON report saved to {output_path}")

    # Save text report if requested
    if args.text_report:
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
    for a in approaches[:10]:
        print(f"  [{a['warmth']:>8}] @{a['username']:<20} {a['followers']:>6,} followers | {a['best_topic']}")
    if len(approaches) > 10:
        print(f"  ... and {len(approaches) - 10} more (see full report)")
    print()


if __name__ == "__main__":
    main()
