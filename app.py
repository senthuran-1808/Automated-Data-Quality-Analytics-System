import streamlit as st
import pandas as pd

from backend.loaders.dataset_loader import DatasetLoader
from backend.analysis.data_analyzer import DataAnalyzer
from backend.analysis.statistics_analyzer import StatisticsAnalyzer
from backend.analysis.outlier_analyzer import OutlierAnalyzer
from backend.rules.rule_engine import RuleEngine
from backend.visualization.visualizer import Visualizer
from backend.ai.ai_agent import AIAgent
from backend.reports.report_generator import ReportGenerator
from backend.reports.pdf_report import PDFReport


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Automated Data Quality & Analytics System",
    page_icon="🤖",
    layout="wide"
)


# ==========================================================
# TITLE
# ==========================================================

st.title("Automated Data Quality & Analytics System")
st.caption("Enterprise Data Quality & AI Analysis Platform")


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Dashboard",
        "Dataset Overview",
        "Statistics",
        "Data Quality",
        "Visualizations",
        "AI Assistant",
        "Reports"
    ]
)

st.sidebar.divider()

uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset",
    type=[
        "csv",
        "xlsx",
        "xls",
        "txt",
        "tsv"
    ]
)


# ==========================================================
# NO DATA
# ==========================================================

if uploaded_file is None:

    st.info("Please upload a dataset from the left sidebar.")

    st.stop()


# ==========================================================
# LOAD DATA
# ==========================================================

try:

    df = DatasetLoader.load(uploaded_file)

    analysis = DataAnalyzer.analyze(df)

    stats = StatisticsAnalyzer.analyze(df)

    outliers = OutlierAnalyzer.analyze(df)

    rules = RuleEngine.evaluate(
        analysis,
        df
    )

except Exception as e:

    st.error(e)

    st.stop()


# ==========================================================
# FILTER DATA
# ==========================================================

missing_df = pd.DataFrame({

    "Column": list(analysis["missing_values"].keys()),

    "Missing Values": list(analysis["missing_values"].values()),

    "Missing %": list(analysis["missing_percentage"].values())

})

missing_df = missing_df[
    missing_df["Missing Values"] > 0
]


datatype_df = pd.DataFrame(

    analysis["data_types"].items(),

    columns=[
        "Column",
        "Datatype"
    ]

)


unique_df = pd.DataFrame({

    "Column": list(
        analysis["unique_values"].keys()
    ),

    "Unique Values": list(
        analysis["unique_values"].values()
    )

})


# ==========================================================
# OUTLIER TABLE
# ==========================================================

iqr_df = pd.DataFrame([

    {

        "Column": col,

        "Outliers": info["outlier_count"],

        "Lower Bound": info["lower_bound"],

        "Upper Bound": info["upper_bound"]

    }

    for col, info in outliers["iqr"].items()

])

iqr_df = iqr_df[
    iqr_df["Outliers"] > 0
]


zscore_df = pd.DataFrame([

    {

        "Column": col,

        "Outliers": info["outlier_count"],

        "Threshold": info.get("threshold", 3)

    }

    for col, info in outliers["zscore"].items()

])

zscore_df = zscore_df[
    zscore_df["Outliers"] > 0
]


# ==========================================================
# DASHBOARD
# ==========================================================

