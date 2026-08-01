"""Side-by-side: plain matplotlib/pandas defaults vs. CustomPlots.

Same data, same chart types — the only difference is the styling. Left column
is what pandas' ``.plot()`` gives you out of the box; right column is
CustomPlots.

Run from the repo root:  python examples/comparison.py
Produces examples/comparison.png
"""

import matplotlib
matplotlib.use("Agg")  # render to a file without opening a window
import matplotlib.pyplot as plt
import pandas as pd

import CustomPlots as cust  # note: this applies the CustomPlots theme globally

# Shared data for every panel.
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
revenue = pd.DataFrame(
    {"north": [12, 15, 14, 18, 21, 24], "south": [8, 9, 13, 12, 16, 19]},
    index=months,
)

fig = plt.figure(figsize=(12, 9))
fig.suptitle("Same data, same chart — plain matplotlib vs. CustomPlots",
             fontsize=15, fontweight="bold")

# --- LEFT COLUMN: plain matplotlib / pandas defaults ------------------------
# `plt.style.context("default")` temporarily restores matplotlib's stock look,
# so these panels are unaffected by the CustomPlots theme imported above.
with plt.style.context("default"):
    ax = fig.add_subplot(2, 2, 1)
    revenue.plot(ax=ax)
    ax.set_title("Before — pandas default")

    ax = fig.add_subplot(2, 2, 3)
    revenue.plot.bar(ax=ax)
    ax.set_title("Before — pandas default")

# --- RIGHT COLUMN: CustomPlots ----------------------------------------------
# Drawn outside the context, so the CustomPlots theme is active.
cust.line(revenue, title="After — CustomPlots", ax=fig.add_subplot(2, 2, 2))
ax = cust.bar(revenue, title="After — CustomPlots", ax=fig.add_subplot(2, 2, 4))
cust.label_bars(ax)  # a CustomPlots extra: values printed on the bars

fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig("examples/comparison.png", dpi=110)
print("wrote examples/comparison.png")
