from datetime import datetime


class ReportGenerator:

    @staticmethod
    def generate(
        analysis,
        outliers,
        rules
    ):

        report = f"""
========================================================
        Automated Data Quality & Analytics System
========================================================

Generated : {datetime.now().strftime("%d-%m-%Y %H:%M")}

--------------------------------------------------------
DATASET OVERVIEW
--------------------------------------------------------

Rows              : {analysis["rows"]}

Columns           : {analysis["columns"]}

Memory Usage      : {analysis["memory_usage_mb"]} MB

Quality Score     : {rules["quality_score"]}

--------------------------------------------------------
DATA QUALITY
--------------------------------------------------------

Missing Values    : {analysis["total_null_values"]}

Duplicate Rows    : {analysis["duplicate_rows"]}

Outlier Columns   : {len(outliers["iqr"])}

--------------------------------------------------------
RECOMMENDATIONS
--------------------------------------------------------
"""

        for rec in rules["recommendations"]:
            report += f"\n✔ {rec}"

        return report