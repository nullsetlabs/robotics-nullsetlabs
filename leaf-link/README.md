# LEAF-Link, Null Set Labs

Single-page swipeable card presentation for the Null Set Labs LEAF-Link concept. Lives at `robotics.nullsetlabs.org/leaf-link/`.

## What this is

A polished, mission-page-style introduction to LEAF-Link, the lab's concept for forecasting plant stress in NASA's LEAF lunar plant biology payload. Designed to be shareable with faculty, mission scientists, college admissions readers, and journalists.

The page frames the work using the Null Set Labs five-question research structure:

1. What is the issue we are addressing?
2. What is the source of data?
3. What is the analysis method?
4. How are we solving it?
5. What does this mean for the scientific community?

## Deployment

The page is a single self-contained `index.html`. No build step. Drop it into the robotics subdomain at the `/leaf-link/` path.

For Cloudflare Pages or similar static hosting:

1. Place `index.html` at `/leaf-link/index.html` inside the robotics subdomain.
2. Confirm the canonical URL `https://robotics.nullsetlabs.org/leaf-link/` resolves.
3. Register the Cloudflare Web Analytics token for the robotics subdomain and uncomment the snippet near the bottom of the file, replacing `TBD-ROBOTICS-TOKEN`.
4. Generate `og-preview.png` at 1200x630 and save next to `index.html` so social previews work.

## What's on the page

Seven swipeable cards:

1. Title card with stylized leaf-in-lattice mark, framing the work as a deeper dive into NASA's LEAF lunar plant biology payload
2. The Issue: visible symptoms trail molecular damage, plus the three LEAF species (Arabidopsis thaliana, Brassica rapa, Lemna duckweed), plus working links to NASA mission resources
3. Source of Data: NASA's Open Science Data Repository (OSDR), with working links to osdr.nasa.gov and the NASA Science about-OSDR page
4. Analysis Method: four threads (PCA, ecotype stratification, telemetry-to-stress mapping, closed-loop control simulation)
5. How We Are Solving It: the LEAF-Link concept itself as a forward-looking stress score that sits alongside habitat control software
6. What This Means: two-panel impact card (lunar agriculture and Earth controlled-environment agriculture)
7. Collaborators welcome: short, inviting close card with a single research@nullsetlabs.org contact pill

## External links included and verified

- `https://osdr.nasa.gov/` (NASA Open Science Data Repository)
- `https://science.nasa.gov/biological-physical/data/osdr/` (About OSDR on NASA Science)
- `https://science.nasa.gov/biological-physical/space-crops/` (NASA Space Crops, the public LEAF context page)
- `https://www.nasa.gov/news-release/nasa-selects-first-lunar-instruments-for-artemis-astronaut-deployment/` (NASA's instrument selection announcement, naming LEAF)
- `https://www.nasa.gov/humans-in-space/artemis/` (NASA Artemis program overview)

All URLs verified via web search ahead of publication. No mission dates are stated on the page.

## Interaction

- Touch swipe on mobile (left/right)
- Arrow keys, Page Up/Down, Home, End on desktop
- Mouse wheel on desktop (advances cards when active card is fully scrolled)
- Dot indicators clickable to jump
- Prev/next buttons at the bottom
- GA4 event `leaf_link_slide_view` fires on each slide change with `slide_index` and `slide_total`

## Discretion compliance

Built against `WORKING_PRINCIPLES.md` and `BRAND_PRINCIPLES.md` (Pre-Publication Discretion section). The page is restricted to content already present in the public Concept brief:

- No mention of patent activity, IP language, NDAs, or proprietary framing
- No specific NASA OSDR dataset IDs or study identifiers
- No specific architectural or model-component details
- No faculty names, institutions, or specific collaborator references
- No specific mission dates
- Card 4 carries an explicit discretion note so the absence of architecture detail is intentional and readable

## Voice and framing

- Inventor profile card removed. The lab About page on nullsetlabs.org carries founder background. Project pages stay on the science.
- "High school" framing replaced with "exploring," "a deeper dive into," "investigating," and "the lab" voice.
- Closing card is a short, inviting call for collaborators rather than a build-journey timeline.
- Third-person institutional voice throughout ("the lab," "Null Set Labs").

## Brand alignment

- Same nav, footer, glyph treatment, and palette as the umbrella site
- Same font stack: Newsreader (headlines), Inter (UI/body), JetBrains Mono (labels)
- Cosmic backdrop layer (radial gradients plus low-opacity SVG star field) for space register
- GA4 shared property `G-R1S9F2Z4HS`

## Writing constraints respected

- Zero em-dash characters (U+2014)
- No consultant phrasing (no leverage, no stakeholder, no value proposition, no synergy)
- Short, active sentences
- Newsreader for headlines, Inter for body, JetBrains Mono for labels and resource links

## Version log

| Version | Date | Notes |
|---|---|---|
| v1.0 | 2026-05-18 | Initial 8-card build. Title, Problem, Concept, Approach, Mission, Inventor, Status, Closing. |
| v2.0 | 2026-05-18 | Restructured to seven cards around the lab's five research questions. Removed the inventor profile card and the build-journey status card. Reduced "high school" framing to zero on this page. Added verified working links to NASA OSDR, NASA Space Crops, the NASA Artemis instruments announcement, and the NASA Artemis program page. |

## Next steps

- Generate the OG preview PNG (template: `brand-assets/social/og-preview.svg` on the umbrella site)
- Register Cloudflare Web Analytics token and uncomment the snippet
