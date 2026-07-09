#!/usr/bin/env python3
import csv
import sys
from collections import defaultdict

"""
Reads the raw feedback CSV file and generates summary statistics grouped by
academic year/semester and series.

Examples of generated groups:
    L-A1-CA
    L-A1-S1-CA
    M-A2-IS

Input:
    raw.csv

Output (stdout):
    CSV containing:
        - Series
        - Number of courses
        - Total feedback
        - Feedback percentage
        - Number of users
        - Average evaluation

Usage:
    ./summarize_per_series.py <raw-feedback-csv-file>
"""

# Supported academic year prefixes.
YEAR_GROUPS = {
    "L-A1",
    "L-A2",
    "L-A3",
    "L-A4",
    "M-A1",
    "M-A2",
}

# Supported semester prefixes.
SEMESTER_GROUPS = {
    "L-A1-S1",
    "L-A1-S2",
    "L-A2-S1",
    "L-A2-S2",
    "L-A3-S1",
    "L-A3-S2",
    "L-A4-S1",
    "L-A4-S2",
    "M-A1-S1",
    "M-A1-S2",
    "M-A2-S1",
    "M-A2-S2",
}

# Valid series names.
SERIES = {
    "CA", "CB", "CC", "CD",
    "AA", "AB", "AC",
    "C1", "C2", "C3", "C4",
    "A", "B",
    "Tehnologia, informaţiei",
    "CTI", "IS",
    "AAC", "ABD", "eGuv",
    "G", "GMRV",
    "IA", "ISI", "MTI",
    "SAS", "SCPD", "SPF",
    "SRIC", "SSA",
    "AII", "CASTR", "IMSA",
}


def load_feedback(filename):
    """
    Load the raw feedback CSV into memory.
    """
    data = {}

    with open(filename, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            data[row[0]] = {
                "num": int(row[2]),
                "users": int(row[4]),
                "val": float(row[5]),
            }

    return data


def aggregate(data):
    """
    Aggregate statistics by year/semester and series.

    Returns:
        Dictionary containing summary statistics.
    """
    results = defaultdict(lambda: {
        "count": 0,
        "num": 0,
        "users": 0,
        "val": 0.0,
    })

    for course_name, stats in data.items():
        parts = course_name.split("-")

        if len(parts) < 4:
            continue

        year_prefix = "-".join(parts[:2])
        semester_prefix = "-".join(parts[:3])
        series = parts[-1]

        if series not in SERIES:
            continue

        prefixes = []

        if year_prefix in YEAR_GROUPS:
            prefixes.append(year_prefix)

        if semester_prefix in SEMESTER_GROUPS:
            prefixes.append(semester_prefix)

        for prefix in prefixes:
            key = f"{prefix}-{series}"
            summary = results[key]

            summary["count"] += 1
            summary["num"] += stats["num"]
            summary["users"] += stats["users"]

            # Store the weighted total for later average calculation.
            summary["val"] += stats["val"] * stats["num"]

    return results


def print_results(results):
    """Write the aggregated CSV to stdout."""

    print(
        '"serie","num_cursuri","num_feedback","proc_feedback","num_utilizatori","evaluare"'
    )

    for key, summary in results.items():
        percentage = (
            100 * summary["num"] / summary["users"]
            if summary["users"]
            else 0
        )

        average = (
            summary["val"] / summary["num"]
            if summary["num"]
            else 0
        )

        print(
            f'"{key}",'
            f'"{summary["count"]}",'
            f'"{summary["num"]}",'
            f'"{percentage:.2f}",'
            f'"{summary["users"]}",'
            f'"{average:.2f}"'
        )


def main():
    """Program entry point."""

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <raw-feedback-csv-file>", file=sys.stderr)
        return 1

    data = load_feedback(sys.argv[1])
    results = aggregate(data)
    print_results(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
