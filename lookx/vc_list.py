"""Seed list of VC firms to find individual partners/associates on X."""

VC_FIRMS = [
    # Crypto-native
    "1Confirmation",
    "5c Capital",
    "Dragonfly Capital",
    "Multicoin Capital",
    "Pantera Capital",
    "Paradigm",
    "Framework Ventures",
    "a16z crypto",
    "Blockchain Capital",
    "Coinbase Ventures",
    "Electric Capital",
    "Fabric Ventures",
    "Galaxy Interactive",
    "Haun Ventures",
    "Jump Crypto",
    "Polychain Capital",
    "Sino Global Capital",
    "Parafi",
    "Wintermute Ventures",

    # Tier-1 generalist / crossover
    "Sequoia Capital",
    "Ribbit Capital",
    "Coatue Management",
    "Forerunner Ventures",
    "Founders Fund",
    "Point72 Ventures",
    "1789 Capital",
    "Accel",
    "Chemistry VC",
    "D1 Capital",
    "General Catalyst",
    "IVP",
    "Meritech Capital",
    "NFX",
    "SV Angel",
    "Spark Capital",
    "Bessemer Venture Partners",

    # Sports / gaming / betting focused
    "Bitkraft Ventures",
    "Bond Capital",
    "Elysian Park Ventures",
    "Bruin Capital",
    "RSE Ventures",
    "Makers Fund",
    "Arctos Sports Partners",
    "Edge Equity",
    "SeventySix Capital",
    "Courtside Ventures",
    "HXCO",
    "Sapphire Sport",
]

# Alternate names / search aliases so we catch bio variations
FIRM_ALIASES = {
    "a16z crypto": ["a16z", "andreessen horowitz", "a16z crypto"],
    "5c Capital": ["5c capital", "5cc"],
    "Dragonfly Capital": ["dragonfly", "dragonfly capital"],
    "Multicoin Capital": ["multicoin", "multicoin capital"],
    "Pantera Capital": ["pantera", "pantera capital"],
    "Framework Ventures": ["framework", "framework ventures"],
    "Coinbase Ventures": ["coinbase ventures", "coinbase"],
    "Jump Crypto": ["jump crypto", "jump trading"],
    "Polychain Capital": ["polychain", "polychain capital"],
    "Sino Global Capital": ["sino global", "sino capital"],
    "Wintermute Ventures": ["wintermute"],
    "Sequoia Capital": ["sequoia"],
    "Coatue Management": ["coatue"],
    "Founders Fund": ["founders fund", "ff"],
    "Point72 Ventures": ["point72", "point 72"],
    "General Catalyst": ["general catalyst", "gc"],
    "Bessemer Venture Partners": ["bessemer", "bvp"],
    "Elysian Park Ventures": ["elysian park"],
    "RSE Ventures": ["rse ventures", "rse"],
    "Arctos Sports Partners": ["arctos"],
    "SeventySix Capital": ["seventysix capital", "76 capital"],
    "Courtside Ventures": ["courtside"],
    "HXCO": ["hxco", "halo experience"],
    "Sapphire Sport": ["sapphire sport", "sapphire ventures"],
    "Haun Ventures": ["haun ventures", "haun"],
}


def get_search_terms(firm: str) -> list[str]:
    """Get all search terms for a firm (name + aliases)."""
    terms = [firm.lower()]
    if firm in FIRM_ALIASES:
        terms.extend(FIRM_ALIASES[firm])
    return list(set(terms))
