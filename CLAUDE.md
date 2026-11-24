# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal academic homepage for Valentin Klotzbücher, built with [Quarto](https://quarto.org/). The site is published with GitHub Pages at https://valentinklotzbuecher.github.io. Until November 2026 it was published to Quarto Pub (https://valentink.quarto.pub/home), which stops accepting updates at the end of 2026.

This repository is public. Keep out of it, and out of its history, anything that is not meant for the site: contact details beyond those the site shows, unpublished research code, and anything about students.

## Build Commands

```bash
# Preview the site locally with live reload
quarto preview

# Render the site (generates HTML in _site/)
quarto render

# Publish to GitHub Pages (renders, then pushes _site/ to the gh-pages branch)
quarto publish gh-pages
```

`index.qmd` runs Python through the `homepage` Jupyter kernel, which lives in the project's `.venv`. direnv activates it in an interactive shell; anywhere else run `source .venv/bin/activate` first, or the render stops with "Jupyter kernel 'homepage' not found".

## Architecture

- **Quarto website project** configured in `_quarto.yml`
- Renders `index.qmd`, `resources.qmd`, the two guides in `resources/` and `teaching/reproducible-research/index.qmd` (cv.qmd and teaching.qmd are kept but commented out)
- Code execution: `index.qmd` runs Python in the Jupyter kernel `homepage`; `resources/r-quarto.qmd` runs R through knitr with `freeze: auto`, so its results sit in `_freeze/` (committed) and a site render needs R only after that file changes. Project-wide, freeze and cache are off.
- `_site/` is the build output and is not tracked. `quarto publish gh-pages` renders it on this machine and pushes it to the `gh-pages` branch, which GitHub Pages serves; `main` holds only the sources.
- The CV is not in the repository: `VK_CV_onlinelong.tex` and its class files stay in the local folder and are ignored. If `VK_CV_onlinelong.pdf` is present when the site is rendered, it is published as a resource.
- Theme: Journal base theme with custom `theme-light.scss` and `theme-dark.scss` ("Old Print": ivory paper, spruce ink, mauve `#5A317E`). Keep the two files in step.
- Bibliography: `VKpublications.bib` with Nature citation style (`nature.csl`)

## Key Files

- `_quarto.yml` - Main site configuration (navbar, theme, rendering options, static resources)
- `index.qmd` - Home page: bio plus the News, Research and Contact sections, which the navbar links to as anchors
- `resources.qmd` - Resources page: a `.ledger` list (label in the left gutter, then title, description and a `.ledger-links` row). Coding agents and the review skills come first, then R and Quarto. Entries that are only a linked title (the review skills, the two talks) are meant to stay that bare until their descriptions have been reviewed
- `resources/r-quarto.qmd` - Guide "R and Quarto: a short start", the summary of the 2024 Freiburg seminar *Reproducible research pipelines with R and Quarto*. Runs R (MASS, dplyr, ggplot2, knitr) on `MASS::birthwt`. A chunk prints `resources/example/report.qmd` and `references.bib` verbatim, so page and files cannot differ; the example renders on its own to HTML, Word and Typst PDF. Citations from `resources/r-quarto.bib`.
- `resources/coding-agents.qmd` - Guide "Coding agents with GitHub", no code. Tool facts come from code.claude.com, agents.md and docs.github.com (checked November 2026); recheck before changing them.
- `teaching/reproducible-research/` - Examples from the 2024/25 seminar "Reproducible Research Pipelines with R and Quarto": `index.qmd` is its page; `slides/`, `handouts/`, `source/` and `template/` hold finished files that are copied to the site as they are
- `theme-light.scss`, `theme-dark.scss` - SCSS theme overrides, including the `.ledger` list, the guides' code blocks, printed output (accent rule), file-name labels, chunk tables and R figure plates
- `VKpublications.bib` - BibTeX bibliography for academic publications

## Seminar materials

- The seminar page is kept minimal on purpose: it shows what R and Quarto can produce and links good sources, for readers with basic R. It does not describe the course (sessions, dates, assignments, grading); do not add that back.
- Only the curated set in `teaching/reproducible-research/` is in the repository and published. Nothing there is rendered by the site: the slide decks and handouts are the HTML and PDF files produced in 2024, and each zip in `source/` is one session's project folder without data.
- The seminar's original working folder, `seminar_2024/` (raw data, knitr caches, RStudio state, every draft), was removed in November 2026. Its `.gitignore` rule stays as a guard: the folder was half a gigabyte, held files over GitHub's 100 MB limit, and contained material that must not be published.
- The decks were slimmed after the fact: about 17 MB of embedded fonts were taken out of each, and a MathJax setting asks for MathJax's own web fonts.
- The decks wear the website's design. Their theme is `teaching/reproducible-research/_theme/slides.scss`; `python3 teaching/reproducible-research/_theme/apply-theme.py` writes its rules into the deck files (between marker comments, so it can be re-run) and stores it as `custom.scss` in each deck's source zip. Edit the scss, run the script, never edit the theme inside a deck. `_theme/` itself is not published.
- Not published: the course's introductory slides, the causal-inference session (source only, no rendered version), the final take-home assignment and all solutions. The posted handout, slides and template still end with the take-home tasks they were handed out with.

## Traps

- Quarto resolves navbar links through `index.qmd`, so rendering even one page needs the Jupyter kernel `homepage` (pandas, plotly, openpyxl, numpy). In a fresh container, create it with `python -m ipykernel install --user --name homepage`.
- ggplot2 4 draws themes on white paper, so R figures are not transparent; the theme's plate frames them in both modes.
- knitr evaluates inline R even inside Markdown code spans: to show inline code literally, write it with `knitr::inline_expr()`.

## Extensions

- `schochastics/academicons` - Academic icon font (ORCID, Google Scholar, etc.)
- `qmd-lab/closeread` - Scrollytelling/close reading extension
- `bootstrap-icons` - Bootstrap icon set
