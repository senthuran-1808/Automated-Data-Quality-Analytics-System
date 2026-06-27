import streamlit as st
import pandas as pd

from backend.loaders.dataset_loader import DatasetLoader
from backend.analysis.data_analyzer import DataAnalyzer
from backend.analysis.statistics_analyzer import StatisticsAnalyzer
from backend.analysis.outlier_analyzer import OutlierAnalyzer
from backend.rules.rule_engine import RuleEngine
from backend.visualization.visualizer import Visualizer


st.set_page_config(
    page_title="AI Data Quality Copilot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Data Quality Copilot")
st.markdown("Upload any dataset (CSV, Excel, TSV, TXT) for full data quality analysis.")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx", "xls", "txt", "tsv"]
)

if uploaded_file:

    try:
        # ---------------- LOAD DATA ----------------
        df = DatasetLoader.load(uploaded_file)

        # ---------------- ANALYSIS ENGINE ----------------
        analysis = DataAnalyzer.analyze(df)

        # ---------------- STATISTICS ENGINE ----------------
        stats = StatisticsAnalyzer.analyze(df)

        # ---------------- OUTLIER ENGINE ----------------
        outliers = OutlierAnalyzer.analyze(df)

        # ---------------- RULE ENGINE ----------------
        rules = RuleEngine.evaluate(analysis, df)

        st.success("Dataset successfully analyzed!")

        # =========================================================
        # DATASET PREVIEW
        # =========================================================
        st.header("📊 Dataset Preview")
        st.dataframe(df, use_container_width=True)

        # =========================================================
        # BASIC OVERVIEW
        # =========================================================
        st.header("📌 Dataset Overview")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Rows", analysis["rows"])
        c2.metric("Columns", analysis["columns"])
        c3.metric("Duplicates", analysis["duplicate_rows"])
        c4.metric("Null Values", analysis["total_null_values"])

        st.info(f"Memory Usage: {analysis['memory_usage_mb']} MB")

        # =========================================================
        # DATA QUALITY SCORE
        # =========================================================
        st.header("⭐ Data Quality Score")

        st.metric(
            "Score",
            rules["quality_score"],
            rules["quality_flags"][0]
        )

        # =========================================================
        # RULE ENGINE OUTPUT
        # =========================================================
        st.subheader("⚠️ Warnings")

        if rules["warnings"]:
            for w in rules["warnings"]:
                st.warning(w)
        else:
            st.success("No major issues detected.")

        st.subheader("💡 Recommendations")

        if rules["recommendations"]:
            for r in rules["recommendations"]:
                st.info(r)
        else:
            st.success("Dataset looks clean. No recommendations.")

        # =========================================================
        # DATA TYPES
        # =========================================================
        st.header("🧾 Data Types")

        datatype_df = pd.DataFrame(
            analysis["data_types"].items(),
            columns=["Column", "Type"]
        )

        st.dataframe(datatype_df, use_container_width=True)

        # =========================================================
        # MISSING VALUES
        # =========================================================
        st.header("❌ Missing Value Analysis")

        missing_df = pd.DataFrame({
            "Column": analysis["missing_values"].keys(),
            "Missing Values": analysis["missing_values"].values(),
            "Missing %": analysis["missing_percentage"].values()
        })

        st.dataframe(missing_df, use_container_width=True)

        # =========================================================
        # UNIQUE VALUES
        # =========================================================
        st.header("🔢 Unique Values")

        unique_df = pd.DataFrame({
            "Column": analysis["unique_values"].keys(),
            "Unique Values": analysis["unique_values"].values()
        })

        st.dataframe(unique_df, use_container_width=True)

        # =========================================================
        # STATISTICS ENGINE
        # =========================================================
        st.header("📈 Statistical Analysis")

        if "message" in stats:
            st.warning(stats["message"])
        else:

            st.subheader("Mean")
            st.dataframe(pd.DataFrame(stats["mean"].items(), columns=["Column", "Mean"]))

            st.subheader("Median")
            st.dataframe(pd.DataFrame(stats["median"].items(), columns=["Column", "Median"]))

            st.subheader("Variance")
            st.dataframe(pd.DataFrame(stats["variance"].items(), columns=["Column", "Variance"]))

            st.subheader("Standard Deviation")
            st.dataframe(pd.DataFrame(stats["std_dev"].items(), columns=["Column", "Std Dev"]))

            st.subheader("Skewness")
            st.dataframe(pd.DataFrame(stats["skewness"].items(), columns=["Column", "Skewness"]))

            st.subheader("Kurtosis")
            st.dataframe(pd.DataFrame(stats["kurtosis"].items(), columns=["Column", "Kurtosis"]))

            st.subheader("Correlation Matrix")
            st.dataframe(pd.DataFrame(stats["correlation"]))

        # =========================================================
        # OUTLIER DETECTION (FIXED UI)
        # =========================================================
        st.header("🚨 Outlier Detection")

        # ---------------- IQR METHOD ----------------
        st.subheader("IQR Method")

        iqr_list = []

        for col, info in outliers["iqr"].items():
            iqr_list.append({
                "Column": col,
                "Outliers Count": info["outlier_count"],
                "Lower Bound": info["lower_bound"],
                "Upper Bound": info["upper_bound"]
            })

        st.dataframe(pd.DataFrame(iqr_list), use_container_width=True)

        # ---------------- Z SCORE ----------------
        st.subheader("Z-Score Method")

        z_list = []

        for col, info in outliers["zscore"].items():
            z_list.append({
                "Column": col,
                "Outliers Count": info["outlier_count"],
                "Threshold": info.get("threshold", 3)
            })

        st.dataframe(pd.DataFrame(z_list), use_container_width=True)

        # ---------------- ISOLATION FOREST ----------------
        st.subheader("Isolation Forest")

        st.metric(
            "Total Outliers",
            outliers["isolation_forest"]["outlier_count"]
        )

        st.write("Outlier Row Indices:")
        st.write(outliers["isolation_forest"]["outlier_indices"])

    except Exception as e:
        st.error(str(e))