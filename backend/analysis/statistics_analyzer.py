import pandas as pd


class StatisticsAnalyzer:

    @staticmethod
    def analyze(df: pd.DataFrame) -> dict:

        numeric_df = df.select_dtypes(include=["number"])

        # If no numeric columns
        if numeric_df.empty:
            return {
                "message": "No numeric columns found for statistical analysis."
            }

        stats = {}

        # Basic descriptive stats
        stats["describe"] = numeric_df.describe().round(2).to_dict()

        # Central tendency
        stats["mean"] = numeric_df.mean().round(2).to_dict()
        stats["median"] = numeric_df.median().round(2).to_dict()

        stats["mode"] = numeric_df.mode().iloc[0].to_dict() \
            if not numeric_df.mode().empty else {}

        # Spread
        stats["variance"] = numeric_df.var().round(2).to_dict()
        stats["std_dev"] = numeric_df.std().round(2).to_dict()

        # Range
        stats["min"] = numeric_df.min().to_dict()
        stats["max"] = numeric_df.max().to_dict()

        # Quartiles
        stats["quantiles"] = {
            "Q1": numeric_df.quantile(0.25).to_dict(),
            "Q2": numeric_df.quantile(0.50).to_dict(),
            "Q3": numeric_df.quantile(0.75).to_dict(),
        }

        # Shape of distribution
        stats["skewness"] = numeric_df.skew().round(2).to_dict()
        stats["kurtosis"] = numeric_df.kurtosis().round(2).to_dict()

        # Correlation matrix
        stats["correlation"] = numeric_df.corr().round(2).to_dict()

        return stats