#!/usr/bin/env python3
import csv
import sys
from collections import defaultdict

"""
summarize_per_semester.py

Reads the raw feedback CSV file and generates summary statistics grouped by:

    • Academic year (e.g. L-A1, M-A2)
    • Semester (e.g. L-A1-S1, M-A2-S2)

Input:
    raw.csv

Output (stdout):
    CSV containing:
        - Academic year / semester
        - Number of courses
        - Total feedback
        - Feedback percentage
        - Number of users
        - Average evaluation

Usage:
    ./summarize_per_semester.py <raw-feedback-csv-file>
"""

# Aggregation prefixes
YEAR_GROUPS = [
    "L-A1",
    "L-A2",
    "L-A3",
    "L-A4",
    "M-A1",
    "M-A2",
]

SEMESTER_GROUPS = [
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
]


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


def aggregate(data, groups):
    """
    Aggregate statistics for the supplied grouping prefixes.

    Args:
        data: Parsed feedback data.
        groups: List of prefixes to aggregate.

    Returns:
        Dictionary containing aggregated statistics.
    """
    results = defaultdict(lambda: {
        "count": 0,
        "num": 0,
        "users": 0,
        "val": 0.0,
    })

    for course_name, stats in data.items():
        for group in groups:
            if course_name.startswith(group):
                summary = results[group]

                summary["count"] += 1
                summary["num"] += stats["num"]
                summary["users"] += stats["users"]

                # Weighted sum used later to compute the average rating.
                summary["val"] += stats["val"] * stats["num"]

    return results


def print_results(results):
    """Write the aggregated CSV to stdout."""

    print(
        '"an/sem","num_cursuri","num_feedback","proc_feedback","num_utilizatori","evaluare"'
    )

    for group, summary in results.items():
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
            f'"{group}",'
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

    results = aggregate(data, YEAR_GROUPS)
    results.update(aggregate(data, SEMESTER_GROUPS))

    print_results(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
