#!/usr/bin/env python3
"""Generate personalized DM messages for each prospect based on their tweets + Notch pitch."""
from __future__ import annotations

import json
from pathlib import Path

DECK_URL = "https://frertommy.github.io/DEck/"

# Hand-crafted messages based on real tweet content + research evidence
MESSAGES = {
    "eightyhi": {
        "tweet_ref": "Bio says prediction markets can be useful and good for the world + runs 5c(c) Capital",
        "message": (
            "Hey Adhi — big fan of the 50 Cent Dollars writing. You and Noah are building the thesis we're executing on: "
            "we built Notch, the first perpetual derivatives for sports teams. Instead of expiring event contracts, "
            "users go long/short team strength continuously across entire seasons. Oracle live for 96 soccer teams + NBA/MLB, "
            f"DEX on Solana. Raising seed. Would love 15 min. {DECK_URL}"
        ),
    },
    "Nostroah": {
        "tweet_ref": "Tweeted 'Golf is the perfect sport for prediction market trading' — sports prediction market thesis",
        "message": (
            "Hey Noah — your tweet about golf being perfect for prediction market trading hit home. "
            "We're building exactly that thesis but as perpetuals: Notch lets you hold continuous positions on team strength "
            "instead of expiring bets. Live oracle for 96 soccer teams + NBA/MLB, Solana DEX with 13 markets. "
            f"Your Kalshi ops background is exactly the perspective we'd value. {DECK_URL}"
        ),
    },
    "joeykrug": {
        "tweet_ref": "Said he uses Polymarket odds to inform trading decisions on policy/geopolitical events",
        "message": (
            "Hey Joey — saw you mention using Polymarket odds to inform trading decisions. "
            "We're taking that a step further with Notch: perpetual derivatives on sports team strength. "
            "No expiry, continuous positions, leverage — basically what Augur would be if it were perps instead of event contracts. "
            f"Oracle live, Solana DEX with 13 markets, raising seed. {DECK_URL}"
        ),
    },
    "NTmoney": {
        "tweet_ref": "Previously said Polymarket sports odds are 'insanely better than Vegas' and the market is 100x undervalued",
        "message": (
            "Hey Nick — you said sports prediction markets need to be 100x bigger. We agree and we're building the infrastructure for it: "
            "Notch creates perpetual derivatives on team strength indices. No expiring bets, continuous positions that compound through seasons. "
            f"Oracle live for 96 soccer teams + full NBA/MLB. Solana DEX. Raising seed. {DECK_URL}"
        ),
    },
    "arjunblj": {
        "tweet_ref": "Tweeted 'any sufficiently advanced multi-agent workflow is indistinguishable from hypergambling'",
        "message": (
            "Hey Arjun — loved the 'advanced multi-agent workflow indistinguishable from hypergambling' take. "
            "We're building what sits between those worlds: Notch, perpetual derivatives on sports teams. "
            "Continuous long/short positions on team strength, no expiry. Heard you're building a prediction markets terminal at Paradigm — "
            f"we'd be a natural new asset class for it. {DECK_URL}"
        ),
    },
    "_alekslarsen": {
        "tweet_ref": "Led $55M Polymarket round, wrote 'Put Your Money Where Your Mouth Is'",
        "message": (
            "Hey Aleks — your piece on Polymarket becoming part of modern media and financial markets really resonated. "
            "We're building the next surface area for that thesis: Notch creates perpetual derivatives on team strength. "
            "Instead of binary event contracts, users hold continuous positions across seasons. "
            f"Oracle live, Solana DEX, raising seed. {DECK_URL}"
        ),
    },
    "guywuolletjr": {
        "tweet_ref": "Tweeted 'Is the vending machine the next killer product structure after perps and prediction markets?'",
        "message": (
            "Hey Guy — your tweet asking if vending machines are the next killer structure after perps and prediction markets made me laugh. "
            "We're fusing those two: Notch is perpetual derivatives for sports teams. Continuous long/short on team strength indices, "
            f"not expiring contracts. Solana DEX live, oracle covering 96 soccer teams + NBA/MLB. Raising seed. {DECK_URL}"
        ),
    },
    "veradittakit": {
        "tweet_ref": "Led Novig Series B, tweeted about prediction markets reshaping sports betting + his dad making him read sports section",
        "message": (
            "Hey Paul — loved the Novig announcement and the story about your dad making you read the sports section. "
            "We're building the next layer: Notch creates perpetual derivatives on team strength. Instead of expiring bets, "
            "fans hold continuous positions that compound through transfers, injuries, entire seasons. "
            f"Oracle live for 96 soccer + NBA/MLB. Solana DEX. Raising seed. {DECK_URL}"
        ),
    },
    "fawzitani": {
        "tweet_ref": "Led Forerunner's Novig investment, said consumers spend attention with financial products",
        "message": (
            "Hey Fawzi — your take on consumers spending attention with financial products is exactly our thesis. "
            "We built Notch: perpetual derivatives on sports team strength. Not one-off bets — continuous positions "
            "that compound across seasons. Live oracle, Solana DEX, 13 markets. "
            f"Raising seed — would love to chat. {DECK_URL}"
        ),
    },
    "RealOmeedMalik": {
        "tweet_ref": "Invested tens of millions in Polymarket, called it intersection of free expression and financial innovation",
        "message": (
            "Hey Omeed — 1789's Polymarket bet was bold and right. We're extending that thesis to sports: "
            "Notch is perpetual derivatives on team strength. Continuous positions, no expiry, leverage — "
            "things prediction markets can't do yet. Live oracle for 96 soccer teams + NBA/MLB, Solana DEX. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "prayanks": {
        "tweet_ref": "Led Accel's seed in Pred (sports prediction exchange on Base)",
        "message": (
            "Hey Prayank — saw the Pred investment, you clearly get on-chain sports trading. "
            "We built Notch, which takes that further: perpetual derivatives on team strength indices. "
            "Users go long/short continuously, positions compound through seasons. Live oracle, Solana DEX. "
            f"Different angle than event contracts — would love to show you. {DECK_URL}"
        ),
    },
    "danrobinson": {
        "tweet_ref": "Co-authored pm-AMM paper for prediction markets + Distribution Markets research",
        "message": (
            "Hey Dan — your pm-AMM paper is one of the best pieces of mechanism design work in prediction markets. "
            "We're building in that design space but for perpetuals: Notch creates continuous derivatives on sports team strength. "
            "Our oracle reprices from bookmaker odds, match results, and transfer news. "
            f"Would love your technical take. {DECK_URL}"
        ),
    },
    "shayonsengupta": {
        "tweet_ref": "Said 'an exchange is a strictly superior market mechanism for sports betting'",
        "message": (
            "Hey Shayon — your take that an exchange is strictly superior to sportsbooks is our founding thesis. "
            "Notch builds perpetual derivatives on team strength — continuous positions, no expiry, leverage. "
            "We're basically building the exchange-native sports product you described. "
            f"Oracle live, Solana DEX. Raising seed. {DECK_URL}"
        ),
    },
    "_Dave__White_": {
        "tweet_ref": "Created floor perpetuals, power perpetuals, co-authored Distribution Markets paper",
        "message": (
            "Hey Dave — your work on power perpetuals and distribution markets is genuinely pioneering. "
            "We're applying perpetual structures to sports: Notch creates continuous derivatives on team strength indices. "
            "Funding rate, leverage, no expiry — perps for a new asset class. "
            f"Would really value your perspective on the mechanism design. {DECK_URL}"
        ),
    },
    "HadickM": {
        "tweet_ref": "Tweeted 'Josh is the single smartest person in crypto derivatives' — deep derivatives conviction",
        "message": (
            "Hey Rob — between your CFTC advisory role and backing of Polymarket and Megapot, you get both the regulatory "
            "and product side of prediction markets. We built Notch: perpetual derivatives on sports team strength. "
            "Framed as continuous index derivatives (like equity indices) to navigate regs. "
            f"Oracle live, Solana DEX. Raising seed. {DECK_URL}"
        ),
    },
    "tomhschmidt": {
        "tweet_ref": "Tweeted about Polymarket election markets outside the US growing to $1.7B volume",
        "message": (
            "Hey Tom — your point about Polymarket's $1.7B in global election markets is massive. "
            "Sports is the next frontier: we built Notch, perpetual derivatives on team strength covering 96 soccer teams globally + NBA/MLB. "
            "Continuous positions, not expiring contracts. "
            f"Solana DEX live. Raising seed. {DECK_URL}"
        ),
    },
    "mickymalka": {
        "tweet_ref": "Backed 5c(c) Capital prediction markets fund, Ribbit thesis on tokenizing everything",
        "message": (
            "Hey Micky — you backed 5c(c) Capital's prediction markets thesis, and your 'Everything is a token' conviction "
            "maps directly to what we're building. Notch creates perpetual derivatives on sports team strength — "
            "tokenized continuous positions on Solana. "
            f"Oracle live for 96 soccer teams + NBA/MLB. Raising seed. {DECK_URL}"
        ),
    },
    "GigiLevy": {
        "tweet_ref": "Former CEO of 888 Holdings (online gambling), founded Playtika, NFX invested in Novig",
        "message": (
            "Hey Gigi — you ran 888 Holdings and know sports gambling infrastructure better than anyone in VC. "
            "We built Notch: perpetual derivatives on team strength. Instead of expiring match bets, users hold "
            "continuous positions with leverage. Think what perps did to spot crypto, applied to sports. "
            f"Oracle live, Solana DEX. {DECK_URL}"
        ),
    },
    "mhiggins": {
        "tweet_ref": "Invested $17.5M in Action Network (sports betting media/analytics)",
        "message": (
            "Hey Matt — your Action Network investment showed conviction in sports betting infrastructure. "
            "We're building the trading layer: Notch creates perpetual derivatives on team strength. "
            "Continuous positions that compound through seasons, not one-off bets. "
            f"Live oracle, Solana DEX. Raising seed — would love to chat. {DECK_URL}"
        ),
    },
    "cegapereira": {
        "tweet_ref": "Commented on prediction market integrity/insider trading risks at Polymarket",
        "message": (
            "Hey Carlos — your takes on prediction market integrity are important. "
            "We're building with that in mind: Notch creates perpetual derivatives on sports teams with pricing "
            "from our own oracle (96 soccer teams + NBA/MLB). Transparent on-chain settlement on Solana. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "tomloverro": {
        "tweet_ref": "IVP published 'Kalshi: The Everything Exchange', Board at Coinbase",
        "message": (
            "Hey Tom — IVP's 'Kalshi: The Everything Exchange' thesis is exactly our starting point. "
            "Notch extends it: perpetual derivatives on sports team strength. Not event contracts that expire — "
            "continuous positions with leverage. Live oracle, Solana DEX with 13 markets. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "ahall_research": {
        "tweet_ref": "Published a16z's prediction markets research, 'How AI judges can scale prediction markets'",
        "message": (
            "Hey Andrew — your research on scaling prediction markets with AI judges is fascinating. "
            "We're tackling a related problem: Notch builds perpetual derivatives on sports team strength, "
            "powered by our own oracle that reprices from bookmaker odds, results, and transfer news in real time. "
            f"Would love your academic perspective. {DECK_URL}"
        ),
    },
    "waynekimmel": {
        "tweet_ref": "SeventySix Capital investor, '#SportsTechVC #AssetClassofSports' in bio",
        "message": (
            "Hey Wayne — you literally coined #AssetClassofSports. That's exactly what we built: "
            "Notch creates perpetual derivatives on sports teams as a tradeable asset class. "
            "Go long Arsenal, short Man City — continuously, with leverage, across entire seasons. "
            f"Oracle live, Solana DEX. Raising seed. {DECK_URL}"
        ),
    },
    "kagisobond": {
        "tweet_ref": "Courtside Ventures partner, Real Money Gaming focus",
        "message": (
            "Hey Kai — Courtside's Real Money Gaming thesis maps directly to what we built. "
            "Notch is perpetual derivatives on sports team strength — continuous positions, "
            "not expiring bets. A new financial primitive for sports fans. "
            f"Oracle live for 96 soccer teams + NBA/MLB, Solana DEX. {DECK_URL}"
        ),
    },
    "zxocw": {
        "tweet_ref": "Tweeted 'the doomscrollers of today may be the fund managers of tomorrow'",
        "message": (
            "Hey Olaf — 'the doomscrollers of today may be the fund managers of tomorrow' is exactly our thesis. "
            "We built Notch: perpetual derivatives on sports teams that turn fans into continuous position holders. "
            "You seeded Polymarket for information markets — we're building the perps layer for sports. "
            f"Oracle live, Solana DEX. {DECK_URL}"
        ),
    },
    "thechrisbuskirk": {
        "tweet_ref": "Co-founded 1789 Capital which invested tens of millions in Polymarket",
        "message": (
            "Hey Chris — 1789's Polymarket conviction was prescient. We're building the next surface: "
            "Notch creates perpetual derivatives on sports team strength. Continuous positions, leverage, "
            "no expiry dates. Think perps applied to the $167B sports wagering market. "
            f"Solana DEX live. Raising seed. {DECK_URL}"
        ),
    },
    "FranklinBi": {
        "tweet_ref": "Tweeted about 'chaos markets' and 'leveraged prediction markets on streakers at the Super Bowl'",
        "message": (
            "Hey Franklin — your 'leveraged prediction markets' and 'chaos markets' tweets are hilarious and prescient. "
            "We actually built the leveraged sports markets: Notch is perpetual derivatives on team strength. "
            "Continuous positions, funding rates, leverage — all on Solana. "
            f"Oracle live for 96 soccer + NBA/MLB. {DECK_URL}"
        ),
    },
    "0xMasonH": {
        "tweet_ref": "Tweeted about investing in Megapot and why it's better than Fomo3d",
        "message": (
            "Hey Mason — saw your take on Megapot vs Fomo3d and the 'make it better yourself' thesis. "
            "That's what we did with sports markets: Notch is perpetual derivatives on team strength. "
            "Not event contracts, not lotteries — continuous perps for sports. "
            f"Solana DEX live, oracle for 96 teams. {DECK_URL}"
        ),
    },
    "_kinjalbshah": {
        "tweet_ref": "GP at Blockchain Capital which led $55M Polymarket round",
        "message": (
            "Hey Kinjal — Blockchain Capital's Polymarket conviction shows deep prediction markets thesis. "
            "We're building the perpetuals layer: Notch creates continuous derivatives on sports team strength. "
            "Positions don't expire, they compound through seasons. "
            f"Oracle live, Solana DEX. Raising seed. {DECK_URL}"
        ),
    },
    "im_manderson": {
        "tweet_ref": "Led Framework's Synthetix investment (perps protocol), co-founded Hashletes (NFL)",
        "message": (
            "Hey Michael — you bet on Synthetix becoming 'a decentralized BitMex' and founded Hashletes with NFL licensing. "
            "Notch sits at that exact intersection: perpetual derivatives on sports team strength. "
            "Synthetix-style perps for a new asset class. "
            f"Oracle live, Solana DEX. {DECK_URL}"
        ),
    },
    "GuptaRK22": {
        "tweet_ref": "Co-hosts Glue Guys podcast about sports/business intersection",
        "message": (
            "Hey Ravi — the Glue Guys podcast shows you think deeply about sports as business. "
            "We built Notch: perpetual derivatives that let you hold continuous positions on team strength. "
            "Go long the Lakers across an entire season, not just one game. "
            f"Oracle live for NBA/MLB + 96 soccer teams. {DECK_URL}"
        ),
    },
    "PeteVlastelica": {
        "tweet_ref": "Former CEO of Activision Blizzard Esports, Elysian Park portfolio includes DraftKings",
        "message": (
            "Hey Pete — from running Activision Blizzard Esports to investing alongside DraftKings, "
            "you know where gaming and sports wagering converge. Notch is perpetual derivatives on team strength — "
            "the tradeable layer between sports fandom and financial markets. "
            f"Oracle live, Solana DEX. {DECK_URL}"
        ),
    },
    "deepenparikh": {
        "tweet_ref": "Partner at Courtside investing in sports/gaming, Ravens fan",
        "message": (
            "Hey Deepen — as a Ravens fan, imagine going long Baltimore at the start of the season "
            "and holding that position through every game, trade, and injury. That's Notch: "
            "perpetual derivatives on team strength. Continuous, not expiring. "
            f"Oracle live for NFL + 96 soccer teams + NBA/MLB. {DECK_URL}"
        ),
    },
    "chadstender": {
        "tweet_ref": "Bio: 'Sports media enthusiast and Web3', Managing Partner SeventySix Capital",
        "message": (
            "Hey Chad — sports media x Web3 is exactly where we sit. Notch creates perpetual derivatives "
            "on team strength, fully on-chain on Solana. The financial layer sports media has been missing. "
            f"Oracle live, DEX with 13 markets. Raising seed. {DECK_URL}"
        ),
    },
    "santiagoroel": {
        "tweet_ref": "Asked about Polymarket NFT definitions, deeply active in DeFi",
        "message": (
            "Hey Santiago — your DeFi lens is exactly the perspective we need. "
            "Notch is perpetual derivatives on sports team strength — a new uncorrelated asset class for DeFi. "
            "Funding rates, leverage, continuous positions on Solana. "
            f"Oracle live for 96 soccer + NBA/MLB. {DECK_URL}"
        ),
    },
    "EvgenyGaevoy": {
        "tweet_ref": "Wintermute is major crypto market maker, directly relevant to prediction market liquidity",
        "message": (
            "Hey Evgeny — Wintermute's market making is exactly what our markets need. "
            "Notch is perpetual derivatives on sports team strength — new uncorrelated asset class on Solana. "
            "We're looking for liquidity partners and strategic investors who understand market making for new primitives. "
            f"{DECK_URL}"
        ),
    },
    "ColeVanNice1": {
        "tweet_ref": "Dodgers ownership group, Elysian Park portfolio includes DraftKings and SeatGeek",
        "message": (
            "Hey Cole — as part of the Dodgers ownership and backing DraftKings, you see where sports and financial products converge. "
            "Notch creates perpetual derivatives on team strength — imagine fans holding continuous positions on the Dodgers. "
            f"Oracle live, Solana DEX. {DECK_URL}"
        ),
    },
    "vasu": {
        "tweet_ref": "Tweeted about NBA Draft Lottery excitement, manages Courtside Ventures",
        "message": (
            "Hey Vasu — your NBA Draft Lottery excitement is the energy we're building for. "
            "Notch is perpetual derivatives on team strength — hold continuous positions across NBA seasons, "
            "not just single games. Real Money Gaming evolved. "
            f"Oracle live, Solana DEX. {DECK_URL}"
        ),
    },
    "mattyryze": {
        "tweet_ref": "Ryze Labs focuses on crypto x AI intersection, invested in Solana ecosystem",
        "message": (
            "Hey Matthew — your crypto x AI thesis and Solana ecosystem conviction align perfectly. "
            "Notch is perpetual derivatives on sports teams, built on Solana. "
            "Our oracle uses real-time data feeds to reprice team strength indices. "
            f"13 markets live. Raising seed. {DECK_URL}"
        ),
    },
    # Accounts that were not found
    "willreed_21": {
        "tweet_ref": "Led Spark's $70M Underdog Fantasy Series C",
        "message": (
            "Hey Will — the Underdog Fantasy deal showed massive sports gaming conviction. "
            "We're building the next layer: Notch creates perpetual derivatives on team strength. "
            "Continuous positions, leverage, no expiry. Think what perps did to spot applied to sports. "
            f"Oracle live, Solana DEX. {DECK_URL}"
        ),
    },
}


def main():
    prospects = json.loads(Path("output/prospect_report.json").read_text())
    tweets_data = json.loads(Path("output/tweets.json").read_text())

    outreach = []
    for p in prospects:
        username = p["username"]
        msg_data = MESSAGES.get(username)
        if not msg_data:
            continue

        # Get follower count from tweets data
        tw = tweets_data.get(username, {})

        outreach.append({
            "username": username,
            "name": p["name"],
            "firm": p["firm"],
            "role": p.get("role", ""),
            "tier": p["tier"],
            "profile_url": p["profile_url"],
            "followers": tw.get("followers", 0),
            "bio": tw.get("bio", p.get("evidence", "")),
            "message": msg_data["message"],
            "tweet_ref": msg_data["tweet_ref"],
            "evidence": p.get("evidence", ""),
        })

    # Sort by tier priority
    tier_order = {"HOT": 0, "WARM": 1, "LUKEWARM": 2}
    outreach.sort(key=lambda x: tier_order.get(x["tier"], 3))

    out_path = Path("output/outreach.json")
    out_path.write_text(json.dumps(outreach, indent=2))
    print(f"Generated {len(outreach)} personalized messages")
    print(f"Saved to {out_path}")

    # Print sample
    for o in outreach[:3]:
        print(f"\n[{o['tier']}] @{o['username']} ({o['firm']})")
        print(f"  Message: {o['message'][:150]}...")


if __name__ == "__main__":
    main()
