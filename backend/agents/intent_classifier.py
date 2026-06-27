class IntentClassifier:

    @staticmethod
    def classify(question: str):

        q = question.lower()

        # ---------------- Summary ----------------

        if any(word in q for word in [
            "summary",
            "summarize",
            "overview",
            "describe"
        ]):
            return "summary"

        # ---------------- Missing ----------------

        if any(word in q for word in [
            "missing",
            "null",
            "nan",
            "empty"
        ]):
            return "missing"

        # ---------------- Duplicate ----------------

        if any(word in q for word in [
            "duplicate",
            "duplicates"
        ]):
            return "duplicate"

        # ---------------- Outliers ----------------

        if any(word in q for word in [
            "outlier",
            "outliers",
            "iqr",
            "zscore"
        ]):
            return "outlier"

        # ---------------- Statistics ----------------

        if any(word in q for word in [
            "mean",
            "median",
            "variance",
            "statistics",
            "std",
            "skew",
            "kurtosis"
        ]):
            return "statistics"

        # ---------------- Correlation ----------------

        if any(word in q for word in [
            "correlation",
            "relationship"
        ]):
            return "correlation"

        # ---------------- Scaling ----------------

        if any(word in q for word in [
            "scale",
            "scaling",
            "normalize",
            "standardize"
        ]):
            return "scaling"

        # ---------------- Encoding ----------------

        if any(word in q for word in [
            "encode",
            "encoding",
            "label",
            "one hot"
        ]):
            return "encoding"

        # ---------------- Cleaning ----------------

        if any(word in q for word in [
            "clean",
            "cleaning",
            "improve"
        ]):
            return "cleaning"

        # ---------------- ML ----------------

        if any(word in q for word in [
            "machine learning",
            "ml",
            "feature",
            "model"
        ]):
            return "ml"

        return "general"
