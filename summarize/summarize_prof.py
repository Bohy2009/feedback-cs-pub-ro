#!/usr/bin/env python3
import csv
import sys
from collections import defaultdict

"""
Reads the raw feedback CSV file and generates summary statistics grouped by
professor.

Input:
    raw.csv

Output (stdout):
    CSV containing:
        - Professor
        - Number of courses
        - Total feedback
        - Feedback percentage
        - Number of users
        - Average evaluation

Usage:
    ./summarize_prof.py <raw-feedback-csv-file>
"""

def load_feedback(filename):
    """
    Load the raw feedback CSV into memory.

    Returns:
        Dictionary indexed by course identifier.
    """
    data = {}

    with open(filename, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            data[row[0]] = {
                "prof": row[1],
                "num": int(row[2]),
                "users": int(row[4]),
                "val": float(row[5]),
            }

    return data


def aggregate(data):
    """
    Aggregate statistics for each professor.

    Returns:
        Dictionary containing summary statistics indexed by professor name.
    """
    results = defaultdict(lambda: {
        "count": 0,
        "num": 0,
        "users": 0,
        "val": 0.0,
    })

    for course_name, stats in data.items():
        professor = stats["prof"]
        summary = results[professor]

        summary["count"] += 1
        summary["num"] += stats["num"]
        summary["users"] += stats["users"]

        # Store a weighted total to compute the final average rating.
        summary["val"] += stats["val"] * stats["num"]

    return results


def print_results(results):
    """Write the aggregated CSV to stdout."""

    print(
        '"prof","num_cursuri","num_feedback","proc_feedback","num_utilizatori","evaluare"'
    )

    for professor, summary in results.items():
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
            f'"{professor}",'
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
