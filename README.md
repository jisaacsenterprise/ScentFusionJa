# scentfusionja.com

The web presence for **Scent Fusion Jamaica Ltd.** — a Caribbean lifestyle house based in Kingston.

Static site. No frameworks, no npm, no build tooling beyond Python 3 (standard library only).
Hosted on GitHub Pages, DNS on Cloudflare, domain registered at Namecheap.

---

## How it works

Everything is generated from two files:

| File | What it controls |
|---|---|
| `data/collection.json` | Every fragrance, price, scent family and description |
| `assets/js/config.js` | WhatsApp number, email, Instagram, card-checkout link |

`build.py` reads them and writes the HTML. Run it after any change:

```bash
python3 build.py
```

That regenerates 59 product pages plus the 9 core pages, the sitemap and robots.txt.
GitHub Actions runs the same command on every push to `main`, so in practice you just commit.

## Making changes

**Change a price** — edit `meta.priceGlass` / `meta.pricePlastic` in `data/collection.json`. One edit updates every page.

**Add a fragrance** — copy any block in the `products` array, change the fields, rebuild.
`id` becomes the URL (`/fragrance/<id>/`), so use lowercase and hyphens.

**Change the WhatsApp number or email** — `assets/js/config.js` for the ordering flow,
and the constants at the top of `build.py` for the pages themselves.

**Switch on card payments** — put your payment link in `checkoutUrl` in `assets/js/config.js`.
Until then, "Pay by card" stays hidden and WhatsApp ordering handles every order.

## Local preview

```bash
python3 build.py && python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Structure

```
index.html              House homepage
collection/             All 59 fragrances, filterable
fragrance/<id>/         One page per scent (generated)
scent-luxe/             Prestige collection + waitlist
the-house/              Story, founder, expansion arc
partners/               Wholesale tiers + consignment + trade enquiry
contact/                Contact form
legal/                  Privacy, terms, delivery & returns
assets/                 CSS, JS, images
data/collection.json    The catalogue
build.py                The generator
```

## A note on product naming

Every fragrance in this collection carries an original Scent Fusion name and its own
olfactory description. No third-party trade mark appears anywhere on this site, in the
source, or in the metadata. Keep it that way — it protects the company from trade mark
claims, keeps payment processors comfortable, and is what allows the house to be stocked
by resorts, duty-free operators and boutiques.

---

© Scent Fusion Jamaica Ltd.
