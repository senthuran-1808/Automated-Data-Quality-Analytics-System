import pandas as pd


class RuleEngine:

    @staticmethod
    def evaluate(analysis: dict, df: pd.DataFrame) -> dict:

        rules_output = {
            "warnings": [],
            "recommendations": [],
            "quality_flags": []
        }

        rows = analysis["rows"]

        missing_values = analysis["missing_values"]
        missing_percentage = analysis["missing_percentage"]

        duplicates = analysis["duplicate_rows"]
        duplicate_pct = analysis["duplicate_percentage"]

        data_types = analysis["data_types"]

        # ---------------- Rule 1: High Missing Values ----------------
        for col, pct in missing_percentage.items():

            if pct > 70:
                rules_output["warnings"].append(
                    f"{col} has very high missing values ({pct}%)."
                )
                rules_output["recommendations"].append(
                    f"Consider dropping column '{col}' or heavy imputation."
                )

            elif pct > 30:
                rules_output["warnings"].append(
                    f"{col} has moderate missing values ({pct}%)."
                )
                rules_output["recommendations"].append(
                    f"Impute missing values in '{col}'."
                )

        # ---------------- Rule 2: Duplicate Rows ----------------
        if duplicate_pct > 10:
            rules_output["warnings"].append(
                f"High duplicate rows detected ({duplicate_pct}%)."
            )
            rules_output["recommendations"].append(
                "Remove duplicate records before training."
            )

        elif duplicates > 0:
            rules_output["warnings"].append(
                f"{duplicates} duplicate rows found."
            )
            rules_output["recommendations"].append(
                "Deduplicate dataset."
            )

        # ---------------- Rule 3: Constant Columns ----------------
        for col in df.columns:

            if df[col].nunique(dropna=True) == 1:
                rules_output["warnings"].append(
                    f"{col} is a constant column."
                )
                rules_output["recommendations"].append(
                    f"Remove '{col}' (no variance)."
                )

        # ---------------- Rule 4: High Cardinality ----------------
        for col, unique in analysis["unique_values"].items():

            if rows > 0 and unique / rows > 0.9:
                rules_output["warnings"].append(
                    f"{col} has very high cardinality."
                )
                rules_output["recommendations"].append(
                    f"Check encoding strategy for '{col}'."
                )

        # ---------------- Rule 5: Memory Usage ----------------
        if analysis["memory_usage_mb"] > 100:
            rules_output["warnings"].append(
                "Dataset is large in memory usage."
            )
            rules_output["recommendations"].append(
                "Consider downcasting data types."
            )

        # ---------------- Quality Score (Simple Heuristic) ----------------
        score = 100

        score -= min(30, duplicate_pct * 2)
        score -= min(30, sum(missing_percentage.values()) / len(missing_percentage))

        rules_output["quality_score"] = round(max(score, 0), 2)

        # ---------------- Final Flag ----------------
        if rules_output["quality_score"] > 80:
            rules_output["quality_flags"].append("GOOD")
        elif rules_output["quality_score"] > 50:
            rules_output["quality_flags"].append("MODERATE")
        else:
            rules_output["quality_flags"].append("POOR")

        return rules_output
