#!/usr/bin/env python3
"""Add AUM + lead round tag to each prospect."""
from __future__ import annotations

import json
from pathlib import Path

# Combined data from 3 parallel research agents
DATA = {
    # Batch 1
    "RealOmeedMalik": ("$1B", True),
    "thechrisbuskirk": ("$1B", True),
    "NTmoney": ("$1B", True),
    "lalleclausen": ("$275M", True),
    "pet3rpan_": ("$275M", True),
    "ricomallozzi": ("$300M", False),
    "richkleiman": ("Family Office", False),
    "eightyhi": ("$35M", False),
    "Nostroah": ("$35M", False),
    "mdudas": ("$145M", True),
    "StaniKulechov": ("Angel", False),
    "prayanks": ("$8.6B", False),
    "QwQiao": ("Accelerator", False),
    "cegapereira": ("$1B", True),
    "armaniferrante": ("Angel", False),
    "stefancoh": ("$560M", True),
    "nigeleccles": ("Angel", False),
    "_kinjalbshah": ("$2B", False),
    "_alekslarsen": ("$2B", False),
    "Tristan0x": ("Angel", False),
    "adamscochran": ("Angel", False),
    "nate_levine": ("$60M", True),
    "mattytay": ("$60M", True),
    "kagisobond": ("$300M", True),
    "deepenparikh": ("$300M", True),
    "vasu": ("$300M", True),
    "pierskicks": ("$1B", False),
    "YanLiberman": ("$150M", True),
    "shaughnessy119": ("$150M", True),
    "ZeMariaMacedo": ("$150M", False),
    "Austin_Federa": ("Angel", False),
    "HadickM": ("$2.6B", True),
    "tomhschmidt": ("$2.6B", True),
    "davijlu": ("Angel", False),

    # Batch 2
    "mariashen": ("$1B+", False),
    "avichal": ("$1B+", False),
    "PeteVlastelica": ("$399M", True),
    "ColeVanNice1": ("$399M", False),
    "jack__sanford": ("Angel", False),
    "fawzitani": ("$3B", False),
    "joeykrug": ("$3B+", False),
    "im_manderson": ("$1.4B", False),
    "sethgrosenberg": ("$3.5B", False),
    "ed_roman": ("$425M", False),
    "roshunpatel": ("$425M", False),
    "ahnchrisj": ("$2.5B", True),
    "diogomonica": ("$2.5B", False),
    "tomloverro": ("$9B", True),
    "buffalu__": ("Angel", False),
    "y2kappa": ("Founder", False),
    "PrimordialAA": ("Angel", False),
    "shayonsengupta": ("$6B", False),
    "GigiLevy": ("$2.3B", False),
    "j__fort": ("Founder", False),
    "FranklinBi": ("$5B", True),
    "veradittakit": ("$5B", True),
    "_Dave__White_": ("$12.7B", False),
    "arjunblj": ("$12.7B", True),
    "danrobinson": ("$12.7B", False),
    "jmonegro": ("$150M", False),
    "cburniske": ("$150M", False),
    "zxocw": ("$5B", False),
    "Domahhhh": ("Angel", False),
    "LucaNetz": ("Angel", False),
    "mhiggins": ("$1B+", False),
    "mickymalka": ("$12B", True),
    "tarunchitra": ("$75M", False),
    "mattyryze": ("$200M", False),

    # Batch 3
    "gametheorizing": ("$200M", False),
    "GuptaRK22": ("$56B", False),
    "chadstender": ("$50M", False),
    "waynekimmel": ("$50M", False),
    "NateSilver538": ("Advisor", False),
    "lessin": ("$770M", False),
    "calilyliu": ("Foundation", False),
    "akshaybd": ("Foundation", False),
    "rajgokal": ("Angel", False),
    "therealchaseeb": ("Angel", False),
    "willreed_21": ("$12B", False),
    "SplitCapital": ("Angel", False),
    "rleshner": ("$1.23B", False),
    "kashdhanda": ("Angel", False),
    "kaiynne": ("Angel", False),
    "blknoiz06": ("Angel", False),
    "mariogabriele": ("$12M", False),
    "jessewldn": ("$700M", True),
    "ljin18": ("$700M", False),
    "spencernoon": ("$700M", False),
    "masonnystrom": ("$5B", False),
    "EvgenyGaevoy": ("Market Maker", False),
    "nemild": ("Accelerator", False),
    "Fiskantes": ("$100M", False),
    "0xMasonH": ("$90B", False),
    "guywuolletjr": ("$90B", True),
    "ahall_research": ("Advisor", False),
    "AntonioMJuliano": ("Angel", False),
    "santiagoroel": ("$26.5M", False),
    "_charlienoyes": ("Angel", False),
}


def main():
    outreach = json.loads(Path("output/outreach.json").read_text())
    added = 0
    missing = []

    for prospect in outreach:
        username = prospect["username"]
        if username in DATA:
            aum, leads = DATA[username]
            prospect["aum"] = aum
            prospect["leads_rounds"] = leads
            added += 1
        else:
            missing.append(username)
            prospect["aum"] = ""
            prospect["leads_rounds"] = False

    # Sort by followers ascending again (preserve the sort)
    outreach.sort(key=lambda p: p.get("followers", 0) or 999999)

    Path("output/outreach.json").write_text(json.dumps(outreach, indent=2))

    leads_count = sum(1 for p in outreach if p.get("leads_rounds"))
    print(f"Added AUM + leads data to {added}/{len(outreach)} prospects")
    print(f"Leads Rounds: {leads_count} prospects tagged")
    if missing:
        print(f"Missing: {missing}")


if __name__ == "__main__":
    main()