if page == "Dashboard":

    st.header("Dashboard")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Rows",
        analysis["rows"]
    )

    c2.metric(
        "Columns",
        analysis["columns"]
    )

    c3.metric(
        "Missing Cells",
        analysis["total_null_values"]
    )

    c4.metric(
        "Duplicate Rows",
        analysis["duplicate_rows"]
    )

    c5.metric(
        "Quality Score",
        rules["quality_score"]
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("Dataset Summary")

        st.write(f"Rows : **{analysis['rows']}**")

        st.write(f"Columns : **{analysis['columns']}**")

        st.write(f"Memory Usage : **{analysis['memory_usage_mb']} MB**")

        st.write(f"Quality : **{rules['quality_flags'][0]}**")

    with right:

        st.subheader("Detected Issues")

        if len(missing_df):

            st.error(
                f"Missing Columns : {len(missing_df)}"
            )

        else:

            st.success(
                "No Missing Values"
            )

        if analysis["duplicate_rows"]:

            st.error(
                f"Duplicate Rows : {analysis['duplicate_rows']}"
            )

        else:

            st.success(
                "No Duplicate Rows"
            )

        if len(iqr_df):

            st.error(
                f"Columns with Outliers : {len(iqr_df)}"
            )

        else:

            st.success(
                "No Outliers"
            )

    st.divider()

    st.subheader("Top Recommendations")

    if rules["recommendations"]:

        for rec in rules["recommendations"]:

            st.info(rec)

    else:

        st.success(
            "Dataset looks good."
        )




# ==========================================================
# DATASET OVERVIEW
# ==========================================================

elif page == "Dataset Overview":

    st.header("Dataset Overview")

    tab1, tab2, tab3 = st.tabs([
        "Dataset",
        "Data Types",
        "Unique Values"
    ])

    # ---------------- Dataset ----------------

    with tab1:

        st.subheader("Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True,
            height=500
        )

        st.divider()

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Rows",
            analysis["rows"]
        )

        c2.metric(
            "Columns",
            analysis["columns"]
        )

        c3.metric(
            "Memory Usage",
            f'{analysis["memory_usage_mb"]} MB'
        )

    # ---------------- Data Types ----------------

    with tab2:

        st.subheader("Column Data Types")

        st.dataframe(
            datatype_df,
            use_container_width=True,
            hide_index=True
        )

    # ---------------- Unique Values ----------------

    with tab3:

        st.subheader("Unique Values")

        search = st.text_input(
            "Search Column",
            ""
        )

        if search:

            temp = unique_df[
                unique_df["Column"].str.contains(
                    search,
                    case=False
                )
            ]

            st.dataframe(
                temp,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.dataframe(
                unique_df,
                use_container_width=True,
                hide_index=True
            )


# ==========================================================
# STATISTICS
# ==========================================================

elif page == "Statistics":

    st.header("Statistical Analysis")

    if "message" in stats:

        st.warning(stats["message"])

    else:

        with st.expander("Mean", expanded=False):

            mean_df = pd.DataFrame(
                stats["mean"].items(),
                columns=[
                    "Column",
                    "Mean"
                ]
            )

            st.dataframe(
                mean_df,
                use_container_width=True,
                hide_index=True
            )

        with st.expander("Median", expanded=False):

            median_df = pd.DataFrame(
                stats["median"].items(),
                columns=[
                    "Column",
                    "Median"
                ]
            )

            st.dataframe(
                median_df,
                use_container_width=True,
                hide_index=True
            )

        with st.expander("Variance", expanded=False):

            variance_df = pd.DataFrame(
                stats["variance"].items(),
                columns=[
                    "Column",
                    "Variance"
                ]
            )

            st.dataframe(
                variance_df,
                use_container_width=True,
                hide_index=True
            )

        with st.expander("Standard Deviation", expanded=False):

            std_df = pd.DataFrame(
                stats["std_dev"].items(),
                columns=[
                    "Column",
                    "Std Dev"
                ]
            )

            st.dataframe(
                std_df,
                use_container_width=True,
                hide_index=True
            )

        with st.expander("Skewness", expanded=False):

            skew_df = pd.DataFrame(
                stats["skewness"].items(),
                columns=[
                    "Column",
                    "Skewness"
                ]
            )

            st.dataframe(
                skew_df,
                use_container_width=True,
                hide_index=True
            )

        with st.expander("Kurtosis", expanded=False):

            kurt_df = pd.DataFrame(
                stats["kurtosis"].items(),
                columns=[
                    "Column",
                    "Kurtosis"
                ]
            )

            st.dataframe(
                kurt_df,
                use_container_width=True,
                hide_index=True
            )

        with st.expander("Correlation Matrix", expanded=True):

            st.dataframe(
                pd.DataFrame(
                    stats["correlation"]
                ),
                use_container_width=True
            )


# ==========================================================
# DATA QUALITY
# ==========================================================

elif page == "Data Quality":

    st.header("Data Quality Analysis")

    # ---------------- SCORE ----------------

    st.metric(
        "Overall Quality Score",
        rules["quality_score"],
        rules["quality_flags"][0]
    )

    st.divider()

    # ---------------- Missing ----------------

    st.subheader("Missing Values")

    if missing_df.empty:

        st.success(
            "No Missing Values Found."
        )

    else:

        st.dataframe(
            missing_df,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # ---------------- Duplicate ----------------

    st.subheader("Duplicate Rows")

    if analysis["duplicate_rows"] == 0:

        st.success(
            "No Duplicate Rows Found."
        )

    else:

        st.error(
            f'Duplicate Rows : {analysis["duplicate_rows"]}'
        )

    st.divider()

    # ---------------- IQR ----------------

    st.subheader("IQR Outliers")

    if iqr_df.empty:

        st.success(
            "No Outliers Found."
        )

    else:

        st.dataframe(
            iqr_df,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # ---------------- Z Score ----------------

    st.subheader("Z-Score Outliers")

    if zscore_df.empty:

        st.success(
            "No Outliers Found."
        )

    else:

        st.dataframe(
            zscore_df,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # ---------------- Isolation Forest ----------------

    st.subheader("Isolation Forest")

    st.metric(
        "Detected Outliers",
        outliers["isolation_forest"]["outlier_count"]
    )

    with st.expander("Outlier Row Indices"):

        st.write(
            outliers["isolation_forest"]["outlier_indices"]
        )

    st.divider()

    # ---------------- Warnings ----------------

    st.subheader("Warnings")

    if rules["warnings"]:

        for warning in rules["warnings"]:

            st.warning(warning)

    else:

        st.success(
            "No Warnings."
        )

    st.divider()

    # ---------------- Recommendations ----------------

    st.subheader("Recommendations")

    if rules["recommendations"]:

        for rec in rules["recommendations"]:

            st.info(rec)

    else:

        st.success(
            "No Recommendations."
        )

# ==========================================================
# VISUALIZATIONS
# ==========================================================

elif page == "Visualizations":

    st.header("Data Visualizations")

    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # ===============================================
    # Missing Value Chart
    # ===============================================

    st.subheader("Missing Values")

    fig = Visualizer.missing_value_chart(df)

    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No Missing Values Found.")

    st.divider()

    # ===============================================
    # Correlation Heatmap
    # ===============================================

    st.subheader("Correlation Heatmap")

    fig = Visualizer.correlation_heatmap(df)

    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No Numeric Columns Available.")

    st.divider()

    # ===============================================
    # Histogram
    # ===============================================

    st.subheader("Histogram")

    if len(numeric_columns) > 0:

        hist_col = st.selectbox(
            "Select Histogram Column",
            numeric_columns,
            key="histogram_column"
        )

        fig = Visualizer.histogram(df, hist_col)

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.info("No Numeric Columns Available.")

    st.divider()

    # ===============================================
    # Box Plot
    # ===============================================

    st.subheader("Box Plot")

    if len(numeric_columns) > 0:

        box_col = st.selectbox(
            "Select Box Plot Column",
            numeric_columns,
            key="boxplot_column"
        )

        fig = Visualizer.boxplot(df, box_col)

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.info("No Numeric Columns Available.")

    st.divider()

    # ===============================================
    # Scatter Plot
    # ===============================================

    st.subheader("Scatter Plot")

    if len(numeric_columns) >= 2:

        col1, col2 = st.columns(2)

        with col1:
            x_axis = st.selectbox(
                "X Axis",
                numeric_columns,
                key="scatter_x"
            )

        with col2:
            y_axis = st.selectbox(
                "Y Axis",
                numeric_columns,
                index=1,
                key="scatter_y"
            )

        fig = Visualizer.scatter(df, x_axis, y_axis)

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.info("Need at least two numeric columns.")

    st.divider()

    # ===============================================
    # Pie Chart
    # ===============================================

    st.subheader("Pie Chart")

    if len(categorical_columns) > 0:

        pie_col = st.selectbox(
            "Select Category Column",
            categorical_columns,
            key="pie_column"
        )

        fig = Visualizer.pie_chart(df, pie_col)

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.info("No Categorical Columns Available.")

# ==========================================================
# AI ASSISTANT
# ==========================================================

elif page == "AI Assistant":

    # -------------------------------------------------------
    # SESSION STATE
    # -------------------------------------------------------

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -------------------------------------------------------
    # AI INSIGHTS
    # -------------------------------------------------------

    st.subheader("AI Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Dataset Summary", use_container_width=True):

            with st.spinner("Generating Summary..."):

                response = AIAgent.summarize_dataset(
                    analysis,
                    stats,
                    outliers,
                    rules
                )

            st.success("Dataset Summary")

            st.markdown(response)

    with col2:
        if st.button("🧹 Cleaning Plan", use_container_width=True):

            with st.spinner("Generating Cleaning Plan..."):

                response = AIAgent.cleaning_plan(
                    analysis,
                    stats,
                    outliers,
                    rules
                )

            st.success("Cleaning Plan")

            st.markdown(response)

    with col3:
        if st.button("🤖 ML Readiness", use_container_width=True):

            with st.spinner("Evaluating Dataset..."):

                response = AIAgent.ml_readiness(
                    analysis,
                    stats,
                    outliers,
                    rules
                )

            st.success("Machine Learning Readiness")

            st.markdown(response)

    st.divider()

    # -------------------------------------------------------
    # SUGGESTED QUESTIONS
    # -------------------------------------------------------

    st.subheader("Suggested Questions")

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button("Summarize Dataset"):
            prompt = "Summarize this dataset."

        elif st.button("Missing Values"):
            prompt = "Which columns contain missing values?"

        else:
            prompt = None

    with c2:

        if st.button("Outliers"):
            prompt = "Which columns contain outliers?"

        elif st.button("Improve Quality"):
            prompt = "How can I improve dataset quality?"

    with c3:

        if st.button("Statistics"):
            prompt = "Explain the statistics."

        elif st.button("Feature Engineering"):
            prompt = "Suggest feature engineering techniques."

    # -------------------------------------------------------
    # DISPLAY CHAT HISTORY
    # -------------------------------------------------------

    st.subheader("💬 Chat")

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # -------------------------------------------------------
    # USER INPUT
    # -------------------------------------------------------

    question = st.chat_input(
        "Ask anything about your dataset..."
    )

    if question:
        prompt = question

    # -------------------------------------------------------
    # AI RESPONSE
    # -------------------------------------------------------

    if "prompt" in locals() and prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Analyzing Dataset..."):

                answer = AIAgent.ask(
                    prompt,
                    analysis,
                    stats,
                    outliers,
                    rules
                )

                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    st.divider()

    # -------------------------------------------------------
    # CLEAR CHAT
    # -------------------------------------------------------

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# -------------------------------------------------------
# REPORT
# -------------------------------------------------------


elif page == "Reports":

    st.header("📄 AI Report Generator")

    pdf = PDFReport.generate(

        analysis,

        outliers,

        rules

    )

    st.success("Professional report is ready.")

    st.download_button(

        label="⬇ Download PDF Report",

        data=pdf,

        file_name="Dataset Summary Report",

        mime="application/pdf"

    )