#!/usr/bin/env python3
"""Generate personalized DMs for the NEW prospects."""
from __future__ import annotations

import json
from pathlib import Path

DECK_URL = "https://frertommy.github.io/DEck/"

# Wrong handles — skip
BAD_HANDLES = {"brianreilly", "mboiron"}

# Hand-crafted messages for each new prospect
NEW_MESSAGES = {
    "j__fort": {
        "ref": "Running Novig — CEO of the fastest-growing sports prediction market in America",
        "msg": (
            "Hey Jacob — massive respect for what you've built at Novig. We're building the adjacent primitive: "
            "Notch is perpetual derivatives on sports team strength indices. Continuous long/short positions "
            "that don't expire — think Novig × perps. Oracle live for 96 soccer + NBA/MLB, Solana DEX. "
            f"Would love to chat about where our roadmaps converge. {DECK_URL}"
        ),
    },
    "Domahhhh": {
        "ref": "#1 all-time Polymarket trader — $300M+ volume, 5,000+ markets",
        "msg": (
            "Hey Domer — your analyses on prediction market design are required reading. "
            "We built Notch: perpetual derivatives on sports teams — continuous positions, leverage, no expiry. "
            "Oracle live for 96 soccer teams + NBA/MLB on Solana. Would love your take on where the edge is vs "
            f"traditional event contracts. {DECK_URL}"
        ),
    },
    "nigeleccles": {
        "ref": "Founded FanDuel, now running BetHog/BetDEX",
        "msg": (
            "Hey Nigel — FanDuel, BetDEX, now BetHog — you've literally built every major sports betting category. "
            "We built Notch: perpetual derivatives on team strength. Continuous positions across seasons instead of "
            "match-by-match. Oracle live, Solana DEX. Would genuinely love your take — there's no one better positioned "
            f"to call BS on this. {DECK_URL}"
        ),
    },
    "Tristan0x": {
        "ref": "Building Bullet on-chain perps, ex-Zeta Markets (first Solana orderbook perps DEX)",
        "msg": (
            "Hey Tristan — between Zeta and Bullet, you've built Solana's most sophisticated perps infrastructure. "
            "We built Notch: perpetual derivatives on a new asset class — sports team strength. "
            "Oracle live for 96 soccer teams + NBA/MLB, Solana DEX. Think perps for sports. "
            f"Would love your mechanism design take. {DECK_URL}"
        ),
    },
    "AntonioMJuliano": {
        "ref": "dYdX founder building prediction markets + perps + builder codes",
        "msg": (
            "Hey Antonio — dYdX shipping builder codes and prediction markets at the same time is the convergence "
            "thesis we're building on. Notch is perpetual derivatives on sports team strength — continuous positions, "
            f"no expiry, oracle live for 96 soccer + NBA/MLB on Solana. {DECK_URL}"
        ),
    },
    "rleshner": {
        "ref": "Compound founder, early Polymarket angel (2020)",
        "msg": (
            "Hey Robert — you seeded Polymarket in 2020 when most people thought prediction markets were dead. "
            "We're building the next step: Notch creates perpetual derivatives on sports teams. "
            "Continuous positions, leverage, no expiry. Oracle live, Solana DEX with 13 markets. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "jessewldn": {
        "ref": "Variant's 'Bringing Perps to the People' regulatory thesis",
        "msg": (
            "Hey Jesse — 'Bringing Perps to the People' is one of the best pieces written on perps policy. "
            "We built Notch on that thesis: perpetual derivatives on sports team strength, framed as continuous "
            "index derivatives (like equity indices). Oracle live, Solana DEX. "
            f"Raising seed — would love to chat. {DECK_URL}"
        ),
    },
    "masonnystrom": {
        "ref": "Wrote Variant's RFS 2024 calling out sports prediction markets",
        "msg": (
            "Hey Mason — your Variant RFS calling out longer-tail sports prediction markets is basically our pitch. "
            "Notch is perpetual derivatives on sports teams — continuous positions vs expiring event contracts. "
            "Oracle live for 96 soccer + NBA/MLB, Solana DEX. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "_charlienoyes": {
        "ref": "Paradigm prediction markets lead, publicly debates market design",
        "msg": (
            "Hey Charlie — your takes on prediction market dispute resolution and tokenholder governance are sharp. "
            "We're tackling an orthogonal problem: Notch builds perpetual derivatives on sports team strength "
            "with our own oracle repricing from bookmaker odds, results, and transfer news. "
            f"Would really value your perspective on the design. {DECK_URL}"
        ),
    },
    "adamscochran": {
        "ref": "Prolific CT threader on DeFi + prediction markets",
        "msg": (
            "Hey Adam — your long-form DeFi and prediction market threads are some of the most rigorous analysis on X. "
            "We built Notch: perpetual derivatives on sports team strength — a new asset class with continuous "
            "repricing from our oracle. Solana DEX live. "
            f"Would love your analytical take. {DECK_URL}"
        ),
    },
    "NateSilver538": {
        "ref": "Polymarket Advisory Board member, prediction markets evangelist",
        "msg": (
            "Hey Nate — your Polymarket advisory work has made you the loudest voice in prediction markets. "
            "We built Notch: perpetual derivatives on sports team strength. Instead of binary event contracts, "
            "users hold continuous positions across seasons. Oracle live for NBA/MLB + 96 soccer teams. "
            f"Would love your take. {DECK_URL}"
        ),
    },
    "davijlu": {
        "ref": "Drift co-founder, 20+ Solana angel investments",
        "msg": (
            "Hey David — Drift's BET product pioneered prediction markets on Solana. "
            "We're building a different angle: Notch is perpetual derivatives on sports team strength — "
            "continuous positions on team indices, not event contracts. Oracle live, Solana DEX with 13 markets. "
            f"Would love to compare notes. {DECK_URL}"
        ),
    },
    "MSpirito": {
        "ref": "359 Capital — $300M AUM, LPs include MSG, Adidas, City Football Group",
        "msg": (
            "Hey Michael — 359's LP network (MSG, Adidas, City Football Group, 30+ team owners) is exactly the "
            "strategic backing we need. Notch is perpetual derivatives on sports team strength — fans hold "
            "continuous positions on their teams instead of match-by-match bets. Oracle live for 96 soccer + NBA/MLB. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "richkleiman": {
        "ref": "35V with Kevin Durant, team ownership stakes across sports",
        "msg": (
            "Hey Rich — between 35V's sports portfolio and KD's team stakes, you see where fandom and finance "
            "converge better than anyone. Notch is perpetual derivatives on sports team strength — go long the "
            "Lakers for an entire season, not just one game. Oracle live, Solana DEX. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "SplitCapital": {
        "ref": "Derivatives-focused fund, constantly discusses perps + prediction markets",
        "msg": (
            "Hey Zaheer — Split Capital's derivatives focus is exactly the angle we need. "
            "Notch is perpetual derivatives on sports team strength — new uncorrelated asset class. "
            "Funding rates, leverage, no expiry. Oracle live for 96 soccer + NBA/MLB on Solana. "
            f"{DECK_URL}"
        ),
    },
    "gametheorizing": {
        "ref": "Ex-poker pro, Selini market makes prediction markets + perps",
        "msg": (
            "Hey Jordi — between poker and Selini, you think about odds and liquidity better than almost anyone. "
            "We built Notch: perpetual derivatives on sports team strength. New market structure, Selini-grade "
            "opportunities for MM. Oracle live, Solana DEX. "
            f"Would love to chat. {DECK_URL}"
        ),
    },
    "jack__sanford": {
        "ref": "Flash Trade Solana perps DEX CEO, ex-HFT",
        "msg": (
            "Hey Jack — Flash Trade's HFT-grade execution on Solana is the standard we benchmark against. "
            "We built Notch: perpetual derivatives on a new asset class — sports team strength. "
            "Oracle live for 96 soccer + NBA/MLB. Solana DEX with 13 markets. "
            f"Would love to chat ecosystem. {DECK_URL}"
        ),
    },
    "y2kappa": {
        "ref": "Kamino co-founder with TradFi derivatives pricing background",
        "msg": (
            "Hey Marius — your TradFi exotic derivatives background is exactly the lens we need. "
            "Notch is perpetual derivatives on sports team strength — continuous indices repriced in real time. "
            "Funding rate mechanics, leverage, on-chain settlement on Solana. "
            f"Would love your pricing take. {DECK_URL}"
        ),
    },
    "mdudas": {
        "ref": "6MV 50% Solana-heavy fund, LinksDAO Web3 golf NFT founder",
        "msg": (
            "Hey Mike — LinksDAO showed you get sports-crypto convergence, and 6MV's Solana-heavy thesis is "
            "exactly our playing field. Notch is perpetual derivatives on sports team strength — Solana DEX, "
            "oracle live for 96 soccer teams + NBA/MLB. Your check size range matches our raise. "
            f"{DECK_URL}"
        ),
    },
    "kaiynne": {
        "ref": "Synthetix founder, building Infinex perps superapp on Solana",
        "msg": (
            "Hey Kain — Synthetix was the OG bet that synthetic derivatives could be on-chain, and Infinex is "
            "where perps are going. Notch takes that to a new asset class: sports team strength perpetuals. "
            "Oracle live, Solana DEX. "
            f"Would love your operator take. {DECK_URL}"
        ),
    },
    "rajgokal": {
        "ref": "Solana co-founder, 19 angels incl. TBD (Solana prediction market)",
        "msg": (
            "Hey Raj — your TBD and Fomo angels show you see prediction markets as a Solana-native category. "
            "Notch extends that: perpetual derivatives on sports team strength — continuous positions instead "
            "of event contracts. Oracle live for 96 soccer + NBA/MLB, Solana DEX with 13 markets. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "lessin": {
        "ref": "TBD Solana prediction market angel, writes on betting markets",
        "msg": (
            "Hey Sam — you called Solana prediction markets early with the TBD angel, and your writing on "
            "betting markets has been ahead of the curve. Notch is perpetual derivatives on sports team strength. "
            "Continuous positions, no expiry. Oracle live, Solana DEX. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "mattytay": {
        "ref": "Colosseum $60M Solana fund, ex-Solana Foundation Head of Growth",
        "msg": (
            "Hey Matty — Colosseum's Solana-native thesis is exactly our category. "
            "Notch is perpetual derivatives on sports team strength — built on Solana, oracle for 96 soccer + "
            "NBA/MLB. Solana DEX with 13 markets live. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "QwQiao": {
        "ref": "Alliance DAO partner, called prediction markets + Telegram hottest categories",
        "msg": (
            "Hey Qiao — your take that prediction markets are the hottest crypto category is the energy we're "
            "riding. Notch is perpetual derivatives on sports team strength — different primitive from event "
            "contracts but same core thesis. Oracle live, Solana DEX. "
            f"Raising seed. Would love Alliance's take. {DECK_URL}"
        ),
    },
    "mariogabriele": {
        "ref": "The Generalist — wrote the Joey Krug / Founders Fund prediction markets profile",
        "msg": (
            "Hey Mario — your Joey Krug profile captured the prediction markets zeitgeist perfectly. "
            "We're building the adjacent primitive: Notch is perpetual derivatives on sports team strength. "
            "Oracle live for 96 soccer + NBA/MLB, Solana DEX. "
            f"Happy to be a source for your next piece on this category. {DECK_URL}"
        ),
    },
    "tarunchitra": {
        "ref": "Gauntlet CEO, published ADL and perp mechanism research",
        "msg": (
            "Hey Tarun — your ADL research and the Hyperliquid debates are some of the sharpest perps mechanism "
            "thinking out there. We built Notch: perpetual derivatives on sports team strength. New asset class, "
            "new pricing challenges — our oracle reprices from bookmaker odds, match results, transfer news. "
            f"Would love Gauntlet's risk lens. {DECK_URL}"
        ),
    },
    "ZeMariaMacedo": {
        "ref": "Ex-poker pro, Delphi bullish on perp DEXs eating TradFi",
        "msg": (
            "Hey José — between poker and Delphi's 'perps eating TradFi' thesis, you've been mapping this future "
            "for years. Notch is perpetual derivatives on sports team strength — maybe the largest untapped "
            "derivatives market. Oracle live, Solana DEX. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "shaughnessy119": {
        "ref": "Delphi 'Perp DEXs will eat TradFi 2026' thesis co-author",
        "msg": (
            "Hey Tom — 'Perp DEXs will eat TradFi' is the thesis we're executing on in a new vertical. "
            "Notch is perpetual derivatives on sports team strength — a $150B+ TAM sitting outside what current "
            "perps DEXs touch. Oracle live, Solana DEX. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "pierskicks": {
        "ref": "Gaming x crypto specialist at Delphi/Bitkraft",
        "msg": (
            "Hey Piers — your gaming-crypto lens is exactly where sports perps sit. "
            "Notch creates perpetual derivatives on sports team strength — fans hold continuous positions across "
            "seasons. Oracle live for 96 soccer teams + NBA/MLB, Solana DEX with 13 markets. "
            f"Would love your take. {DECK_URL}"
        ),
    },
    "cburniske": {
        "ref": "Public Solana bull, Placeholder decentralized markets thesis",
        "msg": (
            "Hey Chris — your Solana conviction is unmatched, and Placeholder's decentralized markets thesis "
            "maps directly to what we built. Notch is perpetual derivatives on sports team strength, on Solana. "
            "Oracle live for 96 soccer + NBA/MLB. DEX with 13 markets. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "jmonegro": {
        "ref": "'Fat Protocols' thesis author, Placeholder Solana DeFi investor",
        "msg": (
            "Hey Joel — Fat Protocols still holds up, and Notch is building at that layer: perpetual derivatives "
            "on sports team strength. Oracle (KOPS), DEX (Tail.trade), and consumer app (Notch.win) — "
            "three entities that reinforce the protocol. Solana-native. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "ljin18": {
        "ref": "Variant 'Ownership Economy' thesis, RFS called out prediction markets",
        "msg": (
            "Hey Li — your Ownership Economy thesis maps perfectly: Notch turns sports fans into continuous "
            "position holders on their teams. Perpetual derivatives on team strength, fully on-chain on Solana. "
            "Oracle live, DEX with 13 markets. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "spencernoon": {
        "ref": "OurNetwork covers Solana perps + prediction markets onchain data",
        "msg": (
            "Hey Spencer — OurNetwork has been tracking Drift, Jupiter, and prediction market metrics. "
            "Notch adds a new category: perpetual derivatives on sports team strength — measurable, onchain, "
            "with our own oracle data. Solana DEX with 13 markets live. "
            f"Happy to ship metrics for a future issue. {DECK_URL}"
        ),
    },
    "lalleclausen": {
        "ref": "1kx tracks DeFi perps + Solana tokenization",
        "msg": (
            "Hey Lasse — 1kx's DeFi perps and Solana research is foundational reading. "
            "Notch is perpetual derivatives on sports team strength — native fee capture, oracle licensing, "
            "trading fees, funding spread. Solana DEX live. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "pet3rpan_": {
        "ref": "1kx blockchain + entertainment investor",
        "msg": (
            "Hey Peter — your 1kx gaming/IP thesis maps directly: sports teams as tradeable IP. "
            "Notch creates perpetual derivatives on team strength — fans hold continuous positions across seasons. "
            f"Oracle live for 96 soccer + NBA/MLB, Solana DEX with 13 markets. Raising seed. {DECK_URL}"
        ),
    },
    "avichal": {
        "ref": "Electric Capital led Zeta Markets Solana perps",
        "msg": (
            "Hey Avichal — Electric's Zeta Markets bet showed conviction in Solana perps. "
            "We're extending into a new asset class: Notch is perpetual derivatives on sports team strength. "
            f"Oracle live for 96 soccer + NBA/MLB. Solana DEX, 13 markets. Raising seed. {DECK_URL}"
        ),
    },
    "mariashen": {
        "ref": "Electric Developer Report co-author, Solana bull",
        "msg": (
            "Hey Maria — your Developer Report shows Solana is winning developer mindshare, and Notch is the "
            "kind of Solana-native app you're betting on. Perpetual derivatives on sports team strength — "
            f"oracle live, DEX with 13 markets. Raising seed. {DECK_URL}"
        ),
    },
    "kendeeter": {
        "ref": "Electric DeFi + tokenomics lead",
        "msg": (
            "Hey Ken — Electric's DeFi + tokenomics lens is exactly what our token architecture needs. "
            "Notch is perpetual derivatives on sports team strength. Trading fees, oracle licensing, "
            f"funding spread, builder codes. Solana DEX live. Raising seed. {DECK_URL}"
        ),
    },
    "diogomonica": {
        "ref": "Haun GP, Anchorage founder, 'bridging TradFi with DeFi' takes",
        "msg": (
            "Hey Diogo — your 'bridging TradFi with DeFi' posts are exactly our playbook. "
            "Notch is perpetual derivatives on sports team strength — framed as continuous index derivatives "
            f"to navigate regs. Oracle live, Solana DEX. Raising seed. {DECK_URL}"
        ),
    },
    "ahnchrisj": {
        "ref": "Haun partner, DeFi infrastructure focus",
        "msg": (
            "Hey Chris — Haun's DeFi infra + stablecoins portfolio is the right ecosystem for what we built. "
            "Notch is perpetual derivatives on sports team strength. Oracle + DEX + consumer app on Solana. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "ed_roman": {
        "ref": "250+ crypto investments at Hack VC",
        "msg": (
            "Hey Ed — Hack VC's breadth across Solana perps infra makes you a natural check for Notch. "
            "Perpetual derivatives on sports team strength — oracle live for 96 soccer + NBA/MLB, Solana DEX. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "roshunpatel": {
        "ref": "Ex-Genesis DeFi VP, perps/derivatives expert",
        "msg": (
            "Hey Roshun — your Genesis DeFi background and Hack.labs initiative put you in the exact right seat. "
            "Notch is perpetual derivatives on sports team strength — new asset class, funding rate mechanics, "
            f"Solana DEX. Would love your take. {DECK_URL}"
        ),
    },
    "stefancoh": {
        "ref": "Bain Crypto co-lead, DeFi + games thesis",
        "msg": (
            "Hey Stefan — Bain Crypto's L1 + DeFi + games mandate covers our exact intersection. "
            "Notch is perpetual derivatives on sports team strength — DeFi primitive for sports fans. "
            f"Oracle live, Solana DEX. Raising seed. {DECK_URL}"
        ),
    },
    "sethgrosenberg": {
        "ref": "Greylock consumer + crypto + marketplaces + gaming",
        "msg": (
            "Hey Seth — your consumer + crypto + gaming mandate fits Notch like a glove. "
            "We built perpetual derivatives on sports team strength — a new consumer-crypto marketplace. "
            f"Oracle live for 96 soccer + NBA/MLB, Solana DEX. Raising seed. {DECK_URL}"
        ),
    },
    "PrimordialAA": {
        "ref": "LayerZero founder, ex-poker pro, Fomo prediction market angel",
        "msg": (
            "Hey Bryan — poker, LayerZero, Fomo — you've been on every edge of this curve. "
            "Notch is perpetual derivatives on sports team strength, built on Solana. "
            f"Cross-chain liquidity implications interesting too. Raising seed. {DECK_URL}"
        ),
    },
    "armaniferrante": {
        "ref": "Backpack Exchange derivatives on Solana, Anchor creator",
        "msg": (
            "Hey Armani — Backpack's perps infrastructure is a reference point for us. "
            "Notch creates perpetual derivatives on a new asset class: sports team strength. "
            f"Oracle live, Solana DEX with 13 markets. Raising seed. {DECK_URL}"
        ),
    },
    "StaniKulechov": {
        "ref": "Aave founder, Infinex Solana perps angel",
        "msg": (
            "Hey Stani — Aave's DeFi leadership and your Infinex angel show the range of your conviction. "
            "Notch is perpetual derivatives on sports team strength — new uncorrelated asset class on Solana. "
            f"Oracle live, DEX with 13 markets. Raising seed. {DECK_URL}"
        ),
    },
    "buffalu__": {
        "ref": "Jito CEO, Solana MEV/order-flow expert",
        "msg": (
            "Hey Lucas — Jito's MEV and order-flow insights are directly relevant for perp DEX order flow. "
            "Notch is perpetual derivatives on sports team strength on Solana. "
            f"Would love to chat MEV/liquidity implications. {DECK_URL}"
        ),
    },
    "blknoiz06": {
        "ref": "Solana maxi, active angel, huge amplification",
        "msg": (
            "Hey Ansem — you move Solana attention like no one else. "
            "Notch is perpetual derivatives on sports team strength — Solana DEX with 13 markets live. "
            f"Would love to chat angels + amplification. {DECK_URL}"
        ),
    },
    "Fiskantes": {
        "ref": "Zee Prime 'risk communist', DeFi primitives angel",
        "msg": (
            "Hey Fiskantes — Zee Prime's coverage of DeFi primitives is our kind of fund. "
            "Notch is perpetual derivatives on sports team strength — a new primitive, Solana-native. "
            f"Oracle live, DEX live. Raising seed. {DECK_URL}"
        ),
    },
    "nemild": {
        "ref": "YC invested in Totalis — Solana prediction market in USDC",
        "msg": (
            "Hey Nemil — YC's Totalis investment shows you see Solana prediction markets as a category. "
            "Notch builds adjacent: perpetual derivatives on sports team strength. "
            f"Oracle live, DEX with 13 markets. Raising seed. {DECK_URL}"
        ),
    },
    "calilyliu": {
        "ref": "Solana Foundation president, 'prediction markets defining Solana's evolution'",
        "msg": (
            "Hey Lily — you've said prediction markets are defining Solana's evolution. "
            "Notch is the perpetuals layer: continuous derivatives on sports team strength, Solana-native. "
            f"Oracle live for 96 soccer teams + NBA/MLB. 13 markets on our DEX. {DECK_URL}"
        ),
    },
    "Austin_Federa": {
        "ref": "Solana ecosystem angel, hosts Validated with perps founders",
        "msg": (
            "Hey Austin — you've interviewed every Solana perps founder on Validated. "
            "Notch is the next conversation: perpetual derivatives on sports team strength. "
            f"Oracle live, Solana DEX with 13 markets. Happy to come on the pod. {DECK_URL}"
        ),
    },
    "kashdhanda": {
        "ref": "Superteam Solana connector, active angel",
        "msg": (
            "Hey Kash — Superteam's role in the Solana ecosystem is foundational. "
            "Notch is perpetual derivatives on sports team strength, Solana DEX live. "
            f"Would love to chat builders + angels. {DECK_URL}"
        ),
    },
    "nate_levine": {
        "ref": "Ex-Stripe engineer, Colosseum Solana VC",
        "msg": (
            "Hey Nate — Colosseum's technical diligence reputation precedes you. "
            "Notch is perpetual derivatives on sports team strength — three-entity architecture (oracle, DEX, app) "
            f"for regulatory defensibility. Solana-native. Raising seed. {DECK_URL}"
        ),
    },
    "YanLiberman": {
        "ref": "Delphi managing partner, perps-as-next-TradFi thesis",
        "msg": (
            "Hey Yan — Delphi's perps-eat-TradFi thesis gives us the exact framing. "
            "Notch is perpetual derivatives on sports team strength — $150B+ TAM outside current perps DEXs. "
            f"Oracle live, Solana DEX. Raising seed. {DECK_URL}"
        ),
    },
    "0xChen": {
        "ref": "Ex-HFT, building Phoenix Perps on Solana",
        "msg": (
            "Hey Eugene — Phoenix Perps' HFT-grade engineering is the quality bar. "
            "Notch is perpetual derivatives on a new asset class: sports team strength. "
            "Oracle live for 96 soccer + NBA/MLB, Solana DEX with 13 markets. "
            f"Would love ecosystem chat. {DECK_URL}"
        ),
    },
    "ricomallozzi": {
        "ref": "359 Capital sports + consumer gaming partner",
        "msg": (
            "Hey Rico — 359's sports + consumer gaming mandate is the perfect match. "
            "Notch creates perpetual derivatives on sports team strength — new financial primitive for sports fans. "
            f"Oracle live for 96 soccer + NBA/MLB. Raising seed. {DECK_URL}"
        ),
    },
    "therealchaseeb": {
        "ref": "Solana OG devrel, routes deals to ecosystem funds",
        "msg": (
            "Hey Chase — Solana devrel OG, you know every founder worth backing. "
            "Notch is perpetual derivatives on sports team strength, Solana DEX with 13 markets. "
            f"Raising seed — happy to be a route or resource. {DECK_URL}"
        ),
    },
    "akshaybd": {
        "ref": "Solana Foundation CMO, Superteam DAO founder",
        "msg": (
            "Hey Akshay — Superteam's role in Solana and your Foundation work put you at the center of the ecosystem. "
            "Notch is perpetual derivatives on sports team strength. Oracle live, Solana DEX with 13 markets. "
            f"Raising seed. {DECK_URL}"
        ),
    },
    "LucaNetz": {
        "ref": "Pudgy Penguins CEO, NASCAR partnerships, Fomo angel",
        "msg": (
            "Hey Luca — Pudgy's NASCAR play showed crypto can ride mainstream sports. "
            "Notch is perpetual derivatives on sports team strength — a different angle on that thesis. "
            f"Oracle live for 96 soccer teams + NBA/MLB. Raising seed. {DECK_URL}"
        ),
    },
}


def main():
    new_prospects = json.loads(Path("output/new_prospects.json").read_text())
    tweets_data = json.loads(Path("output/tweets.json").read_text())
    outreach = json.loads(Path("output/outreach.json").read_text())
    existing_usernames = {p["username"] for p in outreach}

    added = 0
    skipped = []
    for prospect in new_prospects:
        username = prospect["username"]
        if username in existing_usernames:
            continue
        if username in BAD_HANDLES:
            skipped.append(f"{username} (bad handle)")
            continue

        tw = tweets_data.get(username, {})
        if tw.get("error") or not tw.get("bio"):
            skipped.append(f"{username} (no data)")
            continue

        msg_data = NEW_MESSAGES.get(username)
        if not msg_data:
            skipped.append(f"{username} (no message crafted)")
            continue

        outreach.append({
            "username": username,
            "name": prospect["name"],
            "firm": prospect["firm"],
            "role": prospect.get("role", ""),
            "tier": prospect["tier"],
            "profile_url": prospect["profile_url"],
            "followers": tw.get("followers", 0),
            "bio": tw.get("bio", ""),
            "message": msg_data["msg"],
            "tweet_ref": msg_data["ref"],
            "evidence": prospect.get("evidence", ""),
        })
        added += 1

    Path("output/outreach.json").write_text(json.dumps(outreach, indent=2))
    print(f"Added {added} new prospects")
    print(f"Total now: {len(outreach)}")
    if skipped:
        print(f"Skipped: {len(skipped)}")
        for s in skipped:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
