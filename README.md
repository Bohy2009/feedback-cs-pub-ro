# Feedback Analysis

## Overview

This repository contains scripts for automating the retrieval, generation, processing, analysis, and presentation of feedback results exported from a [Moodle](https://moodle.org/) instance.

Originally developed for the [UPB Moodle platform](https://curs.upb.ro), the project can be adapted to work with other Moodle instances with minimal changes.

The repository contains two related components:

- **Feedback Generator** – generates realistic, anonymized student feedback datasets that can be used for testing and validating the processing pipeline without exposing real user data.
- **Feedback Processing Pipeline** – retrieves, processes, analyzes, and summarizes Moodle feedback data, producing statistical reports and aggregated results.

---

# Repository Structure

| Directory / Script | Description |
|--------------------|-------------|
| `analysis/` | Analysis scripts and supporting utilities. |
| `mappings/` | Mapping files used during data processing. |
| `process-feedback/` | Scripts for processing feedback files and generating statistics. |
| `retrieve-feedback/` | Scripts for retrieving feedback data from Moodle. |
| `statistics/` | Statistical analysis scripts. |
| `summarize/` | Scripts for generating summary reports. |
| `create_folder_structure` | Creates the directory structure required by the processing pipeline. |
| `create_faculty_structure` | Creates faculty-specific directory structures. |
| `create_upb_structure` | Creates the directory structure for UPB-wide processing. |
| `pack_structure` | Packages generated files into an archive. |
| `pack_structure_upb` | Packages UPB-specific output files into an archive. |


---

# Feedback Generator

## Purpose

The Feedback Generator creates realistic, anonymized student feedback datasets in JSON format.

Its primary purpose is to provide reliable, non-sensitive datasets for testing and validating the feedback processing and analysis scripts without requiring access to real student feedback.

---

## Generator Structure

| File / Directory | Description |
|------------------|-------------|
| `main.py` | Loads course metadata from Pickle files and generates simulated student feedback. Generated files are stored in `feedback-contents/`. |
| `convert_script.py` | Converts metadata between JSON and Pickle formats. |
| `config.conf` | Stores the generator configuration parameters. |
| `pickles/` | Contains the Pickle metadata files required by the generator. |
| `jsons/` | Contains JSON versions of the metadata. |
| `feedback-contents/` | Automatically created directory containing generated feedback JSON files. |

---

## Required Input Files

Before running the generator, the following Pickle files must exist inside the `pickles/` directory:

- `feedbacks.p`
- `courses.p`
- `categories.p`
- `courses4categories.p`

These files contain:

- Existing feedback definitions
- Course metadata
- Category metadata
- Course-category relationships

---

## Requirements

- Python 3.x

A virtual environment is recommended.

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

### Linux/macOS

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

Deactivate it when finished:

```bash
deactivate
```

---

## Running the Generator

Generate the required Pickle files from JSON metadata:

```bash
python3 convert_script.py
```

Run the generator using the configuration from `config.conf`:

```bash
python3 main.py
```

Or specify a custom interval for the number of generated students:

```bash
python3 main.py --min-students <min> --max-students <max>
```

where:

- `<min>` and `<max>` are positive integers
- `<min> <= <max>`

Generated feedback files will be stored in:

```text
feedback-contents/
```

---

# Feedback Processing Pipeline

## Purpose

The Feedback Processing Pipeline contains scripts for processing feedback exported from the [UPB Moodle platform](https://curs.upb.ro) used at the **National University of Science and Technology POLITEHNICA Bucharest**.

The pipeline converts raw Moodle feedback spreadsheets into processed reports containing aggregated statistics for instructors and teaching assistants.

---

## Prerequisites

The processing scripts require:

- Python 3.x
- Gnumeric package installed on the system

The processing scripts use the `ssconvert` utility provided by Gnumeric.

Verify that `ssconvert` is installed:

```bash
which ssconvert
```

Example output:

```text
/usr/bin/ssconvert
```

---

# Processing Scripts

The `process-feedback` directory contains three main scripts:

| Script | Description |
|--------|-------------|
| `xls2csv.sh` | Converts `.xls` feedback files into `.csv` files. |
| `process_feedback.py` | Processes feedback data and generates statistical results. |
| `csv2xls.sh` | Converts processed `.csv` files back into `.xls` format. |

---

# Preparing the Input Data

Clone the repository:

```bash
git clone https://github.com/cs-pub-ro/feedback.git
```

Navigate to the processing directory:

```bash
cd feedback/process-feedback
```

Create a directory for the course feedback:

```bash
mkdir so2
```

Copy the raw Moodle feedback spreadsheet into this directory.

Example:

```text
so2/
└── SO2 2013-2014 - Feedback studenti - neprelucrat.xls
```

---

# Processing Workflow

The scripts must be executed in the following order.

## 1. Convert Excel files to CSV

```bash
./xls2csv.sh so2/
```

This converts raw `.xls` feedback files into `.csv` format.

---

## 2. Process Feedback

```bash
./process_feedback.py so2/
```

This processes the CSV files and generates a new file:

```text
*-prelucrat.csv
```

containing the calculated feedback statistics.

---

## 3. Convert Results Back to Excel

```bash
./csv2xls.sh so2/
```

This converts the processed CSV file into:

```text
*-prelucrat.xls
```

---

# Output

After running the complete processing pipeline, the directory will contain:

```text
so2/
├── original-feedback.xls
├── original-feedback.csv
├── original-feedback-prelucrat.csv
└── original-feedback-prelucrat.xls
```

The final Excel file contains aggregated numerical results and statistics for instructors and teaching assistants.

---

# Complete Workflow

The complete feedback analysis workflow is:

1. **Obtain feedback data**:
   - Retrieve real feedback data from Moodle, 
    **OR**
   - Generate anonymized feedback datasets using the Feedback Generator if real data is unavailable.
2. Create the required folder structure.
3. Convert feedback spreadsheets to CSV format.
4. Process feedback data.
5. Generate statistics and summaries.
6. Convert processed results back to Excel.
7. Package generated reports if required.
---
# Additional Documentation

For an in-depth explanation of the scripts, parameters, configuration files, and usage examples, please refer to the `README.md` file available inside the folders.

---
# License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

You are free to use, modify, and distribute this software under the terms and conditions of the GPL-3.0 license. Any modified or redistributed versions must also be released under the same license.

See the `LICENSE` file for the full license text.
