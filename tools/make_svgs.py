"""Generates the animated SVGs used by README.md.  Run:  python tools/make_svgs.py"""
import os, random

ROOT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(os.path.join(ROOT, "projects"), exist_ok=True)

BG, BG2, LINE = "#0A0F1D", "#111A2E", "#1E2A44"
NAVY, ORANGE, BLUE, GREEN, TEXT, MUTED = "#12203A", "#FF5A1F", "#2F6BFF", "#1ED760", "#E6EAF2", "#8A94AA"
SANS = "'Inter','Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','Cascadia Code',Consolas,'SFMono-Regular',Menlo,monospace"
STYLE = f"<style>.s{{font-family:{SANS}}}.m{{font-family:{MONO}}}</style>"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write(name, body, w, h, label):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
           f'role="img" aria-label="{esc(label)}">{STYLE}{body}</svg>\n')
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def card_bg(w, h, rid, glow=True):
    """Dark rounded card with grid, two soft glows and a slow scan line."""
    s = f'''<defs>
<pattern id="g{rid}" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#fff" stroke-opacity=".035"/></pattern>
<radialGradient id="o{rid}" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate({w*0.12} {h*0.1}) scale({w*0.45} {h*0.9})"><stop stop-color="{ORANGE}" stop-opacity=".22"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>
<radialGradient id="b{rid}" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate({w*0.9} {h*0.95}) scale({w*0.45} {h*0.9})"><stop stop-color="{BLUE}" stop-opacity=".25"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<linearGradient id="sc{rid}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{BLUE}" stop-opacity="0"/><stop offset=".5" stop-color="{BLUE}" stop-opacity=".12"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
<clipPath id="k{rid}"><rect width="{w}" height="{h}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#k{rid})"><rect width="{w}" height="{h}" fill="{BG}"/><rect width="{w}" height="{h}" fill="url(#g{rid})"/>'''
    if glow:
        s += f'''<rect width="{w}" height="{h}" fill="url(#o{rid})"><animate attributeName="opacity" values="1;.55;1" dur="7s" repeatCount="indefinite"/></rect>
<rect width="{w}" height="{h}" fill="url(#b{rid})"><animate attributeName="opacity" values=".6;1;.6" dur="7s" repeatCount="indefinite"/></rect>
<rect y="-80" width="{w}" height="80" fill="url(#sc{rid})"><animateTransform attributeName="transform" type="translate" values="0 0;0 {h+80}" dur="6s" repeatCount="indefinite"/></rect>'''
    return s


def card_end(w, h):
    return f'</g><rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="22" fill="none" stroke="{LINE}"/>'


