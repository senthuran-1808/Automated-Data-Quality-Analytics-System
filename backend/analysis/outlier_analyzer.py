import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class OutlierAnalyzer:

    @staticmethod
    def iqr_method(df: pd.DataFrame) -> dict:

        numeric_df = df.select_dtypes(include=["number"])

        results = {}

        for col in numeric_df.columns:

            Q1 = numeric_df[col].quantile(0.25)
            Q3 = numeric_df[col].quantile(0.75)

            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers = numeric_df[
                (numeric_df[col] < lower_bound) |
                (numeric_df[col] > upper_bound)
            ]

            results[col] = {
                "outlier_count": len(outliers),
                "outlier_indices": outliers.index.tolist(),
                "lower_bound": lower_bound,
                "upper_bound": upper_bound
            }

        return results

    @staticmethod
    def zscore_method(df: pd.DataFrame, threshold: float = 3.0) -> dict:

        numeric_df = df.select_dtypes(include=["number"])

        results = {}

        for col in numeric_df.columns:

            mean = numeric_df[col].mean()
            std = numeric_df[col].std()

            if std == 0:
                results[col] = {
                    "outlier_count": 0,
                    "outlier_indices": []
                }
                continue

            z_scores = (numeric_df[col] - mean) / std

            outliers = numeric_df[np.abs(z_scores) > threshold]

            results[col] = {
                "outlier_count": len(outliers),
                "outlier_indices": outliers.index.tolist(),
                "threshold": threshold
            }

        return results

    @staticmethod
    def isolation_forest(df: pd.DataFrame) -> dict:

        numeric_df = df.select_dtypes(include=["number"])

        if numeric_df.empty:
            return {}

        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_df)

        model = IsolationForest(
            contamination=0.05,
            random_state=42
        )

        preds = model.fit_predict(scaled_data)

        outlier_indices = numeric_df.index[preds == -1].tolist()

        return {
            "outlier_count": len(outlier_indices),
            "outlier_indices": outlier_indices
        }

    @staticmethod
    def analyze(df: pd.DataFrame) -> dict:

        return {
            "iqr": OutlierAnalyzer.iqr_method(df),
            "zscore": OutlierAnalyzer.zscore_method(df),
            "isolation_forest": OutlierAnalyzer.isolation_forest(df)
        }