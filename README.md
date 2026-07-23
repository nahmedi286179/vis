# customplots

Nicer-looking charts than pandas' defaults — in one import.

pandas' built-in `.plot()` is great for a quick look, but the defaults are
noisy: heavy spines, cramped titles, a color cycle that isn't colorblind-safe.
`customplots` is a tiny wrapper (under 200 lines) that applies a clean,
validated theme and gives you a handful of plotting helpers that take the same
pandas objects you already have.

## Install

```bash
pip install -e .
```

Requires `matplotlib` and `pandas`.

## Usage

```python
import pandas as pd
import customplots as pp

df = pd.DataFrame(
    {"north": [12, 15, 14, 18, 21, 24], "south": [8, 9, 13, 12, 16, 19]},
    index=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
)

pp.line(df, title="Revenue by region", ylabel="$k")
```

The theme is applied automatically on `import customplots`. If another library
resets matplotlib's style, call `pp.use()` again to reapply it.

### Helpers

| Function | Chart |
|----------|-------|
| `pp.line(data, ...)`    | line chart |
| `pp.bar(data, ...)`     | vertical bar chart |
| `pp.barh(data, ...)`    | horizontal bar chart |
| `pp.scatter(data, x, y, ...)` | scatter plot of two columns |
| `pp.hist(data, ...)`    | histogram |

Every helper accepts a pandas `Series` or `DataFrame`, optional `title`,
`xlabel`, `ylabel`, and an existing `ax` to draw into. Extra keyword arguments
pass straight through to matplotlib, and each returns the `Axes` so you can keep
customizing.

### Custom colors

Every helper takes an optional `colors` argument. Leave it out to use the
built-in colorblind-safe palette, or pass your own to override it. You can use
plain **color names** — no need to know hex codes:

```python
# one color per series, by name
pp.line(df, colors=["black", "orange"])
pp.bar(df, colors=["red", "green", "blue"])

# a single color (accepts a list or a bare string)
pp.hist(scores, colors="purple")

# hex codes work too, if you want an exact shade
pp.line(df, colors=["#111111", "#ff5500"])
```

Common names: `black`, `white`, `gray` (or `grey`), `red`, `orange`, `yellow`,
`green`, `blue`, `indigo`, `violet`, `purple`, `pink`, `brown`, `cyan`,
`magenta` — plus over a thousand more that matplotlib recognizes.

For multi-series charts (`line`, `bar`, `barh`) the colors are applied one per
series, in order. For single-color charts (`scatter`, `hist`) the first color
is used.

## What the theme changes

- Colorblind-safe categorical palette, assigned in fixed order.
- Drops the top and right spines; soft horizontal gridlines only.
- Left-aligned, bold titles with breathing room.
- A legend appears automatically only when there are two or more series.

## Gallery

Run the demo to render every chart type into `examples/gallery.png`:

```bash
python examples/demo.py
```

![gallery](examples/gallery.png)

## License

MIT — see [LICENSE](LICENSE).
