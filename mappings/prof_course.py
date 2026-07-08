#!/usr/bin/env python

import csv
import sys


def main():
    # Check that the input file was provided.
    if len(sys.argv) != 2:
        sys.stderr.write(
            "Usage: {} <courses-profs-file>\n".format(sys.argv[0])
        )
        sys.exit(1)

    in_file = sys.argv[1]
    d = {}

    # Read the course-professor assignments and keep the professor
    # associated with the largest value in the third column.
    with open(in_file, "rt") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in reader:
            course = row[0]
            prof = row[1]
            num = row[2]

            if course in d and d[course]["num"] > num:
                continue

            d[course] = {
                "prof": prof,
                "num": num,
            }

    # Output the final course-to-professor mapping.
    for course in d:
        print("\"{}\",\"{}\"".format(course, d[course]["prof"]))


if __name__ == "__main__":
    sys.exit(main())
