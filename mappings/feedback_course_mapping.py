#!/usr/bin/env python

import csv
import sys


def main():
    # Check that the required input files were provided.
    if len(sys.argv) != 4:
        sys.stderr.write(
            "Usage: {} <raw-feedback-csv-file> <num-user-csv-file> <prof-courses-csv-file>\n".format(sys.argv[0])
        )
        sys.exit(1)

    # Read the number of enrolled users for each course.
    num_users = {}
    with open(sys.argv[2], "rt") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in reader:
            num_users[row[0]] = int(row[1])

    # Read the professor assigned to each course.
    prof_courses = {}
    with open(sys.argv[3], "rt") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in reader:
            prof_courses[row[0]] = row[1]

    # Read the feedback data and compute participation statistics.
    res = {}
    with open(sys.argv[1], "rt") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in reader:
            course = row[0]
            num = int(row[1])
            val = float(row[2])

            if course not in num_users:
                sys.stderr.write("Error: Course {} absent.\n".format(course))
                sys.exit(1)

            res[course] = {
                "prof": prof_courses[course],
                "num": num,
                "users": num_users[course],
                "perc": (100.0 * num) / num_users[course],
                "val": val,
            }

    # Output the combined statistics as CSV.
    for course in res:
        print(
            "\"{}\",\"{}\",\"{:d}\",\"{:4.2f}\",\"{:d}\",\"{:3.2f}\"".format(
                course,
                res[course]["prof"],
                res[course]["num"],
                res[course]["perc"],
                res[course]["users"],
                res[course]["val"],
            )
        )


if __name__ == "__main__":
    sys.exit(main())
