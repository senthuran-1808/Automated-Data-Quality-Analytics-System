from pathlib import Path

import chardet
import pandas as pd


class DatasetLoader:

    SUPPORTED_FILES = {
        ".csv",
        ".xlsx",
        ".xls",
        ".txt",
        ".tsv"
    }

    @staticmethod
    def detect_encoding(file):

        raw = file.read(100000)

        file.seek(0)

        result = chardet.detect(raw)

        return result["encoding"] or "utf-8"

    @staticmethod
    def detect_delimiter(file, encoding):

        sample = file.read(5000).decode(
            encoding,
            errors="ignore"
        )

        file.seek(0)

        delimiters = [
            ",",
            ";",
            "|",
            "\t"
        ]

        scores = {}

        for delimiter in delimiters:
            scores[delimiter] = sample.count(delimiter)

        return max(scores, key=scores.get)

    @classmethod
    def load(cls, file):

        extension = Path(file.name).suffix.lower()

        if extension not in cls.SUPPORTED_FILES:
            raise ValueError(
                "Unsupported file format."
            )

        if extension in [".xlsx", ".xls"]:

            return pd.read_excel(file)

        encoding = cls.detect_encoding(file)

        delimiter = cls.detect_delimiter(
            file,
            encoding
        )

        return pd.read_csv(
            file,
            encoding=encoding,
            sep=delimiter
        )
