# LEAF-Link, Null Set Labs

Project page for LEAF-Link at `robotics.nullsetlabs.org/leaf-link/`: a completed concept study on forecasting plant stress for NASA's LEAF lunar plant payload. Independent research by Arjun, Null Set Labs, April to October 2026.

## Status

Completed, October 2026. The study is closed and will not be extended by the lab. The patent route considered in April 2026 was not pursued, so the methods, results and code are published in full.

## What the page contains

A single static `index.html` in the lab's project-page layout (nav, breadcrumb, hero, sections, versions row, footer):

1. Summary: question, data, three findings, conclusion
2. Background: the LEAF payload (cited) and the LEAF-Link design
3. Data: NASA OSDR study OSD-37
4. Methods: four analyses
5. Results: four figures and three stat tiles
6. Conclusions
7. Limitations
8. Status and materials, references, versions

The figures are drawn in the browser from JSON embedded in the page, at the width of the screen, so labels stay readable on phones. Each figure has a "Show the numbers" table, so every value is readable without the chart. Chart colors were checked as a set for color-vision deficiency on the dark surface, and flight and ground samples also differ in shape (circle and diamond).

## Updating the numbers

The numbers come from `analysis/results/*.json` (see `analysis/README.md`). If the analysis is re-run, regenerate the page so the text, tables and charts stay in agreement.

## External sources cited

- NASA news release, March 26, 2024, selecting LEAF for Artemis astronaut deployment
- Waite Research Institute, University of Adelaide, April 7, 2024, naming the LEAF plant species (Arabidopsis thaliana, red and green Brassica rapa, Wolffia duckweed)
- NASA Open Science Data Repository, OSD-37
- Choi et al., American Journal of Botany, 2019, doi:10.1002/ajb2.1223

No mission dates are stated on the page, because Artemis schedules change.

## Writing rules

- Credit Arjun by first name only; no collaborator or faculty names (the work was independent)
- Zero em-dash characters (U+2014); no exclamation points or emoji
- Plain, factual headings

## Version log

| Version | Date | Notes |
|---|---|---|
| 1.0 | October 2026 | Concept study completed: four analyses, figures, code and results published. Replaces the May 2026 slide-style concept overview. Corrects the LEAF duckweed genus to Wolffia. |
| 0.1 | May 2026 | Concept overview page (seven swipeable cards). |
