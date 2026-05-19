# robotics.nullsetlabs.org

A sibling subdomain to `research.nullsetlabs.org` and `vex.nullsetlabs.org`. The page is intentionally minimal: it marks the surface, links out to the lab's active robotics work, and holds space for additional robotics projects to be documented as they become ready for public release.

## What's in this folder

```
robotics-subdomain/
  index.html              Robotics overview / placeholder.
  README.md               This file.
```

Single, self-contained HTML file with inline CSS. No build step. External dependencies: Google Fonts (Newsreader, Inter, JetBrains Mono) and the shared favicon hosted at `nullsetlabs.org/brand-assets/favicons/`.

## Where this deploys

- Target: Cloudflare Pages.
- Bound to: `robotics.nullsetlabs.org`.
- Single-page site for now; subpath pages get added as projects mature (for example, `robotics.nullsetlabs.org/artemis/` when the NASA Artemis documentation is ready).

Cloudflare Pages serves `index.html` from the root automatically. No additional routing configuration is required.

## Deployment notes

- The Cloudflare Web Analytics snippet is included as a commented-out placeholder. Replace `TBD-ROBOTICS-TOKEN` with the token issued for `robotics.nullsetlabs.org` and uncomment the script block when the property is registered.
- The GA4 measurement ID `G-R1S9F2Z4HS` is the same one used across the umbrella and every Null Set Labs subdomain. GA4 reports the subdomain hostname as a separate hostname, so robotics traffic remains attributable within the shared property.
- Open Graph preview is referenced at `robotics.nullsetlabs.org/og-preview.png`. Generate it from `brand-assets/social/og-preview.svg` on the umbrella site and place it at the deployment root.
- Favicons load from `nullsetlabs.org/brand-assets/favicons/` so a single source of truth serves every surface.

## Versioning architecture pattern

Per `BRAND_PRINCIPLES.md` (section: Versioning and Archive Architecture), once a robotics project produces public-release artifacts, it gets a dedicated subpath under `robotics.nullsetlabs.org/<project-slug>/` with its own Versions row at the bottom. The current bare path continues to serve "this year." Prior years move under versioned subpaths:

```
robotics.nullsetlabs.org/artemis/         current canonical artemis page
robotics.nullsetlabs.org/artemis/2025/    2025 artemis archive once a 2026 update lands
```

The pattern mirrors the research subdomain and the VEX hub so the lab's archive grows consistently across surfaces.

## Open items / pending work

- Replace `TBD-ROBOTICS-TOKEN` with the real Cloudflare Web Analytics token once the property is registered, and uncomment the snippet.
- Generate `og-preview.png` for the robotics page from the OG template.
- NASA Artemis (2025): documentation is not yet ready for public posting. When it is, this page gets:
  - A project subpath at `robotics.nullsetlabs.org/artemis/` with the full project page (hero, overview, approach, status, versions footer, footer).
  - The placeholder card on this index becomes a working link to the subpath, with the status pill changed from "In Preparation" to whatever fits at the time of release.
- As additional robotics projects come online (beyond VEX and Artemis), each gets its own card on this index and its own subpath, following the research subdomain's "copy, edit, link" pattern.

## Pre-publication discretion

This subdomain follows the rule documented in `BRAND_PRINCIPLES.md`. The Artemis card on the index describes the 2025 work at the highest level only. Methodology, results, collaborators, and institutional acknowledgements stay off the public surface until the documentation is finalized and the relevant permissions are in place.
