class PromptBuilder:

    @staticmethod
    def _dict_to_table(title, data):

        if not data:
            return f"{title}\nNone\n"

        text = f"{title}\n"
        text += "-" * 40 + "\n"

        for key, value in data.items():
            text += f"{key}: {value}\n"

        text += "\n"

        return text

    @staticmethod
    def build(
        question,
        analysis,
        stats,
        outliers,
        rules,
        intent
    ):
        
        
        prompt = f"""

Detected Intent : {intent}

You are an Enterprise AI Data Quality Analyst.

Rules:

• Never invent values.
• Use ONLY the supplied dataset analysis.
• Never estimate statistics.
• Keep answers concise.
• Use bullet points.
• Do not repeat information.
• Do not explain basic data science concepts unless asked.
• If information is unavailable, reply "Not Available".
• Prefer actionable recommendations.

==================================================
DATASET OVERVIEW
==================================================

Rows : {analysis['rows']}

Columns : {analysis['columns']}

Duplicate Rows : {analysis['duplicate_rows']}

Total Missing Values : {analysis['total_null_values']}

Memory Usage : {analysis['memory_usage_mb']} MB

Quality Score : {rules['quality_score']}

==================================================

{PromptBuilder._dict_to_table(
"Missing Values",
analysis["missing_values"]
)}

{PromptBuilder._dict_to_table(
"Missing Percentage",
analysis["missing_percentage"]
)}

{PromptBuilder._dict_to_table(
"Data Types",
analysis["data_types"]
)}

{PromptBuilder._dict_to_table(
"Unique Values",
analysis["unique_values"]
)}

{PromptBuilder._dict_to_table(
"Mean",
stats.get("mean", {})
)}

{PromptBuilder._dict_to_table(
"Median",
stats.get("median", {})
)}

{PromptBuilder._dict_to_table(
"Variance",
stats.get("variance", {})
)}

{PromptBuilder._dict_to_table(
"Standard Deviation",
stats.get("std_dev", {})
)}

{PromptBuilder._dict_to_table(
"Skewness",
stats.get("skewness", {})
)}

{PromptBuilder._dict_to_table(
"Kurtosis",
stats.get("kurtosis", {})
)}

{PromptBuilder._dict_to_table(
"IQR Outliers",
outliers.get("iqr", {})
)}

{PromptBuilder._dict_to_table(
"Z-Score Outliers",
outliers.get("zscore", {})
)}

Warnings

{rules["warnings"]}

Recommendations

{rules["recommendations"]}

==================================================
USER QUESTION
==================================================

{question}

==================================================

==================================================
RESPONSE FORMAT (MANDATORY)
==================================================

Respond ONLY in the following format.

## Summary
Provide a short summary in 2-3 lines.

## Findings
- Finding 1
- Finding 2
- Finding 3

## Issues
- Issue 1
- Issue 2

If there are no issues write:
No major issues detected.

## Recommendations
- Recommendation 1
- Recommendation 2
- Recommendation 3

Keep every point short.

Never write long paragraphs.

Never repeat information.

Maximum response length: 180 words.

If the user asks only one question (example: "How many duplicates?"),
answer ONLY that question in one short paragraph and do not include other sections.

==================================================
USER QUESTION
==================================================

{question}

"""
        return prompt