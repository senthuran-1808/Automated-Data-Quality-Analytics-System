from io import BytesIO
from datetime import datetime

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


class PDFReport:

    @staticmethod
    def generate(
        analysis,
        outliers,
        rules
    ):

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        elements = []

        # ----------------------------------------
        # TITLE
        # ----------------------------------------

        elements.append(
            Paragraph(
                "<b>AI DATA QUALITY REPORT</b>",
                styles["Title"]
            )
        )

        elements.append(
            Paragraph(
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                ),
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 20))

        # ----------------------------------------
        # OVERVIEW
        # ----------------------------------------

        elements.append(
            Paragraph(
                "<b>Dataset Overview</b>",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                f"Rows : {analysis['rows']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Columns : {analysis['columns']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Memory Usage : {analysis['memory_usage_mb']} MB",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Quality Score : {rules['quality_score']}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 15))

        # ----------------------------------------
        # QUALITY SUMMARY
        # ----------------------------------------

        elements.append(
            Paragraph(
                "<b>Data Quality Summary</b>",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                f"Missing Values : {analysis['total_null_values']}",
                styles["Normal"]
            )
        )

        elements.append(
            Paragraph(
                f"Duplicate Rows : {analysis['duplicate_rows']}",
                styles["Normal"]
            )
        )

        affected_outliers = sum(
            1
            for item in outliers["iqr"].values()
            if item["outlier_count"] > 0
        )

        elements.append(
            Paragraph(
                f"Columns with Outliers : {affected_outliers}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 15))

        # ----------------------------------------
        # RECOMMENDATIONS
        # ----------------------------------------

        elements.append(
            Paragraph(
                "<b>Recommendations</b>",
                styles["Heading2"]
            )
        )

        if rules["recommendations"]:

            for rec in rules["recommendations"]:

                elements.append(
                    Paragraph(
                        f"• {rec}",
                        styles["Normal"]
                    )
                )

        else:

            elements.append(
                Paragraph(
                    "Dataset is clean.",
                    styles["Normal"]
                )
            )

        elements.append(Spacer(1, 15))

        # ----------------------------------------
        # WARNINGS
        # ----------------------------------------

        elements.append(
            Paragraph(
                "<b>Warnings</b>",
                styles["Heading2"]
            )
        )

        if rules["warnings"]:

            for warn in rules["warnings"]:

                elements.append(
                    Paragraph(
                        f"• {warn}",
                        styles["Normal"]
                    )
                )

        else:

            elements.append(
                Paragraph(
                    "No warnings detected.",
                    styles["Normal"]
                )
            )

        doc.build(elements)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf
