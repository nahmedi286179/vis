"""customplots — nicer-looking charts than pandas' defaults, in one import.

Wraps matplotlib with a clean, validated theme and a handful of plotting
helpers that accept pandas Series/DataFrames.

    import customplots as cust
    cust.use()                 # apply the theme globally
    cust.line(df)              # styled line chart
    cust.bar(df["sales"])      # styled bar chart

The theme is applied automatically on import; call ``cust.use()`` again after
any other library resets matplotlib's rcParams.
"""

from .core import PALETTE, use, line, bar, barh, scatter, hist

use()

__version__ = "0.1.0"

__all__ = ["PALETTE", "use", "line", "bar", "barh", "scatter", "hist"]
