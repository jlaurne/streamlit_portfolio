import pandas as pd

def calculate_metric(df, definition):
    if definition == "Definition 1":
        return df["MetricA"].mean()
    elif definition == "Definition 2":
        return df["MetricB"].mean()
    else:
        return (df["MetricA"] + df["MetricB"]).mean()
