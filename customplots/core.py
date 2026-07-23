"""Core theme and plotting helpers for customplots.

The design goal is simple: charts that look considered by default. We set a
restrained matplotlib style (no chart junk, soft gridlines, a colorblind-safe
categorical palette) and expose thin wrappers that take pandas objects.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

# Colorblind-safe categorical palette, assigned in fixed order (never cycled
# past its length). Values are the validated data-viz reference palette.
PALETTE = [
    "#2a78d6",  # blue
    "#eb6834",  # orange
    "#1baf7a",  # aqua
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
    """Apply the customplots theme to matplotlib's global rcParams."""
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


def line(data, *, title=None, xlabel=None, ylabel=None, ax=None, **kwargs):
    """Styled line chart from a pandas Series or DataFrame."""
    ax = _new_ax(ax, title, xlabel, ylabel)
    data.plot(ax=ax, legend=False, **kwargs)
    _legend(ax, data)
    return ax


def bar(data, *, title=None, xlabel=None, ylabel=None, ax=None, **kwargs):
    """Styled vertical bar chart from a pandas Series or DataFrame."""
    ax = _new_ax(ax, title, xlabel, ylabel)
    data.plot.bar(ax=ax, legend=False, width=0.72, edgecolor=_SURFACE,
                  linewidth=1.5, **kwargs)
    ax.tick_params(axis="x", rotation=0)
    _legend(ax, data)
    return ax


def barh(data, *, title=None, xlabel=None, ylabel=None, ax=None, **kwargs):
    """Styled horizontal bar chart from a pandas Series or DataFrame."""
    ax = _new_ax(ax, title, xlabel, ylabel)
    data.plot.barh(ax=ax, legend=False, edgecolor=_SURFACE,
                   linewidth=1.5, **kwargs)
    # Horizontal bars read better with a vertical grid instead.
    ax.grid(axis="x", color=_GRID, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    _legend(ax, data)
    return ax


def scatter(data, x, y, *, title=None, xlabel=None, ylabel=None, ax=None,
            **kwargs):
    """Styled scatter plot of two columns from a DataFrame."""
    ax = _new_ax(ax, title, xlabel or x, ylabel or y)
    ax.scatter(data[x], data[y], color=PALETTE[0], alpha=0.8,
               edgecolor=_SURFACE, linewidth=0.8, **kwargs)
    return ax


def hist(data, *, bins=20, title=None, xlabel=None, ylabel="count", ax=None,
         **kwargs):
    """Styled histogram from a pandas Series or 1-D data."""
    ax = _new_ax(ax, title, xlabel, ylabel)
    ax.hist(data, bins=bins, color=PALETTE[0], edgecolor=_SURFACE,
            linewidth=0.8, **kwargs)
    return ax
