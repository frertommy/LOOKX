#!/usr/bin/env python3
"""Rewrite all DMs in user's actual voice — short, casual, punchy.

Style guide based on user's actual successful messages:
- lowercase, casual
- "first ever perp dex for sports" lead
- "Like Hyperliquid meets DraftKings" analogy
- Concrete mechanics: "long/short teams 24/7 365 across seasons"
- Mention beta site: tail.trade
- Mention TG: sempertrade
- Short — 2-4 sentences max
- For prediction markets folks: "Kalshi/poly are mostly sports. So it's an attempt to capture that audience with a totally different derivative product"
"""
from __future__ import annotations

import json
from pathlib import Path

TG = "tg: @sempertrade"
SITE = "tail.trade"

# Personalized hook line per prospect — 1 sentence referencing their work
# Then standard pitch line + tg
HOOKS = {
    # Crypto VCs - Tier 1 prediction markets
    "eightyhi": "you and noah are literally the prediction markets fund — would love your read on this angle",
    "Nostroah": "your kalshi ops experience + sports prediction takes are exactly the lens we need",
    "joeykrug": "augur was right, just early. this is the perp version for sports",
    "NTmoney": "you said sports prediction needs to be 100x bigger — here's our shot at it",
    "arjunblj": "saw paradigm's prediction markets terminal — we'd be a natural new asset class on it",
    "_alekslarsen": "your polymarket thesis is exactly what we're extending into perps for sports",
    "guywuolletjr": "loved the kairos seed. we're the asset class for the trading terminal",
    "veradittakit": "novig was the right bet. we're the perps version of that thesis",
    "fawzitani": "your novig take on consumers + financial products is our exact framing",
    "RealOmeedMalik": "1789's polymarket conviction was right. we're extending that to perps for sports",
    "prayanks": "saw the pred investment. we're a different angle — perps not event contracts",
    "danrobinson": "your pm-amm work is foundational. we're applying perps mechanics to a new asset class",

    # Solana
    "shayonsengupta": "your 'exchange is strictly superior to sportsbooks' take is our founding thesis",
    "_Dave__White_": "your power perpetuals work is the standard. we're applying the structure to sports",
    "HadickM": "between cftc and dragonfly's polymarket bet, you get this space better than anyone",
    "tomhschmidt": "your $1.7B global polymarket take — sports is the next 100x of that",
    "mickymalka": "you backed 5c(c). same thesis but we're the perps layer instead of event contracts",
    "GigiLevy": "you ran 888 — the gambling infra for the next generation looks like this",
    "willreed_21": "underdog showed silicon valley believes in sports gaming. we're the next layer",
    "mhiggins": "action network was the data play. we're the trading layer on top",
    "cegapereira": "your prediction market integrity takes are sharp — we use our own oracle for that reason",
    "tomloverro": "ivp's 'kalshi everything exchange' — we're event contracts taken to perps for sports",
    "ahall_research": "your a16z prediction markets research has been the playbook",
    "waynekimmel": "you literally coined #AssetClassofSports. that's the product",
    "kagisobond": "courtside's real money gaming thesis maps directly. ours is the perps version",
    "zxocw": "you seeded polymarket. we're the perps layer for that thesis on sports",
    "thechrisbuskirk": "1789's polymarket bet was right. we're extending to perps for sports",
    "FranklinBi": "your 'leveraged prediction markets' tweets hit. that's literally what we built",
    "0xMasonH": "your megapot/'make it better' take is exactly what we did to sports markets",
    "_kinjalbshah": "your polymarket conviction is right. we're the next surface — perps for sports",
    "im_manderson": "framework's synthetix bet + your hashletes nfl experience = exact match",
    "GuptaRK22": "glue guys energy + sequoia — perps for sports turns fans into traders",
    "PeteVlastelica": "you ran activision blizzard esports. perps for sports is the next vertical",
    "deepenparikh": "as a ravens fan, imagine going long baltimore for the season instead of game by game",
    "chadstender": "sports media x web3 — we're the financial layer that's been missing",
    "santiagoroel": "your defi lens is exactly what we need — uncorrelated asset class on solana",
    "EvgenyGaevoy": "wintermute's market making is exactly what new asset classes like ours need",
    "ColeVanNice1": "dodgers + draftkings — fans holding continuous positions on their team",
    "vasu": "saw your nba lottery energy. we're built for fans who never want their position to expire",
    "mattyryze": "ryze's solana + ai thesis maps directly. we're solana-native perps for sports",

    # New batch (Solana ecosystem + angels + more VCs)
    "j__fort": "huge respect for novig. this is the adjacent perp primitive — would love your take",
    "Domahhhh": "your prediction market analyses are required reading. perps version for sports here",
    "nigeleccles": "fanduel, betdex, bethog — you've built every category. this is the perps version",
    "Tristan0x": "between zeta and bullet, you've built the perps standard on solana. new asset class here",
    "AntonioMJuliano": "dydx + builder codes + prediction markets is exactly the convergence we're built on",
    "rleshner": "you seeded polymarket in 2020. we're the next step — perps on sports",
    "jessewldn": "'bringing perps to the people' is our exact playbook for a new asset class",
    "masonnystrom": "your variant rfs called out longer-tail sports prediction. this is the perps version",
    "_charlienoyes": "kalshi board observer + paradigm — would value your design take on a new derivative",
    "adamscochran": "your defi/prediction market threads are sharp. would love your take on this primitive",
    "NateSilver538": "polymarket's loudest advocate. perps for sports turns conviction into compounding positions",
    "davijlu": "drift's BET pioneered prediction markets on solana. we're the perps version",
    "MSpirito": "359's LP network (MSG/Adidas/CFG) is exactly the strategic backing we need",
    "richkleiman": "kd's team stakes + 35V — fans holding continuous positions on lakers across seasons",
    "SplitCapital": "split's derivatives focus is the angle. new uncorrelated asset class on solana",
    "gametheorizing": "poker brain + selini — new market structure for MMs to print",
    "jack__sanford": "flash trade quality is the bar. new asset class perps on solana here",
    "y2kappa": "your tradfi exotic derivatives background is the exact lens we need",
    "mdudas": "linksdao showed you get sports x crypto. 6mv's solana thesis matches",
    "kaiynne": "synthetix was the og perps bet. infinex is where perps go. ours is a new asset class",
    "rajgokal": "your tbd angel shows solana prediction markets is your category. this is the perps layer",
    "lessin": "you called solana prediction markets early. perps for sports is the next surface",
    "mattytay": "colosseum's solana thesis is our category. we're solana-native perps for sports",
    "QwQiao": "you said prediction markets is the hottest crypto category. agreed — perps version here",
    "mariogabriele": "your krug profile captured the zeitgeist. happy to be a source for the next piece",
    "tarunchitra": "your ADL research is sharp. new asset class = new pricing/risk problems to solve",
    "ZeMariaMacedo": "delphi's 'perps eat tradfi' + your poker brain = exact match for this thesis",
    "shaughnessy119": "'perp dexs eat tradfi' is the thesis. sports perps is the largest untapped category",
    "pierskicks": "your gaming x crypto lens is exactly where sports perps sit",
    "cburniske": "your solana conviction + placeholder's decentralized markets thesis = direct match",
    "jmonegro": "fat protocols still holds. we're three entities (oracle/dex/app) reinforcing the protocol",
    "ljin18": "ownership economy thesis maps perfectly — fans become continuous position holders",
    "spencernoon": "ournetwork covers solana perps. we'll add new metrics — happy to ship for a future issue",
    "lalleclausen": "1kx's defi perps + solana research is foundational. we're the new asset class on it",
    "pet3rpan_": "your gaming/IP thesis maps — sports teams as tradeable IP",
    "avichal": "electric's zeta bet = solana perps conviction. we're extending to a new asset class",
    "mariashen": "your developer report shows solana wins. notch is the kind of solana-native app you bet on",
    "diogomonica": "your 'bridging tradfi with defi' posts are our exact playbook",
    "ahnchrisj": "haun's defi infra portfolio is the right ecosystem for what we built",
    "ed_roman": "hack vc's breadth across solana perps infra makes you a natural check",
    "roshunpatel": "your genesis defi background + hack labs = exact right seat for this",
    "stefancoh": "bain crypto's L1 + defi + games mandate covers our exact intersection",
    "sethgrosenberg": "greylock's consumer + crypto + gaming mandate fits perfectly",
    "PrimordialAA": "poker + layerzero + fomo — you've been on every edge of this curve",
    "armaniferrante": "backpack's perps infra is a reference point. new asset class here",
    "StaniKulechov": "aave + infinex angel — would love your take on a new defi primitive on solana",
    "buffalu__": "jito's MEV insights are directly relevant for perp DEX order flow",
    "blknoiz06": "you move solana attention like no one else. would love to chat angels",
    "Fiskantes": "zee prime's defi primitives coverage is our kind of fund",
    "nemild": "yc's totalis bet shows solana prediction markets is a category. we're the perps layer",
    "calilyliu": "'prediction markets defining solana's evolution' — this is the perps surface for that",
    "Austin_Federa": "you've interviewed every solana perps founder. this is the next conversation",
    "kashdhanda": "superteam's role is foundational. would love to chat builders + angels",
    "nate_levine": "colosseum's technical diligence is the bar. our three-entity arch will hold up",
    "YanLiberman": "delphi's 'perps eat tradfi' gives the framing. $150B+ TAM here outside current dexs",
    "ricomallozzi": "359's sports + consumer gaming mandate is the perfect match",
    "therealchaseeb": "solana devrel og — happy to be a founder route or resource",
    "akshaybd": "superteam + foundation — you're at the center. would love your take",
    "LucaNetz": "pudgy's nascar play showed crypto rides mainstream sports. we're an adjacent angle",
}