def typing_keys(n, cw, start, T, type_dt=.07, hold=1.6, erase_dt=.025):
    pts = [(0.0, 0)]
    for k in range(1, n + 1):
        pts.append((start + k * type_dt, k * cw))
    t2 = start + n * type_dt + hold
    for k in range(n - 1, -1, -1):
        pts.append((t2 + (n - k) * erase_dt, k * cw))
    end = pts[-1][0]
    kt = ";".join(f"{t / T:.4f}" for t, _ in pts)
    vals = ";".join(f"{v:.1f}" for _, v in pts)
    return kt, vals, end


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1200, 440
    s = card_bg(W, H, "h")
    # neural network on the right
    random.seed(7)
    layers = [(830, 3), (935, 5), (1040, 5), (1135, 2)]
    nodes = [[(x, 220 + (i - (n - 1) / 2) * 62) for i in range(n)] for x, n in layers]
    edges = ""
    for a, b in zip(nodes, nodes[1:]):
        for p in a:
            for q in b:
                edges += f'<path d="M{p[0]} {p[1]}L{q[0]} {q[1]}" stroke="#fff" stroke-opacity=".07"/>'
    s += edges
    sig = ""
    for i in range(14):
        path = [random.choice(l) for l in nodes]
        d = "M" + "L".join(f"{x} {y}" for x, y in path)
        col = ORANGE if i % 2 else BLUE
        sig += (f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity=".0"/>'
                f'<circle r="3.2" fill="{col}" opacity="0"><animateMotion dur="2.6s" begin="{i*0.45:.2f}s" repeatCount="indefinite" path="{d}"/>'
                f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="2.6s" begin="{i*0.45:.2f}s" repeatCount="indefinite"/></circle>')
    s += sig
    for li, layer in enumerate(nodes):
        for ni, (x, y) in enumerate(layer):
            d = (li * 0.3 + ni * 0.17)
            s += (f'<circle cx="{x}" cy="{y}" r="13" fill="{BLUE if li%2 else ORANGE}" opacity=".12"><animate attributeName="r" values="9;15;9" dur="2.4s" begin="{d:.2f}s" repeatCount="indefinite"/></circle>'
                  f'<circle cx="{x}" cy="{y}" r="6" fill="{BG2}" stroke="{BLUE if li%2 else ORANGE}" stroke-width="2"/>')
    for (x, y), t in zip(nodes[0], ["data", "ideas", "users"]):
        s += f'<text x="{x-20}" y="{y+4}" text-anchor="end" class="m" font-size="11" fill="{MUTED}">{t}</text>'
    for (x, y), t in zip(nodes[3], ["models", "products"]):
        s += f'<text x="{x}" y="{y+30}" text-anchor="middle" class="m" font-size="11" fill="{MUTED}">{t}</text>'

    # top row
    s += f'<text x="56" y="62" class="m" font-size="13" letter-spacing="2" fill="{MUTED}">~/shravan-kasar <tspan fill="{ORANGE}">main</tspan> <tspan fill="{GREEN}">✔</tspan></text>'
    s += (f'<g transform="translate(56 92)"><rect width="250" height="30" rx="15" fill="{GREEN}" fill-opacity=".1" stroke="{GREEN}" stroke-opacity=".45"/>'
          f'<circle cx="18" cy="15" r="5" fill="{GREEN}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle>'
          f'<circle cx="18" cy="15" r="5" fill="none" stroke="{GREEN}"><animate attributeName="r" values="5;13" dur="1.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="1.4s" repeatCount="indefinite"/></circle>'
          f'<text x="34" y="20" class="m" font-size="12" letter-spacing="1" fill="{GREEN}">OPEN TO 2026 AI ROLES</text></g>')
    # name with moving gradient
    s += f'''<defs><linearGradient id="ng" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="700" y2="0" spreadMethod="reflect">
<stop stop-color="{ORANGE}"/><stop offset=".45" stop-color="#FFB37A"/><stop offset=".75" stop-color="#7EA6FF"/><stop offset="1" stop-color="{BLUE}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;700 0;0 0" dur="8s" repeatCount="indefinite"/></linearGradient></defs>'''
    s += f'<text x="56" y="160" class="m" font-size="18" fill="{MUTED}">&gt; hello world, I\'m</text>'
    s += f'<text x="52" y="238" class="s" font-size="86" font-weight="800" letter-spacing="-2.5" fill="url(#ng)">Shravan Kasar</text>'
    # typing roles
    roles = ["AI Engineer", "Agentic RAG builder", "Founder @ CaratCloud", "model → ONNX → production"]
    T, cw, x0, y = 14.0, 15.6, 92, 300
    s += f'<text x="56" y="{y}" class="m" font-size="26" fill="{ORANGE}">$</text>'
    for i, r in enumerate(roles):
        start = i * 3.5
        kt, vals, end = typing_keys(len(r), cw, start, T)
        kx = ";".join(f"{x0 + float(v):.1f}" for v in vals.split(";"))
        s += (f'<defs><clipPath id="r{i}"><rect x="{x0}" y="{y-28}" width="0" height="40"><animate attributeName="width" calcMode="discrete" dur="{T}s" repeatCount="indefinite" keyTimes="{kt}" values="{vals}"/></rect></clipPath></defs>'
              f'<text x="{x0}" y="{y}" class="m" font-size="26" fill="{TEXT}" clip-path="url(#r{i})">{esc(r)}</text>'
              f'<rect x="{x0}" y="{y-23}" width="13" height="28" fill="{ORANGE}" opacity="0">'
              f'<animate attributeName="x" calcMode="discrete" dur="{T}s" repeatCount="indefinite" keyTimes="{kt}" values="{kx}"/>'
              f'<animate attributeName="opacity" calcMode="discrete" dur="{T}s" repeatCount="indefinite" keyTimes="0;{start/T:.4f};{(end+0.3)/T:.4f}" values="0;.9;0"/></rect>')
    # bottom chips
    chips = [("B.Tech IT · Pillai College", BLUE), ("Navi Mumbai · IST", MUTED), ("10+ AI products shipped", ORANGE)]
    x = 56
    for t, c in chips:
        w = len(t) * 7.6 + 30
        s += (f'<g transform="translate({x} 352)"><rect width="{w:.0f}" height="32" rx="8" fill="{BG2}" stroke="{LINE}"/>'
              f'<circle cx="14" cy="16" r="3.5" fill="{c}"/><text x="25" y="21" class="m" font-size="12.5" fill="{TEXT}">{esc(t)}</text></g>')
        x += w + 12
    s += card_end(W, H)
    write("hero.svg", s, W, H, "Shravan Kasar — AI Engineer and Founder of CaratCloud")


# ---------------------------------------------------------------- terminal
def terminal():
    W, H = 1200, 340
    s = card_bg(W, H, "t", glow=False)
    s += f'<rect width="{W}" height="44" fill="{BG2}"/><path d="M0 44H{W}" stroke="{LINE}"/>'
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        s += f'<circle cx="{28 + i*22}" cy="22" r="6.5" fill="{c}"/>'
    s += f'<text x="{W/2}" y="27" text-anchor="middle" class="m" font-size="13" fill="{MUTED}">shravan@caratcloud: ~ — zsh</text>'
    lines = [
        ("cmd", "whoami"),
        ("out", [("shravan kasar", TEXT), ("  ·  AI engineer & founder of CaratCloud", MUTED)]),
        ("cmd", "cat focus.txt"),
        ("out", [("agentic RAG  ·  speech & NLP  ·  ML training → ONNX  ·  full-stack SaaS", "#7EA6FF")]),
        ("cmd", "./ship --to production"),
        ("out", [("✔ 10+ products shipped    ", GREEN), ("✔ 5 paying customers    ", GREEN), ("✔ 0 invented citations", GREEN)]),
    ]
    cw, t, y = 9.6, 0.6, 86
    for kind, val in lines:
        if kind == "cmd":
            n = len(val)
            dur = n * 0.06
            kt = ";".join(f"{k/n:.4f}" for k in range(n + 1))
            vals = ";".join(f"{k*cw:.1f}" for k in range(n + 1))
            s += (f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
                  f'<text x="32" y="{y}" class="m" font-size="16" fill="{ORANGE}">❯</text>'
                  f'<text x="54" y="{y}" class="m" font-size="16" fill="{BLUE}">~</text>'
                  f'<defs><clipPath id="tc{y}"><rect x="76" y="{y-18}" width="0" height="26"><animate attributeName="width" calcMode="discrete" begin="{t:.2f}s" dur="{dur:.2f}s" keyTimes="{kt}" values="{vals}" fill="freeze"/></rect></clipPath></defs>'
                  f'<text x="76" y="{y}" class="m" font-size="16" fill="{TEXT}" clip-path="url(#tc{y})">{esc(val)}</text></g>')
            t += dur + 0.35
        else:
            spans = "".join(f'<tspan fill="{c}">{esc(x)}</tspan>' for x, c in val)
            s += (f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
                  f'<text x="54" y="{y}" class="m" font-size="16">{spans}</text></g>')
            t += 0.6
        y += 36
    s += (f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
          f'<text x="32" y="{y}" class="m" font-size="16" fill="{ORANGE}">❯</text><text x="54" y="{y}" class="m" font-size="16" fill="{BLUE}">~</text>'
          f'<rect x="78" y="{y-15}" width="10" height="19" fill="{TEXT}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/></rect></g>')
    s += card_end(W, H)
    write("terminal.svg", s, W, H, "Terminal: whoami, focus areas, shipped results")


# ---------------------------------------------------------------- metrics
def metrics():
    W, H = 1200, 190
    s = f'''<defs><linearGradient id="mb" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="0" spreadMethod="reflect">
<stop stop-color="{ORANGE}"/><stop offset=".5" stop-color="{LINE}"/><stop offset="1" stop-color="{BLUE}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;1200 0" dur="6s" repeatCount="indefinite"/></linearGradient></defs>'''
    items = [
        (["0", "3", "6", "9", "10+"], "AI & WEB PRODUCTS", "SHIPPED", ORANGE, 1.0),
        (["0", "1", "2", "3", "4", "5"], "PAYING SAAS", "CUSTOMERS", GREEN, 0.5),
        (["0.0", "2.4", "5.1", "7.3", "8.5+"], "B.TECH", "CGPA", "#7EA6FF", 0.85),
        (["#99", "#62", "#31", "#18", "#14"], "SIH 2026 INTERNAL", "TOP 15 · TEAM NERVEAI", ORANGE, 0.93),
    ]
    cw, gap = 285, 20
    for i, (frames, l1, l2, col, frac) in enumerate(items):
        x = i * (cw + gap) + 1
        g = f'<g transform="translate({x} 1)">'
        g += f'<rect width="{cw-2}" height="{H-2}" rx="18" fill="{BG}"/><rect width="{cw-2}" height="{H-2}" rx="18" fill="none" stroke="url(#mb)" stroke-width="1.5"/>'
        g += f'<text x="24" y="38" class="m" font-size="11" letter-spacing="2" fill="{MUTED}">METRIC / 0{i+1}</text>'
        step = 0.12
        for k, fr in enumerate(frames):
            b = 0.3 + i * 0.15 + k * step
            if k < len(frames) - 1:
                g += (f'<text x="22" y="104" class="s" font-size="54" font-weight="800" fill="{col}" opacity="0">{esc(fr)}'
                      f'<set attributeName="opacity" to="1" begin="{b:.2f}s" end="{b+step:.2f}s"/></text>')
            else:  # final value is visible by default, hidden only while counting
                g += (f'<text x="22" y="104" class="s" font-size="54" font-weight="800" fill="{col}">{esc(fr)}'
                      f'<set attributeName="opacity" to="0" begin="0s" end="{b:.2f}s"/></text>')
        g += f'<text x="24" y="134" class="m" font-size="12" letter-spacing="1.3" fill="{TEXT}">{esc(l1)}</text>'
        g += f'<text x="24" y="152" class="m" font-size="12" letter-spacing="1.3" fill="{MUTED}">{esc(l2)}</text>'
        bw = cw - 50
        g += (f'<rect x="24" y="166" width="{bw}" height="4" rx="2" fill="{LINE}"/>'
              f'<rect x="24" y="166" width="{bw*frac:.0f}" height="4" rx="2" fill="{col}"><animate attributeName="width" values="0;0;{bw*frac:.0f}" keyTimes="0;{(0.3+i*0.15)/1.8:.3f};1" begin="0s" dur="1.8s" fill="freeze"/></rect>')
        s += g + "</g>"
    write("metrics.svg", s, W, H, "10+ products shipped, 5 paying customers, 8.5+ CGPA, SIH 2026 rank 14")


# ---------------------------------------------------------------- project cards
PROJECTS = [
    ("01", "Kavach 2.0", "AI Scam Shield for India",
     ["Checks SMS, WhatsApp screenshots, QR codes and live", "calls for scams in English, Hindi and Marathi."],
     "precision 0.992 · recall 0.969", ["Python", "FastAPI", "ONNX", "Next.js", "Whisper"], ORANGE),
    ("02", "NyayaSathi", "Agentic RAG Legal Aid",
     ["Turns a citizen's problem into a ready-to-file", "complaint with a 5-agent, citation-checked pipeline."],
     "0 invented citations", ["Next.js", "TypeScript", "Groq", "Gemini", "RAG"], BLUE),
    ("03", "VaaniShield 2.0", "Voice Deepfake Detection",
     ["Detects AI-cloned voices in calls and recordings.", "Wav2Vec2 fine-tuned on ASVspoof, int8 ONNX."],
     "2.66% EER on 4 s windows", ["PyTorch", "Wav2Vec2", "ONNX", "FastAPI"], BLUE),
    ("04", "ARIA", "Sovereign Agentic AI Workbench",
     ["On-prem agentic AI for a refinery team that proves", "what it did and that nothing left the building."],
     "10-attack red-team panel", ["Python", "LLM Agents", "Qwen", "Granite"], ORANGE),
    ("05", "TRINETRA", "Cyclone Decision Support",
     ["Satellite intensity, rapid-intensification and", "genesis models with Grad-CAM and CAP alerts."],
     "MAE 7.4 kt · ROC-AUC 0.89", ["PyTorch", "FastAPI", "Next.js", "ERA5"], ORANGE),
    ("06", "CaratCloud", "Jewellery Shop SaaS · my company",
     ["Stock, GST billing, saving schemes and gold loans", "in 3 languages as an installable PWA."],
     "5 paying shops", ["React", "Supabase", "PostgreSQL", "PWA"], BLUE),
]


def project(p):
    num, name, sub, desc, metric, tech, col = p
    W, H = 580, 250
    rid = "p" + num
    s = card_bg(W, H, rid, glow=False)
    s += f'''<defs><radialGradient id="pg{num}" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate({W} 0) scale(330 230)"><stop stop-color="{col}" stop-opacity=".22"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>
<linearGradient id="pl{num}" gradientUnits="userSpaceOnUse" x1="0" x2="200" y1="0" y2="0"><stop stop-color="{col}" stop-opacity="0"/><stop offset=".5" stop-color="{col}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#pg{num})"><animate attributeName="opacity" values="1;.5;1" dur="5s" repeatCount="indefinite"/></rect>
<rect y="0" width="200" height="3" fill="url(#pl{num})"><animateTransform attributeName="transform" type="translate" values="-200 0;{W} 0" dur="3.5s" repeatCount="indefinite"/></rect>'''
    s += f'<text x="{W-26}" y="70" text-anchor="end" class="s" font-size="64" font-weight="800" fill="#fff" fill-opacity=".05">{num}</text>'
    s += f'<text x="26" y="38" class="m" font-size="11" letter-spacing="2" fill="{col}">✦ FEATURED BUILD · {num}</text>'
    s += (f'<g transform="translate({W-92} 22)"><circle cx="8" cy="8" r="4" fill="{GREEN}"><animate attributeName="opacity" values="1;.25;1" dur="1.4s" repeatCount="indefinite"/></circle>'
          f'<text x="18" y="12" class="m" font-size="11" letter-spacing="1.5" fill="{GREEN}">SHIPPED</text></g>')
    s += f'<text x="26" y="78" class="s" font-size="27" font-weight="800" fill="{TEXT}">{esc(name)}</text>'
    s += f'<text x="26" y="101" class="s" font-size="14" fill="{MUTED}">{esc(sub)}</text>'
    for i, line in enumerate(desc):
        s += f'<text x="26" y="{132 + i*21}" class="s" font-size="14.5" fill="#C5CCDA">{esc(line)}</text>'
    mw = len(metric) * 7.3 + 34
    s += (f'<g transform="translate(26 166)"><rect width="{mw:.0f}" height="26" rx="6" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".5"/>'
          f'<text x="12" y="17.5" class="m" font-size="12" fill="{col}">▲ {esc(metric)}</text></g>')
    x = 26
    for t in tech:
        w = len(t) * 7.2 + 22
        s += f'<g transform="translate({x:.0f} 206)"><rect width="{w:.0f}" height="24" rx="12" fill="{BG2}" stroke="{LINE}"/><text x="{w/2:.0f}" y="16" text-anchor="middle" class="m" font-size="11.5" fill="{TEXT}">{esc(t)}</text></g>'
        x += w + 8
    s += f'<text x="{W-26}" y="223" text-anchor="end" class="m" font-size="12" fill="{MUTED}">view →</text>'
    s += card_end(W, H)
    write(f"projects/{num}.svg", s, W, H, f"{name}: {sub}")


# ---------------------------------------------------------------- tech stack marquee
COL = {"Python": "#FFD43B", "PyTorch": "#EE4C2C", "Hugging Face": "#FFD21E", "ONNX Runtime": "#B0B8C8", "Whisper": "#10A37F",
       "Wav2Vec2": "#7EA6FF", "scikit-learn": "#F7931E", "Agentic RAG": ORANGE, "Groq": "#F55036", "Gemini": "#8E75B2",
       "Qwen": "#615CED", "Grad-CAM": "#E0521D", "Speech & NLP": "#1ED760", "Next.js": "#FFFFFF", "React": "#61DAFB",
       "TypeScript": "#3178C6", "JavaScript": "#F7DF1E", "FastAPI": "#009688", "Flask": "#FFFFFF", "Django": "#2BA977",
       "Supabase": "#3FCF8E", "PostgreSQL": "#4169E1", "Firebase": "#FFCA28", "Vite": "#646CFF", "Flutter": "#02569B",
       "Vercel": "#FFFFFF", "Google Cloud": "#4285F4", "Git": "#F05032", "C#": "#9B4F96", "PHP": "#777BB4", "Tailwind": "#38BDF8"}


def stack():
    W, H = 1200, 170
    rows = [["Python", "PyTorch", "Hugging Face", "ONNX Runtime", "Whisper", "Wav2Vec2", "scikit-learn", "Agentic RAG", "Groq", "Gemini", "Qwen", "Grad-CAM", "Speech & NLP"],
            ["Next.js", "React", "TypeScript", "JavaScript", "FastAPI", "Flask", "Django", "Supabase", "PostgreSQL", "Firebase", "Vite", "Flutter", "Vercel", "Google Cloud", "Git"]]
    s = f'''<defs><linearGradient id="fade" x1="0" x2="1"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".08" stop-color="#fff"/><stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="fm"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask><clipPath id="sk"><rect width="{W}" height="{H}" rx="22"/></clipPath></defs>
<g clip-path="url(#sk)"><rect width="{W}" height="{H}" fill="{BG}"/><g mask="url(#fm)">'''
    for ri, row in enumerate(rows):
        y = 28 + ri * 64
        chips, x = "", 0
        for t in row:
            w = len(t) * 8.4 + 46
            chips += (f'<g transform="translate({x:.0f} 0)"><rect width="{w:.0f}" height="44" rx="12" fill="{BG2}" stroke="{LINE}"/>'
                      f'<circle cx="20" cy="22" r="5" fill="{COL.get(t, ORANGE)}"/><text x="33" y="27" class="m" font-size="14" fill="{TEXT}">{esc(t)}</text></g>')
            x += w + 12
        a, b = ("0", f"-{x:.0f}") if ri == 0 else (f"-{x:.0f}", "0")
        s += (f'<g transform="translate(0 {y})"><g><animateTransform attributeName="transform" type="translate" values="{a} 0;{b} 0" dur="{30+ri*6}s" repeatCount="indefinite"/>'
              f'{chips}<g transform="translate({x:.0f} 0)">{chips}</g><g transform="translate({2*x:.0f} 0)">{chips}</g></g></g>')
    s += f'</g></g><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="{LINE}"/>'
    write("stack.svg", s, W, H, "Tech stack: Python, PyTorch, ONNX, Next.js, React, FastAPI, Supabase and more")


# ---------------------------------------------------------------- divider + footer
def divider():
    W, H = 1200, 24
    s = f'''<defs><linearGradient id="dl" x1="0" x2="1"><stop stop-color="{ORANGE}" stop-opacity="0"/><stop offset=".5" stop-color="{ORANGE}" stop-opacity=".6"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
<radialGradient id="dg"><stop stop-color="#fff"/><stop offset=".35" stop-color="{ORANGE}"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient></defs>
<rect y="11" width="{W}" height="2" fill="url(#dl)"/>
<circle cy="12" r="10" fill="url(#dg)"><animate attributeName="cx" values="0;{W}" dur="4s" repeatCount="indefinite"/></circle>'''
    write("divider.svg", s, W, H, "divider")


def footer():
    W, H = 1200, 230
    s = card_bg(W, H, "f")
    for i, (col, op, dur, amp) in enumerate([(BLUE, .25, 9, 18), (ORANGE, .3, 7, 14), (NAVY, 1, 11, 10)]):
        y0 = 160 + i * 18
        d1 = f"M0 {y0} C300 {y0-amp} 300 {y0+amp} 600 {y0} S900 {y0-amp} 1200 {y0} V{H} H0Z"
        d2 = f"M0 {y0} C300 {y0+amp} 300 {y0-amp} 600 {y0} S900 {y0+amp} 1200 {y0} V{H} H0Z"
        s += f'<path d="{d1}" fill="{col}" fill-opacity="{op}"><animate attributeName="d" values="{d1};{d2};{d1}" dur="{dur}s" repeatCount="indefinite"/></path>'
    s += f'<text x="{W/2}" y="74" text-anchor="middle" class="s" font-size="40" font-weight="800" fill="{TEXT}">Student by day, <tspan fill="{ORANGE}">founder by night.</tspan></text>'
    s += f'<text x="{W/2}" y="112" text-anchor="middle" class="m" font-size="15" fill="{MUTED}">Hiring for AI, Agentic AI or Full-Stack? I reply within 24 hours  →</text>'
    s += card_end(W, H)
    write("footer.svg", s, W, H, "Student by day, founder by night. Let's build what's next.")


hero(); terminal(); metrics(); stack(); divider(); footer()
for p in PROJECTS:
    project(p)
print("ok:", sorted(os.listdir(ROOT)), sorted(os.listdir(os.path.join(ROOT, "projects"))))
