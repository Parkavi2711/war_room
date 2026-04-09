import pandas as pd


def load_metrics(csv_path: str) -> pd.DataFrame:
    """
    Load metrics CSV into a pandas DataFrame.
    """
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def analyze_trends(df: pd.DataFrame) -> dict:
    """
    Analyze simple metric trends by comparing first and last values.
    """
    metrics = [
        "activation_rate",
        "dau",
        "d1_retention",
        "crash_rate",
        "api_latency_p95_ms",
        "support_tickets"
    ]

    trends = {}

    for metric in metrics:
        start = df[metric].iloc[0]
        end = df[metric].iloc[-1]

        if end > start * 1.05:
            trend = "increasing"
        elif end < start * 0.95:
            trend = "decreasing"
        else:
            trend = "stable"

        trends[metric] = {
            "start": round(float(start), 3),
            "end": round(float(end), 3),
            "trend": trend
        }

    return trends


def detect_anomalies(df: pd.DataFrame) -> dict:
    """
    Detect simple anomalies using fixed thresholds.
    """
    latest = df.iloc[-1]
    anomalies = {}

    if latest["crash_rate"] > 1.5:
        anomalies["crash_rate"] = "High crash rate detected"

    if latest["api_latency_p95_ms"] > 280:
        anomalies["api_latency"] = "High API latency detected"

    if latest["support_tickets"] > 40:
        anomalies["support_tickets"] = "Spike in support tickets"

    return anomalies