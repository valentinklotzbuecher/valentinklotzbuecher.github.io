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
- Renders `index.qmd`, `resources.qmd` and the course page `teaching/reproducible-research/index.qmd` (cv.qmd and teaching.qmd are kept but commented out)
- Code execution: only `index.qmd` runs code, Python in the Jupyter kernel `homepage`. No page runs R, and freeze and cache are off.
- `_site/` is the build output and is not tracked. `quarto publish gh-pages` renders it on this machine and pushes it to the `gh-pages` branch, which GitHub Pages serves; `main` holds only the sources.
- The CV is not in the repository: `VK_CV_onlinelong.tex` and its class files stay in the local folder and are ignored. If `VK_CV_onlinelong.pdf` is present when the site is rendered, it is published as a resource.
- Theme: Journal base theme with custom `theme-light.scss` and `theme-dark.scss` ("Old Print": ivory paper, spruce ink, mauve `#5A317E`). Keep the two files in step.
- Bibliography: `VKpublications.bib` with Nature citation style (`nature.csl`)

## Key Files

- `_quarto.yml` - Main site configuration (navbar, theme, rendering options, static resources)
- `index.qmd` - Home page: bio plus the News, Research and Contact sections, which the navbar links to as anchors
- `resources.qmd` - Resources page: a `.ledger` list (label in the left gutter, then title, description and a `.ledger-links` row). The course comes first, then the review skills, the thesis template and the talks. Entries that are only a linked title (the review skills, the two talks) are meant to stay that bare until their descriptions have been reviewed
- `teaching/reproducible-research/` - The course "Reproducible research with R, Quarto and coding agents": `index.qmd` is its page; `slides/`, `handouts/`, `source/` and `template/` hold the examples, finished files from the 2024/25 Freiburg seminar "Reproducible Research Pipelines with R and Quarto" that are copied to the site as they are
- `theme-light.scss`, `theme-dark.scss` - SCSS theme overrides, including the `.ledger` list, code blocks and their file-name labels, the `.pipeline` row and the tours ("Scrollytelling" block). The rules for printed R output, chunk tables and R figure plates are left from the guides the course replaced and style nothing at present
- `VKpublications.bib` - BibTeX bibliography for academic publications

## Course page and seminar materials

- The course page replaced three pages in November 2026: the seminar's page of examples and the guides "R and Quarto: a short start" and "Coding agents with GitHub" (all three last in commit `917bd66`). Its front matter lists the guides' addresses under `aliases`, so `/resources/r-quarto.html` and `/resources/coding-agents.html` redirect to it.
- It is for a broad audience and kept short on purpose: it shows what R, Quarto and a coding agent do and leaves the details to the sources it links (Quarto's first tutorial and guide, R for Data Science, Happy Git, the Claude Code documentation). Do not add back an R walk-through, installation steps, a table of formats or a description of the seminar (sessions, dates, assignments, grading).
- It has two scrollytelling tours, closeread sections (`:::{.cr-section}`): the text scrolls, the panel beside it stays. The first switches from a source file to its outputs. The second follows one task given to a coding agent: the notes file, the request, the branch, the changed lines, the review and the merge; its panels are text and two inline SVG diagrams (`.tour-diagram`), with no pictures. The second tour changes the `report.qmd` of the first, and its notes file says to ask before leaving out observations, which the changed lines then do: keep the three in step.
- For the tours the page's format is `closeread-html`, which does not inherit the site's `format: html` settings, so theme, page layout and body width are repeated in its front matter. The pictures in `tour/` are screenshots of the posted examples (headless Chrome for the HTML files, `pdftoppm` for the PDF pages); retake them if an example changes. The styles are the "Scrollytelling" block in both theme files; on a narrow screen the panel is pinned to the top so that a step's text arrives below it.
- Facts about the tools (Claude Code, Codex, Copilot coding agent, `CLAUDE.md` and `AGENTS.md`) come from code.claude.com, agents.md and docs.github.com (checked November 2026); recheck before changing them.
- Only the curated set in `teaching/reproducible-research/` is in the repository and published. Nothing there is rendered by the site: the slide decks and handouts are the HTML and PDF files produced in 2024, and each zip in `source/` is one session's project folder without data.
- The seminar's original working folder, `seminar_2024/` (raw data, knitr caches, RStudio state, every draft), was removed in November 2026. Its `.gitignore` rule stays as a guard: the folder was half a gigabyte, held files over GitHub's 100 MB limit, and contained material that must not be published.
- The decks were slimmed after the fact: about 17 MB of embedded fonts were taken out of each, and a MathJax setting asks for MathJax's own web fonts.
- The decks wear the website's design. Their theme is `teaching/reproducible-research/_theme/slides.scss`; `python3 teaching/reproducible-research/_theme/apply-theme.py` writes its rules into the deck files (between marker comments, so it can be re-run) and stores it as `custom.scss` in each deck's source zip. Edit the scss, run the script, never edit the theme inside a deck. `_theme/` itself is not published.
- Not published: the course's introductory slides, the causal-inference session (source only, no rendered version), the final take-home assignment and all solutions. The posted handout, slides and template still end with the take-home tasks they were handed out with.

## Traps

- Quarto resolves navbar links through `index.qmd`, so rendering even one page needs the Jupyter kernel `homepage` (pandas, plotly, openpyxl, numpy). In a fresh container, create it with `python -m ipykernel install --user --name homepage`.
- No page runs R. The code panels of the course page show `{{r}}` chunks and inline R as text; if a page there ever gets the knitr engine, knitr will evaluate that inline R, even inside code spans.

## Extensions

- `schochastics/academicons` - Academic icon font (ORCID, Google Scholar, etc.)
- `qmd-lab/closeread` - Scrollytelling/close reading extension
- `bootstrap-icons` - Bootstrap icon set
