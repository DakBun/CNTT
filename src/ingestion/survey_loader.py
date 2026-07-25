"""Ingestion utilities for survey data."""

from pathlib import Path

import pandas as pd

from src.config import SURVEY_YEARS, COLUMN_MAPPING


def load_survey(year: int, path: str) -> None:
    """Load Stack Overflow Developer Survey data for a given year.

    Args:
        year: Survey year (e.g., 2019-2025).
        path: Path to the survey dataset file.

    Returns:
        None
    """
    raise NotImplementedError


def load_single_year(year: int) -> pd.DataFrame:
    """Load one survey year and tag rows with survey_year.

    Args:
        year: Survey year to load (must be in SURVEY_YEARS).

    Returns:
        pd.DataFrame: Raw data for the requested year with an added
        `survey_year` column.
    """
    path = SURVEY_YEARS[year]
    df = pd.read_csv(path)
    df["survey_year"] = year
    return df


def load_all_years(years: list[int]) -> pd.DataFrame:
    """Load multiple survey years and concatenate them with renamed columns.

    Only columns present in COLUMN_MAPPING are renamed; others remain as-is.

    Args:
        years: List of survey years to load.

    Returns:
        pd.DataFrame: Combined DataFrame across requested years with
        normalized column names defined in COLUMN_MAPPING.
    """
    frames = []
    for year in years:
        df = load_single_year(year)
        df = df.rename(columns=COLUMN_MAPPING)
        frames.append(df)
    combined = pd.concat(frames, ignore_index=True)
    return combined
