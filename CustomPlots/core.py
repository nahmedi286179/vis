"""Core theme and plotting helpers for CustomPlots.

The design goal is simple: charts that look considered by default. We set a
restrained matplotlib style (no chart junk, soft gridlines, a colorblind-safe
categorical palette) and expose thin wrappers that take pandas objects.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

# Categorical palette, assigned in fixed order (never cycled past its length).
# The first two slots are the project's default colors; the remaining slots
# fall back to the validated colorblind-safe reference palette for charts with
# three or more series.
PALETTE = [
    "#266867",  # teal        (default 1 — also the single-color default)
    "#051821",  # deep teal   (default 2)
    "#eb6834",  # orange
    "#eda100",  # yellow
    "#e87ba4",  # magenta
    "#008300",  # green
    "#4a3aa7",  # violet
    "#e34948",  # red
]

# Ink / chrome colors pulled from the same reference system.
_INK = "#0b0b0b"
_MUTED = "#898781"
_GRID = "#e1e0d9"
_SURFACE = "#fcfcfb"


def use() -> None:
    """Apply the CustomPlots theme to matplotlib's global rcParams."""
    plt.rcParams.update({
        # Typography
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 12,
        "axes.labelsize": 11,
        "axes.labelcolor": _MUTED,
        # Color & surface
        "axes.prop_cycle": plt.cycler(color=PALETTE),
        "figure.facecolor": _SURFACE,
        "axes.facecolor": _SURFACE,
        "text.color": _INK,
        "axes.edgecolor": _MUTED,
        "xtick.color": _MUTED,
        "ytick.color": _MUTED,
        "xtick.labelcolor": _INK,
        "ytick.labelcolor": _INK,
        # De-cluttered frame: drop top/right spines, soft horizontal grid only
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": _GRID,
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,
        # Ticks: minimal
        "xtick.bottom": True,
        "ytick.left": False,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        # Marks & layout
        "lines.linewidth": 2.0,
        "lines.markersize": 6,
        "figure.figsize": (8, 5),
        "figure.dpi": 110,
        "figure.autolayout": True,
        "legend.frameon": False,
        "legend.fontsize": 10,
    })


def _new_ax(ax, title, xlabel, ylabel):
    """Return an Axes, creating a figure if needed, and set common labels."""
    if ax is None:
        _, ax = plt.subplots()
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    return ax


def _legend(ax, data):
    """Show a legend only when there are two or more series."""
    if getattr(data, "ndim", 1) == 2 and data.shape[1] >= 2:
        ax.legend(loc="best")


def _palette(colors):
    """Normalize a user ``colors`` argument to a list, defaulting to PALETTE.

    Accepts ``None`` (use the theme palette), a single color string, or any
    sequence of colors.
    """
    if colors is None:
        return list(PALETTE)
    if isinstance(colors, str):
        return [colors]
    return list(colors)


def line(data, *, colors=None, title=None, xlabel=None, ylabel=None, ax=None,
         **kwargs):
    """Styled line chart from a pandas Series or DataFrame.

    ``colors`` optionally overrides the palette, one color per series.
    """
    ax = _new_ax(ax, title, xlabel, ylabel)
    data.plot(ax=ax, legend=False, color=_palette(colors), **kwargs)
    _legend(ax, data)
    return ax


def bar(data, *, colors=None, title=None, xlabel=None, ylabel=None, ax=None,
        **kwargs):
    """Styled vertical bar chart from a pandas Series or DataFrame.

    ``colors`` optionally overrides the palette, one color per series.
    """
    ax = _new_ax(ax, title, xlabel, ylabel)
    data.plot.bar(ax=ax, legend=False, width=0.72, edgecolor=_SURFACE,
                  linewidth=1.5, color=_palette(colors), **kwargs)
    ax.tick_params(axis="x", rotation=0)
    _legend(ax, data)
    return ax


