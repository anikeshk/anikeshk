"""Regenerate assets/header-{light,dark}.svg (subset Google Fonts embedded as base64). Run: python3 scripts/banner.py"""
import base64, re, urllib.parse, urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"
OUT = __import__("pathlib").Path(__file__).resolve().parent.parent / "assets"

EYEBROW = "SANTA CLARA, CALIFORNIA"
SITE = "ANIKESHK.COM ↗"
NAME = "Anikesh G Kamath"
TAG1 = "Software engineer building security automation — the APIs,"
TAG2 = "pipelines, and agentic workflows that turn security findings into fixes."
META_B = "Senior Software Engineer at Lineaje"
META = " · MSCS from Northeastern"


def font(family, text):
    q = urllib.parse.quote(text)
    req = urllib.request.Request(f"https://fonts.googleapis.com/css2?family={family}&text={q}", headers={"User-Agent": UA})
    css = urllib.request.urlopen(req).read().decode()
    url = re.search(r"url\((https://[^)]+)\)", css).group(1)
    data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read()
    return base64.b64encode(data).decode()


fonts = {
    "F": font("Fraunces:opsz,wght@144,600", NAME),
    "W": font("Work+Sans:wght@400", TAG1 + TAG2 + META),
    "WB": font("Work+Sans:wght@600", META_B),
    "M": font("IBM+Plex+Mono:wght@500", EYEBROW + SITE),
}

PALETTES = {
    "light": dict(bg="#fdfdfd", fg="#1b1b1b", muted="#5a5a5a", rule="#d6d6d6"),
    "dark": dict(bg="#0d1117", fg="#f3f3f3", muted="#b0b0b0", rule="#30363d"),
}

W, H = 880, 300

for name, p in PALETTES.items():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{NAME} — {TAG1} {TAG2}">
  <style>
    @font-face {{ font-family: "F"; font-weight: 600; src: url(data:font/woff2;base64,{fonts["F"]}) format("woff2"); }}
    @font-face {{ font-family: "W"; font-weight: 400; src: url(data:font/woff2;base64,{fonts["W"]}) format("woff2"); }}
    @font-face {{ font-family: "W"; font-weight: 600; src: url(data:font/woff2;base64,{fonts["WB"]}) format("woff2"); }}
    @font-face {{ font-family: "M"; font-weight: 500; src: url(data:font/woff2;base64,{fonts["M"]}) format("woff2"); }}
    .eyebrow {{ font: 500 12px "M", ui-monospace, monospace; letter-spacing: 0.16em; fill: {p["muted"]}; }}
    .name {{ font: 600 64px "F", Georgia, serif; letter-spacing: -0.005em; fill: {p["fg"]}; }}
    .tag {{ font: 400 19px "W", system-ui, sans-serif; fill: {p["fg"]}; }}
    .meta {{ font: 400 15px "W", system-ui, sans-serif; fill: {p["muted"]}; }}
    .meta tspan.b {{ font-weight: 600; fill: {p["fg"]}; }}
    .rise {{ opacity: 0; animation: rise .7s cubic-bezier(.2,.7,.2,1) forwards; }}
    .d1 {{ animation-delay: .05s; }} .d2 {{ animation-delay: .15s; }} .d3 {{ animation-delay: .25s; }} .d4 {{ animation-delay: .35s; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
    @media (prefers-reduced-motion: reduce) {{ .rise {{ animation: none; opacity: 1; }} }}
  </style>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{p["bg"]}" stroke="{p["rule"]}"/>
  <g class="rise d1">
    <circle cx="44" cy="58" r="4" fill="{p["fg"]}"/>
    <text class="eyebrow" x="58" y="62">{EYEBROW}</text>
    <text class="eyebrow" x="{W - 40}" y="62" text-anchor="end">{SITE}</text>
  </g>
  <text class="name rise d2" x="38" y="138">{NAME}</text>
  <g class="rise d3">
    <text class="tag" x="40" y="186">{TAG1}</text>
    <text class="tag" x="40" y="214">{TAG2}</text>
  </g>
  <g class="rise d4">
    <line x1="40" y1="242" x2="{W - 40}" y2="242" stroke="{p["rule"]}"/>
    <text class="meta" x="40" y="272"><tspan class="b">{META_B}</tspan>{META}</text>
  </g>
</svg>
"""
    with open(f"{OUT}/header-{name}.svg", "w") as f:
        f.write(svg)
    print(name, len(svg))
