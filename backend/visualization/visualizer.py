import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class Visualizer:

    @staticmethod
    def missing_value_chart(df: pd.DataFrame):

        missing = df.isnull().sum()

        missing = missing[missing > 0]

        if missing.empty:
            return None

        fig = px.bar(
            x=missing.index,
            y=missing.values,
            labels={
                "x": "Columns",
                "y": "Missing Values"
            },
            title="Missing Values by Column"
        )

        return fig

    @staticmethod
    def correlation_heatmap(df: pd.DataFrame):

        numeric = df.select_dtypes(include="number")

        if numeric.empty:
            return None

        corr = numeric.corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            title="Correlation Heatmap"
        )

        return fig

    @staticmethod
    def histogram(df: pd.DataFrame, column: str):

        fig = px.histogram(
            df,
            x=column,
            title=f"Histogram - {column}"
        )

        return fig

    @staticmethod
    def boxplot(df: pd.DataFrame, column: str):

        fig = px.box(
            df,
            y=column,
            title=f"Box Plot - {column}"
        )

        return fig

    @staticmethod
    def scatter(df: pd.DataFrame, x: str, y: str):

        fig = px.scatter(
            df,
            x=x,
            y=y,
            title=f"{x} vs {y}"
        )

        return fig

    @staticmethod
    def pie_chart(df: pd.DataFrame, column: str):

        counts = df[column].value_counts()

        fig = px.pie(
            values=counts.values,
            names=counts.index,
            title=f"{column} Distribution"
        )

        return fig
