
# Feedback Processing Scripts

The scripts are designed to be executed through the `all-mappings` script, which runs the entire processing pipeline in the correct order.

The pipeline consists of the following steps:

1. Generate the course-to-professor mapping (`prof_course.py`).
2. Count the number of students enrolled in each course (`num_students_per_course`).
3. Extract user email addresses (`person_email`).
4. Combine feedback statistics with enrollment and professor information (`feedback_course_mapping.py`).
5. Generate complete feedback statistics, including courses with no feedback (`full_feedback_course_mapping.py`).

## Usage

```bash
./all-mappings <top-folder>

