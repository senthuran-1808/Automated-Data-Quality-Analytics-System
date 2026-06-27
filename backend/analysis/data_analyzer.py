import pandas as pd


class DataAnalyzer:

    @staticmethod
    def analyze(df: pd.DataFrame) -> dict:

        report = {}

        report["rows"] = len(df)

        report["columns"] = len(df.columns)

        report["column_names"] = list(df.columns)

        report["data_types"] = (
            df.dtypes.astype(str).to_dict()
        )

        report["missing_values"] = (
            df.isnull().sum().to_dict()
        )

        report["missing_percentage"] = (
            (df.isnull().mean() * 100).round(2).to_dict()
        )

        report["duplicate_rows"] = int(
            df.duplicated().sum()
        )

        report["duplicate_percentage"] = round(
            (df.duplicated().sum() / len(df)) * 100,
            2
        )

        report["unique_values"] = (
            df.nunique(dropna=True).to_dict()
        )

        report["total_null_values"] = int(
            df.isnull().sum().sum()
        )

        report["memory_usage_mb"] = round(
            df.memory_usage(deep=True).sum() /
            (1024 * 1024),
            2
        )

        return report
