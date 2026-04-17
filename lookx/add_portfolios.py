#!/usr/bin/env python3
"""Add portfolio companies to each prospect in outreach.json."""
from __future__ import annotations

import json
from pathlib import Path

# Portfolio companies from 3 parallel research agents
PORTFOLIOS = {
    # Batch 1 (1-33)
    "SplitCapital": "Plasma, Hyperliquid, Ethena, Pendle",
    "chadstender": "VSiN, Vigtory, FORTË, IC360",
    "ricomallozzi": "Overtime, Fevo, Backbone, beehiiv",
    "fawzitani": "Chime, Faire, Hims & Hers, OURA",
    "kagisobond": "Camb.ai, Fanstake, Overtime, 100 Thieves",
    "cegapereira": "Immutable, Karate Combat, EVE Frontier, Axie Infinity",
    "nate_levine": "Ore, Urani, BlockMesh, Helium",
    "j__fort": "Novig (sports prediction exchange, $75M raised)",
    "ahnchrisj": "Lighter, Helius, Conduit, BVNK",
    "PeteVlastelica": "PrizePicks, Second Spectrum, IDL, Appetite",
    "eightyhi": "5c(c) fund (prediction markets infrastructure, Kalshi/Polymarket LPs)",
    "ed_roman": "EigenLayer, Mysten Labs, Goldfinch, AltLayer",
    "jack__sanford": "Flash Trade (Solana perps DEX, 20x leverage)",
    "Nostroah": "5c(c) fund (prediction markets infra, ex-Kalshi)",
    "waynekimmel": "VSiN, Vigtory, Lucra, IC360",
    "stefancoh": "Compound Finance, BlockFi, Zero Hash, ParaFi",
    "prayanks": "Pred, Zetwerk, Bizongo, OnsiteGo",
    "0xMasonH": "Megapot (angel), a16z crypto Web3 infra deals",
    "shayonsengupta": "Novig, io.net, Geodnet, Helium, Drift",
    "davijlu": "Drift Protocol, Magic Eden, Katana",
    "ahall_research": "a16z research advisor (governance work: Optimism, Uniswap)",
    "deepenparikh": "Draftea, Rei do Pitaco, Xpoint, Players Lounge",
    "GigiLevy": "Novig, Playtika, Plarium, 888 Holdings",
    "nemild": "Totalis (YC Solana prediction market), Coinbase, OpenSea, dYdX",
    "lalleclausen": "Liquity, WalletConnect, Rarible, Celestia",
    "vasu": "The Athletic, StockX, Draftea, Packz",
    "y2kappa": "Kamino Finance (Solana DeFi), Hubble Protocol",
    "nigeleccles": "BetDEX, BetHog, Rei do Pitaco, Draftea",
    "jmonegro": "0x, Aptos, Avalanche, Arweave",
    "sethgrosenberg": "Ramp, Wisetack, Pine, Tome",
    "HadickM": "Polymarket, Ethena, Monad, Hidden Road",
    "roshunpatel": "Erebor, EigenLayer, Mysten Labs, AltLayer",
    "guywuolletjr": "Kairos (prediction markets terminal), Solana, LayerZero, EigenLayer",

    # Batch 2 (34-65)
    "RealOmeedMalik": "Polymarket, Enhanced Games, GrabAGun, Substack",
    "im_manderson": "Synthetix, Chainlink, Aave, The Graph",
    "YanLiberman": "dYdX, Lido, Uniswap, Axie Infinity",
    "diogomonica": "Anchorage Digital, Messari, Aptos, OpenSea",
    "Tristan0x": "Bullet (Solana L2 perps), Zeta Markets",
    "mattytay": "Ore, Urani, BlockMesh, Metadow",
    "mickymalka": "Polymarket (5cc LP), Robinhood, Coinbase, Nubank",
    "tomloverro": "Kalshi, Coinbase, HashiCorp, NerdWallet",
    "GuptaRK22": "Fireblocks, Faire, Noom, Instacart",
    "mariashen": "Magic Eden, dYdX, Lido, Helium",
    "_kinjalbshah": "Polymarket, OpenSea, Upshot, Ripple",
    "mhiggins": "The Action Network, Drone Racing League, Relevent Sports, Int'l Champions Cup",
    "buffalu__": "Jito Network, JitoSOL, BAM (Block Assembly Marketplace)",
    "pierskicks": "Axie Infinity, Illuvium, Yuga Labs, Sandbox",
    "Domahhhh": "Polymarket (#1 trader, $2.5M+ profit, 300M+ volume)",
    "masonnystrom": "Farcaster, Uniswap, Ondo, Story Protocol",
    "tomhschmidt": "Polymarket, Ethena, Lido, Parcl",
    "richkleiman": "Coinbase, NBA Top Shot/Dapper Labs, Overtime, Gotham FC",
    "zxocw": "Polymarket (seed), dYdX, Compound, Celestia",
    "FranklinBi": "Novig, Bitso, Ondo Finance, Azra Games",
    "pet3rpan_": "The Sandbox, The Graph, Matter Labs, Parallel",
    "_Dave__White_": "Power Perpetuals/Squeeth research, Floor Perpetuals, Distribution Markets",
    "thechrisbuskirk": "Polymarket, SpaceX, xAI, Perplexity AI",
    "_charlienoyes": "Kalshi (board observer), Polymarket, Uniswap, Blur",
    "akshaybd": "Superteam Solana startups, Balaji Gaming, Aper, Xeet",
    "kashdhanda": "Raiku, Jupiter (advisor), Solana startups",
    "veradittakit": "Novig, Circle, Arbitrum, Ondo",
    "AntonioMJuliano": "dYdX (founder), Magic Eden (advisor), Plume",
    "joeykrug": "Polymarket, Augur (co-founder), Kalshi, Eco",
    "calilyliu": "Osmosis, Earn.com (Coinbase exit), Anagram portfolio, Brave",
    "arjunblj": "BetDEX, Kalshi, 3Jane, Showtime",
    "jessewldn": "Uniswap, Phantom, Farcaster, Flashbots",

    # Batch 3 (66-98)
    "mariogabriele": "Generalist Capital (narrative-driven seed deals)",
    "avichal": "Zeta Markets, dYdX, Anchorage, OpenSea",
    "shaughnessy119": "LayerZero, Immutable, MCDEX, Yield Guild Games",
    "ZeMariaMacedo": "LayerZero, Immutable, Yield Guild Games, MCDEX",
    "tarunchitra": "EigenLayer, Lido Finance, Flashbots, Gauntlet",
    "NTmoney": "Polymarket, Limitless Labs, dYdX, OpenSea",
    "danrobinson": "Uniswap, dYdX, Blur, Optimism",
    "mattyryze": "Solana, LayerZero, Polygon, Wintermute",
    "EvgenyGaevoy": "Wintermute market-making (crypto derivatives/liquidity)",
    "therealchaseeb": "Luminal (ML compiler), Solana Mobile projects",
    "Fiskantes": "Synthetix, Solana, Sigil (DeFi liquid staking)",
    "PrimordialAA": "Fomo, SkyArk Chronicles, Crypto Rogue Games, OpenToken",
    "spencernoon": "Canto, Cap Labs, Aave, Lens Protocol",
    "lessin": "TBD (Solana prediction market), Solana, Algorand, Robinhood",
    "gametheorizing": "Mantle Network (Chief Alchemist), Selini trading",
    "santiagoroel": "Illuvium, Blast, LayerZero, MegaETH",
    "kaiynne": "Synthetix, Infinex, 3Jane, Cap Labs",
    "armaniferrante": "Backpack Exchange, Jito Labs, Mad Lads, Anchor framework",
    "QwQiao": "dYdX, 0x, Synthetix, Paraswap",
    "Austin_Federa": "DoubleZero, Solana ecosystem infrastructure",
    "ljin18": "Yield Guild Games, Syndicate, XMTP, Mirror",
    "LucaNetz": "Pudgy Penguins, Abstract (L2), Overpass NFT, Cube Labs",
    "StaniKulechov": "Aave, Lido, Maple Finance, Zerion",
    "adamscochran": "MakerDAO, Circle, Kraken, Reflexer Labs",
    "rleshner": "Compound, Polymarket (angel), Superstate, Frax",
    "cburniske": "Backpack, Jito, Celestia, Solana",
    "mdudas": "LinksDAO, The Block, POAP, Web3 gaming startups",
    "rajgokal": "Drift, TBD prediction market, Tensor, Helius",
    "blknoiz06": "Solayer, Monad, Ethena Labs, Shogun",
    "_alekslarsen": "Polymarket, Axiom Trust, Blockchain Capital portfolio",
    "willreed_21": "Underdog Fantasy, Abridge, Baseten, Scale AI",
    "ColeVanNice1": "DraftKings, EP Golf Ventures, SeatGeek, Overtime",
    "NateSilver538": "Polymarket (advisor), Silver Bulletin (founder)",
}


def main():
    outreach = json.loads(Path("output/outreach.json").read_text())
    added = 0
    missing = []

    for prospect in outreach:
        username = prospect["username"]
        if username in PORTFOLIOS:
            prospect["portfolio"] = PORTFOLIOS[username]
            added += 1
        else:
            missing.append(username)
            prospect["portfolio"] = ""

    Path("output/outreach.json").write_text(json.dumps(outreach, indent=2))
    print(f"Added portfolios to {added}/{len(outreach)} prospects")
    if missing:
        print(f"Missing: {missing}")


if __name__ == "__main__":
    main()
