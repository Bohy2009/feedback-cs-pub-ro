# Feedback Summarization

This folder contains scripts for generating summary reports from a `raw.csv` feedback dataset.


## Scripts

- **all-summarize** – Runs all summarization scripts for every dataset.
- **summarize_per_series.py** – Generates summaries grouped by academic year/semester and series.
- **summarize_per_semester.py** – Generates summaries grouped by academic year and semester.
- **summarize_common.py** – Combines all series belonging to the same course.
- **summarize_prof.py** – Generates summaries grouped by professor.

## Usage

Generate all summaries:

```bash
./all-summarize <top-folder>
```

Or run an individual script:

```bash
./summarize_per_series.py raw.csv > per_series.csv
./summarize_per_semester.py raw.csv > per_semester.csv
./summarize_common.py raw.csv > common.csv
./summarize_prof.py raw.csv > prof.csv
```

Each script reads a `raw.csv` file and writes the corresponding summary CSV to standard output.
