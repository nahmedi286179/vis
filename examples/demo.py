"""Render every customplots chart type into a comparison image.

Run from the repo root:  python examples/demo.py
Produces examples/gallery.png
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import customplots as pp

rng = np.random.default_rng(7)

months = pd.Index(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], name="month")
revenue = pd.DataFrame(
    {"north": [12, 15, 14, 18, 21, 24], "south": [8, 9, 13, 12, 16, 19]},
    index=months,
)
points = pd.DataFrame({"x": rng.normal(size=200), "y": rng.normal(size=200)})
samples = pd.Series(rng.normal(loc=50, scale=12, size=500))

fig, axes = plt.subplots(2, 2, figsize=(13, 9))

pp.line(revenue, title="Revenue by region", ylabel="$k", ax=axes[0, 0])
pp.bar(revenue, title="Revenue by region", ylabel="$k", ax=axes[0, 1])
pp.scatter(points, "x", "y", title="Sample scatter", ax=axes[1, 0])
pp.hist(samples, title="Score distribution", xlabel="score", ax=axes[1, 1])

fig.tight_layout()
fig.savefig("examples/gallery.png", dpi=110)
print("wrote examples/gallery.png")
