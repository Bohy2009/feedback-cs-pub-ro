#!/usr/bin/env python3
import csv
import re
import sys
from collections import defaultdict

"""
Reads the raw feedback CSV file and aggregates statistics for each course,
combining all series into a single summary.

Input:
    raw.csv

Output (stdout):
    CSV containing:
        - Course
        - Number of course instances
        - Total feedback count
        - Feedback percentage
        - Number of users
        - Average evaluation

Usage:
    ./summarize_common.py <raw-feedback-csv-file>
"""

# Matches course identifiers such as:
#   L-A1-S1-POO
#   M-A2-S2-IA
COURSE_PATTERN = re.compile(r"[LM]-A[1-4]-S[1-2]-[^-]+")


def load_feedback(filename):
    """
    Load the raw feedback CSV into a dictionary indexed by course identifier.
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


def aggregate_courses(data):
    """
    Aggregate all series belonging to the same course.

    Returns:
        Dictionary containing summarized statistics.
    """
    results = defaultdict(lambda: {
        "name": "",
        "count": 0,
        "num": 0,
        "users": 0,
        "val": 0.0,
    })

    for course_name, stats in data.items():
        match = COURSE_PATTERN.match(course_name)

        if not match:
            continue

        course = match.group(0)
        summary = results[course]

        summary["name"] = f"{course}-all"
        summary["count"] += 1
        summary["num"] += stats["num"]
        summary["users"] += stats["users"]

        # Keep a weighted sum to compute the final average.
        summary["val"] += stats["val"] * stats["num"]

    return results


def print_results(results):
    """Write the aggregated CSV to stdout."""

    print(
        '"curs","num_cursuri","num_feedback","proc_feedback","num_utilizatori","evaluare"'
    )

    for summary in results.values():
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
            f'"{summary["name"]}",'
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
    results = aggregate_courses(data)
    print_results(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
