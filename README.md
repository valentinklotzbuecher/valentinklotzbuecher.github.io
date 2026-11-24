# valentinklotzbuecher.github.io

Source of my website, <https://valentinklotzbuecher.github.io>, built with
[Quarto](https://quarto.org).

- `index.qmd`: home page, with the interactive figures
- `resources.qmd` and `resources/`: the Resources page and its guides
- `teaching/reproducible-research/`: materials of the seminar *Reproducible
  Research Pipelines with R and Quarto*
- `theme-light.scss`, `theme-dark.scss`: the design

`quarto render` builds the site into `_site/`, and `quarto publish gh-pages`
publishes it. The home page needs Python with pandas and plotly. The guide in
`resources/r-quarto.qmd` needs R only when it changes, because its results are
stored in `_freeze/`.