def barh(data, *, colors=None, title=None, xlabel=None, ylabel=None, ax=None,
         **kwargs):
    """Styled horizontal bar chart from a pandas Series or DataFrame.

    ``colors`` optionally overrides the palette, one color per series.
    """
    ax = _new_ax(ax, title, xlabel, ylabel)
    data.plot.barh(ax=ax, legend=False, edgecolor=_SURFACE,
                   linewidth=1.5, color=_palette(colors), **kwargs)
    # Horizontal bars read better with a vertical grid instead.
    ax.grid(axis="x", color=_GRID, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    _legend(ax, data)
    return ax


def scatter(data, x, y, *, colors=None, title=None, xlabel=None, ylabel=None,
            ax=None, **kwargs):
    """Styled scatter plot of two columns from a DataFrame.

    ``colors`` optionally sets the point color (first entry if a list).
    """
    ax = _new_ax(ax, title, xlabel or x, ylabel or y)
    ax.scatter(data[x], data[y], color=_palette(colors)[0], alpha=0.8,
               edgecolor=_SURFACE, linewidth=0.8, **kwargs)
    return ax


def hist(data, *, colors=None, bins=20, title=None, xlabel=None,
         ylabel="count", ax=None, **kwargs):
    """Styled histogram from a pandas Series or 1-D data.

    ``colors`` optionally sets the bar color (first entry if a list).
    """
    ax = _new_ax(ax, title, xlabel, ylabel)
    ax.hist(data, bins=bins, color=_palette(colors)[0], edgecolor=_SURFACE,
            linewidth=0.8, **kwargs)
    return ax


# --- Annotation helpers -----------------------------------------------------
# These take an existing Axes (the object every plot function returns) and
# layer a reference mark on top, so you can measure the data against something.


def constant_line(ax, value, *, axis="y", label=None, color=None,
                  linestyle="--", **kwargs):
    """Draw a constant reference line to measure the data against.

    ``axis="y"`` draws a horizontal line at height ``value`` (a target, a
    threshold, a mean); ``axis="x"`` draws a vertical line at ``value``.
    An optional ``label`` is printed next to the line.
    """
    color = color or _MUTED
    draw = ax.axhline if axis == "y" else ax.axvline
    draw(value, color=color, linestyle=linestyle, linewidth=1.5, zorder=1.5,
         **kwargs)
    if label:
        if axis == "y":
            ax.text(0.01, value, label, transform=ax.get_yaxis_transform(),
                    va="bottom", ha="left", color=color, fontsize=9)
        else:
            ax.text(value, 0.98, label, transform=ax.get_xaxis_transform(),
                    va="top", ha="left", color=color, fontsize=9, rotation=90)
    return ax


def mean_line(ax, data, *, axis="y", label="mean", **kwargs):
    """Draw a constant line at the mean of ``data`` (a Series/array/list)."""
    value = float(np.asarray(data, dtype=float).mean())
    if label == "mean":
        label = f"mean {value:.1f}"
    return constant_line(ax, value, axis=axis, label=label, **kwargs)


def band(ax, low, high, *, axis="y", color=None, alpha=0.12, label=None,
         **kwargs):
    """Shade a target range between ``low`` and ``high`` to measure against."""
    color = color or PALETTE[0]
    span = ax.axhspan if axis == "y" else ax.axvspan
    span(low, high, color=color, alpha=alpha, linewidth=0, zorder=0,
         label=label, **kwargs)
    return ax


def add_point(ax, x, y, *, label=None, color=None, size=70, **kwargs):
    """Highlight a single (x, y) point with a marker and optional label."""
    color = color or PALETTE[-1]
    ax.scatter([x], [y], color=color, s=size, zorder=5, edgecolor=_SURFACE,
               linewidth=1.4, **kwargs)
    if label:
        ax.annotate(label, (x, y), textcoords="offset points", xytext=(8, 8),
                    color=_INK, fontsize=9, fontweight="bold")
    return ax


def label_bars(ax, *, fmt="{:.0f}", color=None, padding=3):
    """Print value labels on the bars of a bar/barh chart."""
    color = color or _INK
    for container in ax.containers:
        labels = [fmt.format(v) for v in container.datavalues]
        ax.bar_label(container, labels=labels, padding=padding, color=color,
                     fontsize=9)
    return ax