# Build the message
def build_msg(name: str, hook: str, prospect: dict) -> str:
    first_name = name.split()[0].lower()

    # Decide pitch line based on tier and category
    portfolio = (prospect.get("portfolio") or "").lower()
    bio = (prospect.get("bio") or "").lower()
    evidence = (prospect.get("evidence") or "").lower()
    blob = portfolio + bio + evidence

    # If they're prediction-markets focused, use the kalshi/poly framing
    pm_signals = ["polymarket", "kalshi", "novig", "prediction market", "limitless"]
    is_pm_person = any(sig in blob for sig in pm_signals)

    if is_pm_person:
        pitch = (
            f"hey {first_name}, building the first ever perp dex for sports — "
            f"long/short teams 24/7 365 across seasons. like Hyperliquid meets DraftKings. "
            f"kalshi/poly are mostly sports — this captures that audience with a totally different derivative product. "
            f"{hook}. beta in dev: {SITE}. {TG}"
        )
    else:
        pitch = (
            f"hey {first_name}, building the first ever perp dex for sports — "
            f"long/short teams 24/7 365 across seasons. like Hyperliquid meets DraftKings. "
            f"{hook}. beta in dev: {SITE}. {TG}"
        )

    return pitch


def main():
    outreach = json.loads(Path("output/outreach.json").read_text())
    updated = 0
    missing = []

    for prospect in outreach:
        username = prospect["username"]
        if username not in HOOKS:
            missing.append(username)
            continue

        hook = HOOKS[username]
        prospect["message"] = build_msg(prospect["name"], hook, prospect)
        updated += 1

    Path("output/outreach.json").write_text(json.dumps(outreach, indent=2))

    print(f"Rewrote {updated}/{len(outreach)} messages")
    if missing:
        print(f"Missing hooks for: {missing}")

    # Print 3 samples
    for p in outreach[:3]:
        print(f"\n--- @{p['username']} ({p.get('firm', '')}) ---")
        print(p['message'])


if __name__ == "__main__":
    main()
