#!/usr/bin/env python3
"""Static site generator for scentfusionja.com — no dependencies, no build tooling."""
import json, os, re, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, 'data/collection.json')))
P, FAM, META = DATA['products'], DATA['families'], DATA['meta']
FAMN = {f['id']: f['name'] for f in FAM}
SITE = "https://scentfusionja.com"
WA = "18762535213"
IG = "scentfusionja"
EMAIL = "scentfusion876@gmail.com"

def w(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(content)

def e(s): return html.escape(str(s), quote=True)

# ---------------------------------------------------------------- bottle art
BOTTLES = {
 'amber':   '<path d="M40 8h20v10H40z"/><path d="M43 18h14v8H43z"/><path d="M22 26h56a6 6 0 016 6v54a6 6 0 01-6 6H22a6 6 0 01-6-6V32a6 6 0 016-6z"/><path d="M28 40v34" opacity=".45"/><circle cx="50" cy="60" r="11" opacity=".5"/>',
 'floral':  '<path d="M44 6h12v10H44z"/><ellipse cx="50" cy="21" rx="11" ry="5"/><path d="M25 28c0-4 5-7 25-7s25 3 25 7v44c0 13-11 21-25 21S25 85 25 72V28z"/><g opacity=".5"><ellipse cx="50" cy="52" rx="4" ry="8"/><ellipse cx="50" cy="52" rx="8" ry="4"/><ellipse cx="50" cy="52" rx="6.4" ry="6.4" transform="rotate(45 50 52)"/></g>',
 'gourmand':'<circle cx="50" cy="13" r="6.5"/><path d="M46.5 19.5h7v8h-7z"/><path d="M50 27.5c-15 0-25 11-25 27v20c0 10 10 16 25 16s25-6 25-16V54.5c0-16-10-27-25-27z"/><path d="M31 62q19 8 38 0" opacity=".45"/>',
 'fresh':   '<path d="M42 8h16v9H42z"/><path d="M45 17h10v9H45z"/><path d="M20 30h60v50a12 12 0 01-12 12H32a12 12 0 01-12-12V30z"/><path d="M20 30l60 0" opacity=".5"/><path d="M30 46c8 5 12-5 20 0s12-5 20 0" opacity=".45"/>',
 'woods':   '<path d="M43 8h14v12H43z"/><path d="M26 20h48v68a4 4 0 01-4 4H30a4 4 0 01-4-4V20z"/><path d="M38 20v72M50 20v72M62 20v72" opacity=".3"/>',
 'spice':   '<path d="M44 8h12v10H44z"/><path d="M40 18h20l8 12H32z"/><path d="M32 30h36v50a10 10 0 01-10 10H42a10 10 0 01-10-10V30z"/><path d="M50 48v26M40 58h20" opacity=".4"/>',
 'citrus':  '<path d="M45 6h10v11H45z"/><path d="M41 17h18v9H41z"/><path d="M50 26c-14 0-24 8-24 20v34c0 8 8 14 24 14s24-6 24-14V46c0-12-10-20-24-20z"/><g opacity=".4"><circle cx="50" cy="60" r="13"/><path d="M50 47v26M37 60h26M41 51l18 18M59 51L41 69"/></g>',
}
def bottle(fam, cls=''):
    d = BOTTLES.get(fam, BOTTLES['amber'])
    return (f'<svg class="{cls}" viewBox="0 0 100 100" fill="none" stroke="url(#gg)" '
            f'stroke-width="1.7" stroke-linejoin="round" aria-hidden="true">'
            f'<defs><linearGradient id="gg" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0%" stop-color="#c9962c"/><stop offset="45%" stop-color="#ffcb30"/>'
            f'<stop offset="100%" stop-color="#8a6f22"/></linearGradient></defs>{d}</svg>')

RINGS = ('<svg class="hero-rings" viewBox="0 0 600 600" fill="none" aria-hidden="true">'
 '<defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="1">'
 '<stop offset="0%" stop-color="#efbf00" stop-opacity=".55"/>'
 '<stop offset="100%" stop-color="#efbf00" stop-opacity="0"/></linearGradient></defs>'
 + ''.join(f'<circle cx="300" cy="300" r="{r}" stroke="url(#rg)" stroke-width="1"/>' for r in (110,150,190,232,276,300))
 + ''.join(f'<path d="M40 {y}q130 -26 260 0t260 0" stroke="url(#rg)" stroke-width="1" opacity=".5"/>' for y in (120,146,172,428,454,480))
 + '</svg>')

# ---------------------------------------------------------------- chrome
def head(title, desc, path, extra='', depth=0):
    url = SITE + path
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Scent Fusion Jamaica">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#08070a">
<link rel="icon" href="/assets/img/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/monogram-32.png">
<link rel="apple-touch-icon" href="/assets/img/monogram-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=Jost:wght@200;300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/main.css">
{extra}
</head>
<body data-base="{'../' * depth if depth else ''}">'''

NAVLINKS = [('/collection/','Collection'),('/scent-luxe/','Scent Luxe'),('/the-house/','The House'),('/partners/','Partners'),('/contact/','Contact')]

def header(cur=''):
    links = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == cur else '', t) for h, t in NAVLINKS)
    return f'''
<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
 <div class="wrap hdr-in">
  <a class="brand" href="/" aria-label="Scent Fusion Jamaica — home">
   <img src="/assets/img/sf-mark-150.png" srcset="/assets/img/sf-mark-150.png 1x, /assets/img/sf-mark-300.png 2x" alt="Scent Fusion Jamaica" width="28" height="40">
   <span class="brand-txt"><b>Scent Fusion</b><span>Jamaica</span></span>
  </a>
  <nav class="nav" aria-label="Primary">{links}</nav>
  <div class="hdr-act">
   <button class="icon-btn" data-cart-open aria-label="Open your selection">
    <svg viewBox="0 0 24 24"><path d="M6 7h12l-1 13H7L6 7z"/><path d="M9 7V5a3 3 0 016 0v2"/></svg>
    <span class="cart-count" aria-live="polite">0</span>
   </button>
   <button class="icon-btn burger" aria-label="Menu" aria-expanded="false">
    <svg viewBox="0 0 24 24"><path d="M4 8h16M4 16h16"/></svg>
   </button>
  </div>
 </div>
</header>'''

def drawer():
    return f'''
<div class="scrim" data-cart-close></div>
<aside class="drawer" aria-label="Your selection">
 <div class="drawer-hd"><h3>Your selection</h3>
  <button class="icon-btn" data-cart-close aria-label="Close"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>
 <div class="drawer-body"></div>
 <div class="drawer-ft">
  <div class="cart-total"><span class="tiny">Total</span><b data-cart-total>$0</b></div>
  <p class="tiny" style="text-transform:none;letter-spacing:.04em;color:var(--smoke-2);margin:0 0 .4rem">Free delivery in Kingston · island-wide courier available</p>
  <a class="btn btn-wa btn-block" href="#" data-wa-order>Order on WhatsApp</a>
  <a class="btn btn-ghost btn-block" href="#" data-card-pay>Pay by card</a>
 </div>
</aside>'''

def footer():
    fam = ''.join(f'<li><a href="/collection/?family={f["id"]}">{f["name"]}</a></li>' for f in FAM[:5])
    return f'''
<footer class="ftr">
 <div class="wrap">
  <div class="ftr-grid">
   <div>
    <a class="brand" href="/" style="margin-bottom:1.3rem">
     <img src="/assets/img/sf-mark-150.png" alt="" width="28" height="40">
     <span class="brand-txt"><b>Scent Fusion</b><span>Jamaica</span></span></a>
    <p class="small muted" style="max-width:34ch;margin:0 0 1.4rem">A Caribbean lifestyle house, built in Kingston. Where luxury fuses with your aroma.</p>
    <div class="socials">
     <a href="https://instagram.com/{IG}" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.6 0 4.9.07 1.2.05 1.8.25 2.2.42.6.22 1 .48 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c0 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2 0-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c0-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 3.2A6.6 6.6 0 1018.6 12 6.6 6.6 0 0012 5.4zm0 10.9A4.3 4.3 0 1116.3 12 4.3 4.3 0 0112 16.3zm6.9-11.1a1.55 1.55 0 11-1.55-1.55A1.55 1.55 0 0118.9 5.2z"/></svg></a>
     <a href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3A8.2 8.2 0 1112 20.2zm4.5-6.1c-.2-.1-1.4-.7-1.7-.8s-.4-.1-.5.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 01-2-1.2 7.4 7.4 0 01-1.4-1.7c-.1-.3 0-.4.1-.5l.4-.4.2-.4v-.4c0-.1-.5-1.3-.7-1.8s-.4-.4-.5-.4h-.4a.9.9 0 00-.6.3 2.6 2.6 0 00-.8 1.9 4.5 4.5 0 001 2.4 10.3 10.3 0 003.9 3.4 9.9 9.9 0 001.3.5 3.1 3.1 0 001.4.1 2.3 2.3 0 001.5-1.1 1.9 1.9 0 00.1-1.1c0-.1-.2-.2-.4-.3z"/></svg></a>
     <a href="mailto:{EMAIL}" aria-label="Email"><svg viewBox="0 0 24 24"><path d="M3 5h18v14H3z" fill="none" stroke="#f0e3c2" stroke-width="1.5"/><path d="M3 6l9 7 9-7" fill="none" stroke="#f0e3c2" stroke-width="1.5"/></svg></a>
    </div>
   </div>
   <div><h4>The House</h4><ul>
     <li><a href="/collection/">Collection</a></li>
     <li><a href="/scent-luxe/">Scent Luxe</a></li>
     <li><a href="/the-house/">Our story</a></li>
     <li><a href="/partners/">Stockists &amp; partners</a></li>
     <li><a href="/contact/">Contact</a></li></ul></div>
   <div><h4>Families</h4><ul>{fam}</ul></div>
   <div><h4>Visit &amp; order</h4>
    <ul>
     <li><a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp +1 (876) 253-5213</a></li>
     <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
     <li><a href="https://instagram.com/{IG}" target="_blank" rel="noopener">@{IG}</a></li>
    </ul>
    <p class="small muted" style="margin-top:1.1rem">39 Mansfield Avenue<br>Kingston 20, Jamaica</p>
   </div>
  </div>
  <div class="ftr-bot">
   <span>© <span data-year>2026</span> Scent Fusion Jamaica Ltd. All rights reserved.</span>
   <span><a href="/legal/privacy/">Privacy</a> · <a href="/legal/terms/">Terms</a> · <a href="/legal/shipping/">Delivery &amp; returns</a></span>
  </div>
 </div>
</footer>'''

def foot_scripts():
    return '<script src="/assets/js/config.js"></script><script src="/assets/js/app.js"></script></body></html>'


def relativize(html_str, depth):
    """Rewrite root-absolute hrefs/srcs to relative so the site works from
    file://, a subdirectory, or the live domain. Directory links get an
    explicit index.html because file:// does not serve directory indexes."""
    prefix = '../' * depth
    def sub(m):
        attr, path = m.group(1), m.group(2)
        if path.startswith('/'):      # protocol-relative, leave alone
            return m.group(0)
        head, sep, tail = path.partition('?')
        if head == '' or head.endswith('/'):
            head = head + 'index.html'
        return '%s="%s%s%s%s"' % (attr, prefix, head, sep, tail)
    html_str = re.sub(r'(href|src)="/([^"]*)"', sub, html_str)

    def sub_srcset(m):
        parts = []
        for cand in m.group(1).split(','):
            cand = cand.strip()
            if cand.startswith('/') and not cand.startswith('//'):
                cand = prefix + cand[1:]
            parts.append(cand)
        return 'srcset="%s"' % ', '.join(parts)
    return re.sub(r'srcset="([^"]*)"', sub_srcset, html_str)


def page(title, desc, path, body, cur='', extra='', schema='', depth=0, absolute=False):
    sch = f'<script type="application/ld+json">{schema}</script>' if schema else ''
    out = head(title, desc, path, extra, depth) + header(cur) + body + drawer() + footer() + sch + foot_scripts()
    if not absolute:
        out = relativize(out, depth)
    return out

# ---------------------------------------------------------------- cards
def card(p, delay=0):
    notes = ', '.join(p['notes']['top'][:2] + p['notes']['base'][:1])
    d = f' rv-d{delay}' if delay else ''
    search = f"{p['name']} {FAMN[p['family']]} {p['wear']} {notes} {p['line']}".lower()
    return f'''<article class="card rv{d}" data-card data-wear="{p['wear']}" data-family="{p['family']}" data-search="{e(search)}">
 <div class="card-art"><span class="card-fam">{FAMN[p['family']]}</span>{bottle(p['family'])}</div>
 <div class="card-body">
  <h3>{e(p['name'])}</h3>
  <p class="card-line">{e(p['line'])}</p>
  <p class="card-notes">{e(notes)}</p>
  <div class="card-foot">
   <span class="price">${META['priceGlass']:,} <small>JMD</small></span>
   <button class="btn btn-ghost btn-sm" data-quick-add data-id="{p['id']}" data-name="{e(p['name'])}" data-price="{META['priceGlass']}" style="position:relative;z-index:4">Add</button>
  </div>
 </div>
 <a class="stretch" href="/fragrance/{p['id']}/" aria-label="{e(p['name'])} — view details"></a>
</article>'''

# ================================================================ HOME
heroes = [p for p in P if p.get('hero')]
def build_home():
    fam_marquee = ' '.join(f'<span>{f["name"]}</span>' for f in FAM)
    marquee = f'<div class="marquee"><div class="marquee-track">{fam_marquee}{fam_marquee}</div></div>'
    hero_cards = ''.join(card(p, i+1) for i, p in enumerate(heroes[:4]))
    fam_tiles = ''.join(f'''<a class="card rv rv-d{i%4+1}" href="/collection/?family={f['id']}">
      <div class="card-art">{bottle(f['id'])}</div>
      <div class="card-body"><h3>{f['name']}</h3><p class="card-line">{e(f['blurb'])}</p>
      <div class="card-foot"><span class="ul">Explore</span></div></div></a>''' for i, f in enumerate(FAM))

    body = f'''
<main id="main">
<section class="hero">
 <div class="hero-glow"></div>{RINGS}
 <div class="wrap hero-in">
  <div class="hero-copy">
   <span class="eyebrow rv in">Kingston · Est. 2026</span>
   <h1 class="d1 rv in rv-d1">The House of<br><span class="gold-text">Caribbean Luxury</span></h1>
   <p class="hero-sub rv in rv-d2">Where luxury fuses with your aroma.</p>
   <div class="hero-cta rv in rv-d3">
    <a class="btn btn-gold" href="/collection/">Shop the collection</a>
    <a class="btn btn-ghost" href="/scent-luxe/">Discover Scent Luxe</a>
   </div>
   <div class="hero-meta rv in rv-d4">
    <div><b>{len(P)}</b><span>Fragrances</span></div>
    <div><b>7</b><span>Scent families</span></div>
    <div><b>876</b><span>Made in Jamaica</span></div>
   </div>
  </div>
  <div class="hero-art">{bottle('amber')}</div>
 </div>
 <div class="scroll-hint"><i></i><span>Scroll</span></div>
</section>

{marquee}

<section class="sec">
 <div class="wrap">
  <div class="sec-head split">
   <div><span class="eyebrow rv">The signatures</span><h2 class="d2 rv rv-d1">Six scents that built<br>the house</h2></div>
   <a class="ul rv rv-d2" href="/collection/">All {len(P)} fragrances</a>
  </div>
  <div class="grid g4">{hero_cards}</div>
 </div>
</section>

<section class="sec-sm"><div class="stats">
 <div class="stat rv"><b class="gold-text">{len(P)}</b><span>Fragrances in the house</span></div>
 <div class="stat rv rv-d1"><b class="gold-text">10ml</b><span>Concentrated parfum oil</span></div>
 <div class="stat rv rv-d2"><b class="gold-text">Free</b><span>Delivery in Kingston</span></div>
 <div class="stat rv rv-d3"><b class="gold-text">24+</b><span>Wholesale from</span></div>
</div></section>

<section class="sec">
 <div class="wrap split-feat">
  <div class="feat-art rv">{bottle('woods')}</div>
  <div>
   <span class="eyebrow rv">Why oil</span>
   <h2 class="d2 rv rv-d1">Concentration<br>over dilution</h2>
   <p class="lede rv rv-d2" style="margin-top:1.4rem">Most fragrance you buy is mostly alcohol — a bright opening that burns off by lunchtime. We work in concentrated parfum oil instead: no alcohol, no evaporation, no sting on the skin.</p>
   <p class="rv rv-d3 muted" style="margin-top:1.1rem;max-width:52ch">The result is a scent that sits closer, lasts longer through Caribbean heat and humidity, and develops on your skin rather than on the air around you. A little goes further, which is why a 10ml bottle outlasts a 50ml spray.</p>
   <div class="rv rv-d4" style="margin-top:2rem"><a class="btn btn-ghost" href="/the-house/">The house standard</a></div>
  </div>
 </div>
</section>

<section class="sec" style="background:var(--ink-2);border-block:1px solid var(--line-soft)">
 <div class="wrap">
  <div class="sec-head"><span class="eyebrow rv">Seven families</span><h2 class="d2 rv rv-d1">Find your register</h2></div>
  <div class="grid g4">{fam_tiles}</div>
 </div>
</section>

<section class="sec"><div class="wrap quote rv">
 <p>Caribbean culture is a<br><span class="gold-text italic">global export.</span></p>
 <cite>The house thesis</cite>
</div></section>

<section class="sec" style="padding-top:0">
 <div class="wrap">
  <div class="sec-head"><span class="eyebrow rv">The architecture</span>
   <h2 class="d2 rv rv-d1">One house. Three names.</h2>
   <p class="lede rv rv-d2">A deliberate ladder from fragrance to full lifestyle luxury.</p></div>
  <div class="tiers">
   <div class="tier tier--now rv">
    <h3 class="d4">Scent Fusion</h3><p class="tier-when">Available now</p>
    <p>The house collection — {len(P)} concentrated parfum oils across seven families, made and bottled in Kingston.</p>
    <ul><li>10ml glass &amp; plastic</li><li>Retail, wholesale &amp; consignment</li><li>Island-wide delivery</li></ul>
    <a class="ul" href="/collection/">Shop now</a></div>
   <div class="tier rv rv-d1">
    <h3 class="d4">Scent Luxe</h3><p class="tier-when">Q4 2026</p>
    <p>The prestige parfum house. Three hero eaux de parfum built with an established fragrance laboratory.</p>
    <ul><li>Jamaican pimento &amp; coffee blossom</li><li>Vetiver &amp; sea-salt accords</li><li>IFRA-compliant, luxury packaging</li></ul>
    <a class="ul" href="/scent-luxe/">Join the waitlist</a></div>
   <div class="tier rv rv-d2">
    <h3 class="d4">Pleasure &amp; S</h3><p class="tier-when">2028 — 2029</p>
    <p>Body, bath and home, then the monogram line — accessories, leather goods and limited editions.</p>
    <ul><li>Sensorial lifestyle range</li><li>First apparel capsule</li><li>Artist &amp; carnival collaborations</li></ul>
    <a class="ul" href="/the-house/">The expansion arc</a></div>
  </div>
 </div>
</section>

<section class="sec" style="background:linear-gradient(180deg,var(--ink),var(--ink-3))">
 <div class="wrap-narrow" data-center>
  <span class="eyebrow rv">Stock the house</span>
  <h2 class="d2 rv rv-d1">For boutiques, salons,<br>spas and resorts</h2>
  <p class="lede rv rv-d2" style="margin:1.4rem auto 2.4rem">Wholesale from 24 units with tiered pricing, or take the collection on consignment with no capital outlay. Partners across Kingston, the north coast and the diaspora.</p>
  <div class="rv rv-d3" style="display:flex;gap:.9rem;justify-content:center;flex-wrap:wrap">
   <a class="btn btn-gold" href="/partners/">Become a stockist</a>
   <a class="btn btn-ghost" href="/partners/#consignment">Consignment terms</a>
  </div>
 </div>
</section>
</main>'''
    schema = json.dumps({
      "@context":"https://schema.org","@type":"Organization","name":"Scent Fusion Jamaica",
      "url":SITE,"logo":SITE+"/assets/img/monogram-512.png",
      "description":"A Caribbean lifestyle house from Kingston, Jamaica. Concentrated parfum oils across seven scent families.",
      "address":{"@type":"PostalAddress","streetAddress":"39 Mansfield Avenue","addressLocality":"Kingston 20","addressCountry":"JM"},
      "sameAs":[f"https://instagram.com/{IG}"],
      "contactPoint":{"@type":"ContactPoint","telephone":"+1-876-253-5213","contactType":"sales","email":EMAIL}})
    w('index.html', page("Scent Fusion Jamaica — The House of Caribbean Luxury",
        "A Caribbean lifestyle house from Kingston. %d concentrated parfum oils across seven scent families. Free Kingston delivery, wholesale and consignment." % len(P),
        "/", body, '/', schema=schema))

# ================================================================ COLLECTION
def build_collection():
    fam_chips = ''.join(f'<button class="chip" data-filter="family" data-value="{f["id"]}">{f["name"]}</button>' for f in FAM)
    cards = ''.join(card(p, (i % 4) + 1) for i, p in enumerate(P))
    body = f'''
<main id="main" class="sec" style="padding-top:9rem">
 <div class="wrap">
  <div class="sec-head">
   <span class="eyebrow rv in">The collection</span>
   <h1 class="d2 rv in rv-d1">{len(P)} fragrances,<br>seven families</h1>
   <p class="lede rv in rv-d2">Concentrated parfum oil, 10ml. Free delivery in Kingston, island-wide courier available. Every scent is blended and bottled in Jamaica.</p>
  </div>
  <div class="filters rv in rv-d3">
   <button class="chip" data-filter="wear" data-value="all" aria-pressed="true">All</button>
   <button class="chip" data-filter="wear" data-value="women">Women</button>
   <button class="chip" data-filter="wear" data-value="men">Men</button>
   <button class="chip" data-filter="wear" data-value="unisex">Unisex</button>
   <div class="search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
    <input type="search" data-search placeholder="Search a scent or a note — vetiver, vanilla, oud…" aria-label="Search fragrances"></div>
  </div>
  <div class="filters rv in rv-d3" style="margin-top:-1.6rem">
   <button class="chip" data-filter="family" data-value="all" aria-pressed="true">All families</button>{fam_chips}
  </div>
  <p class="count"><span data-count>{len(P)} fragrances</span></p>
  <div class="grid g4" data-collection>{cards}</div>
  <p data-none style="display:none;text-align:center;padding:4rem 0;color:var(--smoke)">No fragrance matches that. Try another note or clear the filters.</p>
 </div>
</main>'''
    w('collection/index.html', page("The Collection — %d Fragrances | Scent Fusion Jamaica" % len(P),
       "Browse all %d Scent Fusion Jamaica parfum oils across seven scent families. Filter by women, men, unisex or scent note." % len(P),
       "/collection/", body, '/collection/', depth=1))

# ================================================================ PRODUCT PAGES
def build_products():
    for i, p in enumerate(P):
        rel = [x for x in P if x['family'] == p['family'] and x['id'] != p['id']][:4]
        if len(rel) < 4:
            rel += [x for x in P if x['id'] != p['id'] and x not in rel][:4-len(rel)]
        notes = p['notes']
        pyr = ''.join(f'<div class="pyr-row"><dt>{lbl}</dt><dd>{e(" · ".join(notes[k]))}</dd></div>'
                      for k, lbl in (('top','Top notes'),('heart','Heart'),('base','Base')))
        body = f'''
<main id="main" class="wrap">
 <div class="pdp" data-pdp="{p['id']}" data-name="{e(p['name'])}">
  <div class="pdp-art rv in">{bottle(p['family'])}</div>
  <div>
   <nav class="crumb rv in"><a href="/">Home</a> · <a href="/collection/">Collection</a> · <span>{e(p['name'])}</span></nav>
   <span class="eyebrow rv in">{FAMN[p['family']]} · {p['wear'].title()}</span>
   <h1 class="d2 rv in rv-d1">{e(p['name'])}</h1>
   <p class="hero-sub rv in rv-d1" style="margin:.8rem 0 1.6rem">{e(p['line'])}</p>
   <p class="lede rv in rv-d2">{e(p['copy'])}</p>
   <dl class="pyramid rv in rv-d2">{pyr}</dl>
   <div class="opts rv in rv-d3">
    <label class="opt"><input type="radio" name="variant" value="{META['priceGlass']}" data-label="Glass 10ml" checked>
     <span class="opt-name">Glass bottle — 10ml<em>Weighted glass, gold cap</em></span>
     <span class="opt-price">${META['priceGlass']:,}</span></label>
    <label class="opt"><input type="radio" name="variant" value="{META['pricePlastic']}" data-label="Roll-on 10ml">
     <span class="opt-name">Roll-on — 10ml<em>Travel-friendly, no spill</em></span>
     <span class="opt-price">${META['pricePlastic']:,}</span></label>
   </div>
   <div class="qty rv in rv-d3">
    <button data-qty-btn="-" aria-label="Decrease quantity">−</button>
    <span data-qty>1</span>
    <button data-qty-btn="+" aria-label="Increase quantity">+</button>
   </div>
   <div class="pdp-buy rv in rv-d4">
    <button class="btn btn-gold btn-block" data-add>Add to selection</button>
    <a class="btn btn-ghost btn-block" href="https://wa.me/{WA}?text={e('Hello Scent Fusion Jamaica — I would like to order ' + p['name'] + '.')}" target="_blank" rel="noopener">Ask about this scent</a>
   </div>
   <p class="small muted rv in rv-d4" style="margin-top:1.4rem">Free delivery in Kingston · island-wide courier available · wholesale from 24 units</p>
  </div>
 </div>

 <section class="sec">
  <div class="sec-head split"><h2 class="d3 rv">More in {FAMN[p['family']]}</h2><a class="ul rv" href="/collection/?family={p['family']}">See all</a></div>
  <div class="grid g4">{''.join(card(r, j+1) for j, r in enumerate(rel))}</div>
 </section>
</main>'''
        schema = json.dumps({
          "@context":"https://schema.org","@type":"Product","name":p['name'],
          "description":p['copy'],"brand":{"@type":"Brand","name":"Scent Fusion Jamaica"},
          "category":FAMN[p['family']],
          "offers":{"@type":"Offer","price":META['priceGlass'],"priceCurrency":"JMD",
                    "availability":"https://schema.org/InStock","url":f"{SITE}/fragrance/{p['id']}/"}})
        w(f"fragrance/{p['id']}/index.html", page(
            f"{p['name']} — {FAMN[p['family']]} Parfum Oil | Scent Fusion Jamaica",
            f"{p['line']} {' · '.join(notes['top'] + notes['base'])}. Concentrated parfum oil, 10ml. ${META['priceGlass']:,} JMD.",
            f"/fragrance/{p['id']}/", body, '/collection/', schema=schema, depth=2))

# ================================================================ SCENT LUXE
def build_luxe():
    body = f'''
<main id="main">
<section class="hero" style="min-height:82svh">
 <div class="hero-glow"></div>{RINGS}
 <div class="wrap hero-in">
  <div class="hero-copy">
   <span class="eyebrow rv in">The prestige house · Q4 2026</span>
   <h1 class="d1 rv in rv-d1"><span class="gold-text">Scent Luxe</span></h1>
   <p class="hero-sub rv in rv-d2">Three eaux de parfum. One island. Stories no European house can tell.</p>
   <div class="hero-cta rv in rv-d3"><a class="btn btn-gold" href="#waitlist">Join the waitlist</a>
    <a class="btn btn-ghost" href="/collection/">Shop available now</a></div>
  </div>
  <div class="hero-art">{bottle('citrus')}</div>
 </div>
</section>

<section class="sec">
 <div class="wrap-narrow">
  <span class="eyebrow rv">The brief</span>
  <h2 class="d2 rv rv-d1">Prestige craft,<br>island raw material</h2>
  <p class="lede rv rv-d2" style="margin-top:1.5rem">Prestige fragrance is booming and creatively homogenous. Niche houses multiply, but nearly all draw from the same European codes. Meanwhile Caribbean culture reaches billions of streams and four million visitors a year — with no luxury fragrance house of its own.</p>
  <p class="rv rv-d3 muted" style="margin-top:1.2rem">Scent Luxe is being formulated with an established fragrance laboratory to prestige standards: eau de parfum concentrations, IFRA-compliant, luxury-grade packaging. Built on materials that belong to this island — Jamaican pimento, coffee blossom from the Blue Mountains, vetiver, and sea-salt accords drawn from the south coast.</p>
 </div>
</section>

<section class="sec-sm"><div class="wrap"><div class="grid g3">
 <div class="tier rv"><h3 class="d4">Pimento</h3><p class="tier-when">Hero one</p>
  <p>The one spice the world took from Jamaica, built into a peppery, green-topped, leather-based parfum.</p></div>
 <div class="tier rv rv-d1"><h3 class="d4">Coffee Blossom</h3><p class="tier-when">Hero two</p>
  <p>Not the bean — the flower. Green, faintly bitter, jasmine-adjacent, set against Haitian vetiver.</p></div>
 <div class="tier rv rv-d2"><h3 class="d4">Sea Salt &amp; Vetiver</h3><p class="tier-when">Hero three</p>
  <p>Saline, mineral and dry. The Atlantic side of the island rendered at parfum concentration.</p></div>
</div></div></section>

<section class="sec" style="background:var(--ink-2);border-block:1px solid var(--line-soft)" id="waitlist">
 <div class="wrap-narrow" data-center>
  <div class="sec-head"><span class="eyebrow rv">Private list</span>
   <h2 class="d2 rv rv-d1">First access</h2>
   <p class="lede rv rv-d2" style="margin-inline:auto">The debut collection releases to the waitlist before anyone else, with a discovery set fully credited toward a full bottle.</p></div>
  <form class="form rv rv-d3" data-wa-form="Scent Luxe waitlist — please add me to the list.">
   <div class="row2">
    <div class="field"><label for="wl-name">Name</label><input id="wl-name" name="Name" required></div>
    <div class="field"><label for="wl-email">Email</label><input id="wl-email" name="Email" type="email" required></div>
   </div>
   <div class="field"><label for="wl-city">City</label><input id="wl-city" name="City" placeholder="Kingston, Miami, London…"></div>
   <div class="field"><label for="wl-pref">What do you usually wear?</label><input id="wl-pref" name="Usually wears" placeholder="Warm and heavy, fresh and clean, floral…"></div>
   <button class="btn btn-gold" type="submit">Join the waitlist</button>
   <p class="small muted" data-sent style="display:none">Opening WhatsApp to confirm your place — send the message and you are on the list.</p>
  </form>
 </div>
</section>
</main>'''
    w('scent-luxe/index.html', page("Scent Luxe — The Prestige Collection | Scent Fusion Jamaica",
      "Scent Luxe is the prestige parfum house of Scent Fusion Jamaica. Three hero eaux de parfum built on Jamaican pimento, coffee blossom and vetiver. Q4 2026.",
      "/scent-luxe/", body, '/scent-luxe/', depth=1))

# ================================================================ THE HOUSE
def build_house():
    body = f'''
<main id="main">
<section class="sec" style="padding-top:9rem">
 <div class="wrap-narrow">
  <span class="eyebrow rv in">The house</span>
  <h1 class="d2 rv in rv-d1">Culture without<br>a house — <span class="gold-text italic">until now</span></h1>
  <p class="lede rv in rv-d2" style="margin-top:1.6rem">Caribbean aesthetics drive global music, fashion and travel. Reggae and dancehall reach billions of streams a year. Four million visitors come to Jamaica annually. Eight million people of Caribbean heritage live in North America and the UK.</p>
  <p class="rv in rv-d3 muted" style="margin-top:1.2rem">And not one globally distributed luxury fragrance house belongs to any of it. The culture is exported constantly and owned almost never. Scent Fusion Jamaica exists to close that gap — starting with fragrance, because it is the highest-margin, most capital-efficient door into a full lifestyle house.</p>
 </div>
</section>

<section class="sec-sm"><div class="stats">
 <div class="stat rv"><b class="gold-text">4M+</b><span>Annual visitors to Jamaica</span></div>
 <div class="stat rv rv-d1"><b class="gold-text">8M+</b><span>Caribbean-heritage consumers abroad</span></div>
 <div class="stat rv rv-d2"><b class="gold-text">Zero</b><span>Caribbean luxury fragrance houses</span></div>
 <div class="stat rv rv-d3"><b class="gold-text">2026</b><span>The year that changes</span></div>
</div></section>

<section class="sec">
 <div class="wrap split-feat">
  <div class="feat-art rv">{bottle('spice')}</div>
  <div>
   <span class="eyebrow rv">The founder</span>
   <h2 class="d2 rv rv-d1">Jamaal Isaacs</h2>
   <p class="small rv rv-d1" style="color:var(--gold);letter-spacing:.2em;text-transform:uppercase;margin-top:.6rem">Founder &amp; Chief Executive · Kingston</p>
   <p class="lede rv rv-d2" style="margin-top:1.4rem">Two decades building consumer ventures across Kingston — retail distribution, import and wholesale trade, events and entertainment promotion.</p>
   <p class="rv rv-d3 muted" style="margin-top:1.1rem">He became the first importer and distributor of fine fragrance oils in Jamaica in 2015, and built the ambassador-style direct-sales networks that moved premium goods from street-level demand onto retail shelves. Consumer brands die on distribution, not product. Scent Fusion gives a proven distribution operator a luxury vessel.</p>
  </div>
 </div>
</section>

<section class="sec" style="background:var(--ink-2);border-block:1px solid var(--line-soft)">
 <div class="wrap">
  <div class="sec-head"><span class="eyebrow rv">The expansion arc</span>
   <h2 class="d2 rv rv-d1">Fragrance → Lifestyle → Luxury</h2>
   <p class="lede rv rv-d2">Fragrance is the wedge. The house is the destination.</p></div>
  <div class="tiers">
   <div class="tier tier--now rv"><h3 class="d4">Phase One</h3><p class="tier-when">2026 — 2027</p>
    <ul><li>House collection of {len(P)} parfum oils</li><li>Scent Luxe debut — three hero EDPs</li><li>Discovery-set funnel</li><li>Kingston flagship &amp; tourism retail</li></ul></div>
   <div class="tier rv rv-d1"><h3 class="d4">Phase Two</h3><p class="tier-when">2028</p>
    <ul><li>Pleasure — body, bath &amp; home</li><li>First apparel capsule</li><li>Diaspora city expansion</li><li>Boutique &amp; resort-spa wholesale</li></ul></div>
   <div class="tier rv rv-d2"><h3 class="d4">Phase Three</h3><p class="tier-when">2029 +</p>
    <ul><li>S — the monogram line</li><li>Leather goods &amp; limited editions</li><li>Artist &amp; carnival collaborations</li><li>Specialty &amp; travel retail scale</li></ul></div>
  </div>
 </div>
</section>

<section class="sec"><div class="wrap quote rv">
 <p>Our origin is <span class="gold-text italic">lived,</span><br>not moodboarded.</p><cite>The house standard</cite>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap-narrow" data-center>
 <h2 class="d3 rv">Work with the house</h2>
 <p class="lede rv rv-d1" style="margin:1.2rem auto 2rem">Stockists, distributors, collaborators and press.</p>
 <div class="rv rv-d2" style="display:flex;gap:.9rem;justify-content:center;flex-wrap:wrap">
  <a class="btn btn-gold" href="/partners/">Partner with us</a>
  <a class="btn btn-ghost" href="/contact/">Get in touch</a></div>
</div></section>
</main>'''
    w('the-house/index.html', page("The House — Our Story | Scent Fusion Jamaica",
      "Caribbean culture is a global export with no luxury house of its own. The story of Scent Fusion Jamaica and its arc from fragrance to lifestyle luxury.",
      "/the-house/", body, '/the-house/', depth=1))

# ================================================================ PARTNERS
def build_partners():
    body = f'''
<main id="main">
<section class="sec" style="padding-top:9rem">
 <div class="wrap-narrow">
  <span class="eyebrow rv in">Stockists &amp; partners</span>
  <h1 class="d2 rv in rv-d1">Carry the house</h1>
  <p class="lede rv in rv-d2" style="margin-top:1.5rem">Boutiques, salons, barbershops, spas, resort shops and gift stores across Jamaica and the diaspora. Buy wholesale, or take the collection on consignment with no capital outlay.</p>
 </div>
</section>

<section class="sec-sm"><div class="wrap">
 <div class="sec-head"><span class="eyebrow rv">Wholesale</span><h2 class="d3 rv rv-d1">Tiered pricing</h2></div>
 <div class="tbl-wrap rv rv-d2"><table class="tbl">
  <thead><tr><th>Tier</th><th>Units per order</th><th>Discount</th><th>Your cost / unit</th><th>Suggested retail</th></tr></thead>
  <tbody>
   <tr><td>Tier 1</td><td>24 — 49</td><td>—</td><td>$1,600 JMD</td><td>$3,600 JMD</td></tr>
   <tr><td>Tier 2</td><td>50 — 199</td><td>10% off</td><td>$1,440 JMD</td><td>$3,600 JMD</td></tr>
   <tr><td>Bulk</td><td>200 +</td><td>18% off</td><td>$1,312 JMD</td><td>$3,600 JMD</td></tr>
  </tbody></table></div>
 <div class="grid g3" style="margin-top:1.6rem">
  <div class="note-box rv"><p class="tiny" style="margin:0 0 .5rem">Minimum order</p><p class="small muted" style="margin:0">24 units per wholesale order, mixed across any scents in the collection.</p></div>
  <div class="note-box rv rv-d1"><p class="tiny" style="margin:0 0 .5rem">Payment</p><p class="small muted" style="margin:0">50% deposit on confirmation, balance before dispatch. Bank transfer (NCB / BNS), online transfer or direct deposit.</p></div>
  <div class="note-box rv rv-d2"><p class="tiny" style="margin:0 0 .5rem">Fulfilment</p><p class="small muted" style="margin:0">3—5 business days after deposit confirmation. Courier or local pickup.</p></div>
 </div>
</div></section>

<section class="sec" id="consignment" style="background:var(--ink-2);border-block:1px solid var(--line-soft)">
 <div class="wrap split-feat">
  <div>
   <span class="eyebrow rv">Consignment</span>
   <h2 class="d2 rv rv-d1">Stock it.<br>Pay when it sells.</h2>
   <p class="lede rv rv-d2" style="margin-top:1.4rem">No capital outlay, no dead stock risk on your books. We place the collection with you, you keep 25% of every bottle sold, and we reconcile on an agreed cycle.</p>
   <ul class="rv rv-d3" style="list-style:none;padding:0;margin:1.8rem 0;display:grid;gap:.8rem">
    <li class="small" style="padding-left:1.3rem;position:relative"><span style="position:absolute;left:0;color:var(--gold)">—</span> Retail $3,600 JMD · you keep $900 per bottle</li>
    <li class="small" style="padding-left:1.3rem;position:relative"><span style="position:absolute;left:0;color:var(--gold)">—</span> Stock remains house property until sold</li>
    <li class="small" style="padding-left:1.3rem;position:relative"><span style="position:absolute;left:0;color:var(--gold)">—</span> Inventory schedule issued with every placement</li>
    <li class="small" style="padding-left:1.3rem;position:relative"><span style="position:absolute;left:0;color:var(--gold)">—</span> Display materials and staff training provided</li>
   </ul>
   <a class="btn btn-ghost rv rv-d3" href="#enquire">Request the agreement</a>
  </div>
  <div class="feat-art rv">{bottle('gourmand')}</div>
 </div>
</section>

<section class="sec" id="enquire"><div class="wrap-narrow" data-center>
 <div class="sec-head"><span class="eyebrow rv">Enquire</span>
  <h2 class="d2 rv rv-d1">Open a trade account</h2>
  <p class="lede rv rv-d2" style="margin-inline:auto">Tell us about your business and we will send pricing, the order form and the consignment agreement.</p></div>
 <form class="form rv rv-d3" data-wa-form="TRADE ENQUIRY — Scent Fusion Jamaica">
  <div class="row2">
   <div class="field"><label for="p-biz">Business name</label><input id="p-biz" name="Business" required></div>
   <div class="field"><label for="p-name">Contact person</label><input id="p-name" name="Contact" required></div>
  </div>
  <div class="row2">
   <div class="field"><label for="p-phone">Phone / WhatsApp</label><input id="p-phone" name="Phone" required></div>
   <div class="field"><label for="p-email">Email</label><input id="p-email" name="Email" type="email"></div>
  </div>
  <div class="field"><label for="p-loc">Location</label><input id="p-loc" name="Location" placeholder="Parish, town or city"></div>
  <div class="row2">
   <div class="field"><label for="p-type">Business type</label><select id="p-type" name="Business type">
    <option>Boutique</option><option>Salon / barbershop</option><option>Spa</option><option>Resort or hotel shop</option>
    <option>Gift shop</option><option>Pharmacy / convenience</option><option>Online reseller</option><option>Distributor</option><option>Other</option>
   </select></div>
   <div class="field"><label for="p-model">Preferred model</label><select id="p-model" name="Preferred model">
    <option>Wholesale purchase</option><option>Consignment</option><option>Not sure — advise me</option>
   </select></div>
  </div>
  <div class="field"><label for="p-msg">Anything else</label><textarea id="p-msg" name="Notes" placeholder="Volumes you have in mind, scents your customers ask for, timelines…"></textarea></div>
  <button class="btn btn-gold" type="submit">Send enquiry</button>
  <p class="small muted" data-sent style="display:none">Opening WhatsApp — send the message and we will reply with full trade terms.</p>
 </form>
</div></section>
</main>'''
    w('partners/index.html', page("Wholesale & Consignment for Stockists | Scent Fusion Jamaica",
      "Stock Scent Fusion Jamaica. Wholesale from 24 units with tiered pricing to 18% off, or consignment with no capital outlay and 25% to the retailer.",
      "/partners/", body, '/partners/', depth=1))

# ================================================================ CONTACT
def build_contact():
    body = f'''
<main id="main">
<section class="sec" style="padding-top:9rem"><div class="wrap">
 <div class="sec-head"><span class="eyebrow rv in">Contact</span>
  <h1 class="d2 rv in rv-d1">Talk to the house</h1></div>
 <div class="split-feat">
  <div>
   <form class="form rv in rv-d2" data-wa-form="ENQUIRY — Scent Fusion Jamaica">
    <div class="row2">
     <div class="field"><label for="c-name">Name</label><input id="c-name" name="Name" required></div>
     <div class="field"><label for="c-phone">Phone / WhatsApp</label><input id="c-phone" name="Phone"></div>
    </div>
    <div class="field"><label for="c-email">Email</label><input id="c-email" name="Email" type="email"></div>
    <div class="field"><label for="c-sub">Subject</label><select id="c-sub" name="Subject">
     <option>An order</option><option>Finding the right scent</option><option>Wholesale or consignment</option>
     <option>Scent Luxe waitlist</option><option>Press or collaboration</option><option>Investment enquiry</option><option>Something else</option>
    </select></div>
    <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="Message" required></textarea></div>
    <button class="btn btn-gold" type="submit">Send message</button>
    <p class="small muted" data-sent style="display:none">Opening WhatsApp — send the message and we will come back to you.</p>
   </form>
  </div>
  <div class="rv in rv-d3">
   <div class="note-box" style="margin-bottom:1.2rem">
    <p class="tiny" style="margin:0 0 .6rem">Fastest reply</p>
    <a class="d4" style="font-family:var(--display);color:var(--gold)" href="https://wa.me/{WA}" target="_blank" rel="noopener">+1 (876) 253-5213</a>
    <p class="small muted" style="margin:.5rem 0 0">WhatsApp, 9am — 8pm Jamaica time</p>
   </div>
   <div class="note-box" style="margin-bottom:1.2rem">
    <p class="tiny" style="margin:0 0 .6rem">Email</p>
    <a class="small" style="color:var(--champagne)" href="mailto:{EMAIL}">{EMAIL}</a>
   </div>
   <div class="note-box" style="margin-bottom:1.2rem">
    <p class="tiny" style="margin:0 0 .6rem">Instagram</p>
    <a class="small" style="color:var(--champagne)" href="https://instagram.com/{IG}" target="_blank" rel="noopener">@{IG}</a>
   </div>
   <div class="note-box">
    <p class="tiny" style="margin:0 0 .6rem">The house</p>
    <p class="small muted" style="margin:0">39 Mansfield Avenue<br>Kingston 20, Jamaica</p>
   </div>
  </div>
 </div>
</div></section>
</main>'''
    w('contact/index.html', page("Contact | Scent Fusion Jamaica",
      "Reach Scent Fusion Jamaica by WhatsApp, email or Instagram. Orders, wholesale, consignment, press and investment enquiries.",
      "/contact/", body, '/contact/', depth=1))

# ================================================================ LEGAL + 404
LEGAL = {
 'privacy': ("Privacy Policy", """
<h2 class="d3">What we collect</h2>
<p>When you place an order, join a waitlist or send an enquiry through this site, the details you type are passed directly into a WhatsApp message or an email that you choose to send. Nothing is stored on this website — it has no database and no server that receives form data.</p>
<h2 class="d3">Your selection</h2>
<p>The bottles you add to your selection are saved in your own browser so the list survives a refresh. That data never leaves your device and we cannot see it.</p>
<h2 class="d3">What we hold once you contact us</h2>
<p>Once you message us, we hold your name, contact details, delivery address and order history for as long as needed to fulfil orders and meet Jamaican record-keeping requirements. We do not sell, rent or share your details with third parties.</p>
<h2 class="d3">Third parties</h2>
<p>Fonts are served by Google Fonts. Payments, where taken by card, are handled by our payment provider on their own secure pages — we never see or store your card number.</p>
<h2 class="d3">Your rights</h2>
<p>Ask us at any time for a copy of what we hold about you, or ask us to delete it. Write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>"""),

 'terms': ("Terms of Sale", """
<h2 class="d3">Products</h2>
<p>Scent Fusion Jamaica sells its own concentrated parfum oils. Every fragrance in this collection is an original Scent Fusion composition, named and blended by the house. We do not sell, copy or claim any association with any other fragrance brand, and no third-party trade mark is used to describe our products.</p>
<h2 class="d3">Prices</h2>
<p>All prices are in Jamaican dollars and include applicable taxes unless stated otherwise. We may change prices at any time; the price confirmed at the point of order is the price you pay.</p>
<h2 class="d3">Orders</h2>
<p>An order is confirmed when we acknowledge it by WhatsApp, email or written invoice. We may decline any order.</p>
<h2 class="d3">Wholesale and consignment</h2>
<p>Trade orders are governed by our wholesale order form or retail consignment agreement, which take precedence over these terms where they conflict.</p>
<h2 class="d3">Skin and safety</h2>
<p>Our oils are for external use on skin and clothing. Patch test before first use. Discontinue if irritation occurs. Keep away from eyes, out of reach of children, and away from direct heat and sunlight. If you are pregnant or have sensitive skin, seek advice before use.</p>
<h2 class="d3">Governing law</h2>
<p>These terms are governed by the laws of Jamaica.</p>"""),

 'shipping': ("Delivery &amp; Returns", """
<h2 class="d3">Delivery</h2>
<p>Free delivery within Kingston and St Andrew. Island-wide delivery by courier at the customer's expense, quoted at the time of order. Standard turnaround is 1—3 business days in Kingston and 2—5 business days island-wide.</p>
<h2 class="d3">Collection</h2>
<p>Local pickup can be arranged in Kingston 20 by appointment.</p>
<h2 class="d3">International</h2>
<p>We ship to the diaspora on request. Message us with your destination for a quote and timeline. Duties and import charges are the customer's responsibility.</p>
<h2 class="d3">Returns</h2>
<p>For hygiene reasons we cannot accept returns on opened fragrance. If a bottle arrives damaged, leaking or incorrect, contact us within 48 hours of delivery with a photograph and we will replace it or refund it in full.</p>
<h2 class="d3">Wholesale returns</h2>
<p>Trade returns are handled under the wholesale order form or consignment agreement in force.</p>"""),
}

def build_legal():
    for slug, (title, content) in LEGAL.items():
        body = f'''
<main id="main" class="sec" style="padding-top:9rem"><div class="wrap-narrow">
 <nav class="crumb"><a href="/">Home</a> · <span>{title}</span></nav>
 <h1 class="d2 rv in">{title}</h1>
 <div class="lede rv in rv-d1" style="margin-top:2rem">{content.format(EMAIL=EMAIL)}</div>
 <p class="small muted" style="margin-top:3rem">Last updated September 2026. Scent Fusion Jamaica Ltd., 39 Mansfield Avenue, Kingston 20, Jamaica.</p>
</div></main>'''
        body = body.replace('<h2 class="d3">', '<h2 class="d3" style="margin:2.4rem 0 .8rem;color:var(--champagne)">')
        w(f'legal/{slug}/index.html', page(f"{re.sub('&amp;','&',title)} | Scent Fusion Jamaica",
          f"{re.sub(chr(38)+chr(97)+chr(109)+chr(112)+chr(59),chr(38),title)} for Scent Fusion Jamaica Ltd. — a Caribbean lifestyle house based in Kingston, Jamaica. Orders, delivery, wholesale and consignment.", f"/legal/{slug}/", body, depth=2))

def build_404():
    body = f'''
<main id="main" class="sec" style="padding-top:11rem;min-height:70svh;display:grid;place-items:center;text-align:center">
 <div class="wrap-narrow">
  <span class="eyebrow">404</span>
  <h1 class="d2">That scent has<br><span class="gold-text italic">drifted away</span></h1>
  <p class="lede" style="margin:1.4rem auto 2.2rem">The page you were looking for is not here — but {len(P)} fragrances are.</p>
  <div style="display:flex;gap:.9rem;justify-content:center;flex-wrap:wrap">
   <a class="btn btn-gold" href="/collection/">Browse the collection</a>
   <a class="btn btn-ghost" href="/">Return home</a></div>
 </div>
</main>'''
    w('404.html', page("Page not found | Scent Fusion Jamaica", "That page has drifted away. Browse the Scent Fusion Jamaica collection — %d concentrated parfum oils across seven scent families, made in Kingston." % len(P), "/404.html", body, absolute=True))

# ================================================================ SEO files
def build_seo():
    urls = ['/', '/collection/', '/scent-luxe/', '/the-house/', '/partners/', '/contact/',
            '/legal/privacy/', '/legal/terms/', '/legal/shipping/'] + [f"/fragrance/{p['id']}/" for p in P]
    items = ''.join(
        f'<url><loc>{SITE}{u}</loc><changefreq>{"weekly" if u in ("/", "/collection/") else "monthly"}</changefreq>'
        f'<priority>{"1.0" if u=="/" else "0.9" if u=="/collection/" else "0.7"}</priority></url>' for u in urls)
    w('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>')
    w('robots.txt', f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    w('CNAME', 'scentfusionja.com\n')
    w('.nojekyll', '')


# ---------------------------------------------------------------- guard
BANNED = ("dior","chanel","ysl","saint laurent","prada","gucci","versace","creed","aventus",
 "byredo","le labo","tom ford","gaultier","givenchy","burberry","lattafa","marc jacobs",
 "armani","valentino","bvlgari","azzaro","louis vuitton","jimmy choo","carolina herrera",
 "michael kors","tory burch","juicy couture","flowerbomb","olympea","invictus","sauvage",
 "baccarat","rihanna","kardashian","victoria's secret","paris hilton","perry ellis",
 "hennessy","clive christian","erba pura","kayali","xerjoff","maison francis","red stripe",
 "black opium","good girl","la vie est belle","miss dior","light blue","mojave ghost")

def guard_check():
    """Fail the build if any third-party mark appears in the catalogue."""
    blob = json.dumps(DATA).lower()
    hits = sorted({b for b in BANNED if b in blob})
    if hits:
        raise SystemExit("BUILD BLOCKED — third-party marks found in data/collection.json: "
                         + ", ".join(hits) + "\nRename them before shipping.")
    print("Trade-mark guard: clean.")

if __name__ == '__main__':
    guard_check()
    for d in ('collection','fragrance','scent-luxe','the-house','partners','contact','legal'):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)
    build_home(); build_collection(); build_products(); build_luxe()
    build_house(); build_partners(); build_contact(); build_legal(); build_404(); build_seo()
    n = sum(len(f) for _,_,f in os.walk(ROOT) if '.git' not in _)
    print(f"Built {len(P)} product pages + 9 core pages.")
