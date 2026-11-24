#!/usr/bin/env python3
"""Apply slides.scss to the finished slide decks and their source bundles.

The decks in ../slides/ are HTML files rendered in 2024; building the site
only copies them. Each carries its theme as one stylesheet inside the file.
This script writes the rules of slides.scss into that stylesheet, between two
marker comments, so it can be run again after every change to the theme:

    python3 teaching/reproducible-research/_theme/apply-theme.py

It also stores the theme as custom.scss in each deck's zip in ../source/, so
that a fresh `quarto render` of the sources gives the same look. Each deck
keeps its own font size and line height.

Standard library only.
"""
import os
import re
import sys
import time
import urllib.parse
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEME = HERE / "slides.scss"
SLIDES = HERE.parent / "slides"
SOURCE = HERE.parent / "source"

# deck -> zip that holds its sources
DECKS = {
    "intro.html": "intro-slides.zip",
    "maps-and-merging.html": "maps-and-merging.zip",
    "interpreting-estimates.html": "interpreting-estimates.zip",
}

START = "/* old-print theme: start */"
END = "/* old-print theme: end */"

# Set per deck, taken from the custom.scss the deck was built with
PER_DECK = ("presentation-font-size-root", "presentation-line-height")


def read_theme():
    text = THEME.read_text(encoding="utf-8")
    defaults, rules = text.split("/*-- scss:rules --*/")
    defaults = defaults.split("/*-- scss:defaults --*/")[1]
    return text, defaults, rules


def scss_variables(defaults):
    """$name: value; pairs of the defaults section, references resolved."""
    values = {}
    for line in defaults.splitlines():
        m = re.match(r"\s*\$([\w-]+):\s*(.+?);\s*(?://.*)?$", line)
        if m:
            values[m.group(1)] = m.group(2).strip()
    for name, value in values.items():
        while True:
            ref = re.fullmatch(r"\$([\w-]+)", value)
            if not ref:
                break
            value = values[ref.group(1)]
        values[name] = value
    return values


def plain_css(rules, values):
    """The rules section as a plain stylesheet: fill in #{$name}."""
    css = re.sub(r"#\{\$([\w-]+)\}", lambda m: values[m.group(1)], rules)
    assert "#{" not in css and "$" not in css, "rules must stay plain CSS"
    return css.strip() + "\n"


def font_imports(defaults):
    urls = re.findall(r"@import\s+url\(['\"]([^'\"]+)['\"]\)\s*;", defaults)
    assert urls, "no font import in the theme"
    return "".join('@import url("%s");\n' % u for u in urls)


def hex_to_rgb(colour):
    h = colour.lstrip("#")
    return "rgb(%d, %d, %d)" % tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def restyle_deck(path, css_block, imports, ink):
    html = path.read_text(encoding="utf-8")
    links = list(re.finditer(r'<link href="(data:text/css,[^"]*)"', html))
    theme = max(links, key=lambda m: len(m.group(1)))
    css = urllib.parse.unquote(theme.group(1)[len("data:text/css,"):])

    # Drop what an earlier run added, and whichever fonts were imported
    css = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "",
                 css, flags=re.S)
    css = re.sub(r'@import\s+url\("https://fonts\.googleapis\.com/[^"]*"\)\s*;\s*',
                 "", css)

    # The menu button is an inline SVG drawn in the old link colour
    css, n = re.subn(
        r'(\.slide-menu-button \.fa-bars::before\s*\{[^}]*?fill=")rgb\([^)]*\)',
        lambda m: m.group(1) + hex_to_rgb(ink), css)
    assert n == 1, "menu button rule not found in %s" % path.name

    css = imports + css.strip() + "\n" + START + "\n" + css_block + END + "\n"
    new = (html[:theme.start(1)] + "data:text/css,"
           + urllib.parse.quote(css, safe="-_.~") + html[theme.end(1):])
    if new != html:
        path.write_text(new, encoding="utf-8")
        return "restyled"
    return "unchanged"


def restyle_bundle(path, theme_text):
    with zipfile.ZipFile(path) as z:
        members = [(info, z.read(info.filename)) for info in z.infolist()]
    target = [i for i, (info, _) in enumerate(members)
              if info.filename.endswith("/custom.scss")]
    assert len(target) == 1, "expected one custom.scss in %s" % path.name
    info, old = members[target[0]]
    old = old.decode("utf-8")

    scss = theme_text
    for name in PER_DECK:
        current = re.search(r"\$%s:\s*([^;]+);" % name, old)
        assert current, "%s not set in %s" % (name, path.name)
        scss, n = re.subn(r"(\$%s:\s*)[^;]+;" % name,
                          lambda m: m.group(1) + current.group(1).strip() + ";",
                          scss)
        assert n == 1
    if scss == old:
        return "unchanged"

    stamp = time.localtime(THEME.stat().st_mtime)[:6]
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for i, (member, data) in enumerate(members):
            if i == target[0]:
                fresh = zipfile.ZipInfo(member.filename, date_time=stamp)
                fresh.compress_type = zipfile.ZIP_DEFLATED
                fresh.external_attr = member.external_attr
                z.writestr(fresh, scss.encode("utf-8"))
            else:
                z.writestr(member, data)
    os.replace(tmp, path)
    return "custom.scss replaced"


def main():
    theme_text, defaults, rules = read_theme()
    values = scss_variables(defaults)
    css_block = plain_css(rules, values)
    imports = font_imports(defaults)
    for deck, bundle in DECKS.items():
        print("%-28s %s" % (deck, restyle_deck(SLIDES / deck, css_block,
                                               imports, values["ink"])))
        print("%-28s %s" % (bundle, restyle_bundle(SOURCE / bundle, theme_text)))


if __name__ == "__main__":
    sys.exit(main())
