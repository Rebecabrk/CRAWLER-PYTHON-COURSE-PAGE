# CRAWLER-PYTHON-COURSE-PAGE
![image](https://github.com/user-attachments/assets/6e62d66f-4749-41a1-893e-c79dd808b769)

## Project Description

This project is a Python-based crawler designed to extract laboratory problem data from the [Python Course](https://gdt050579.github.io/python-course-fii/administrative.html) page. The crawler automates the creation of a structured directory with Python scripts, each containing placeholder functions for exercises. This tool is ideal for students or educators who want a quick setup for solving or reviewing Python problems.

## Features

- Fetches and parses problem descriptions from the website.
- Creates subdirectories for each lab (e.g., `lab1`, `lab2`, etc.).
- Generates `.py` files (e.g., `lab1.py`, `lab2.py`, etc.) for each lab.
- Includes placeholder functions for each exercise in the lab files.

## How it works

- The crawler downloads and parses the HTML content from the course page.
- Relevant data for labs and exercises are extracted.
- For each lab, a new directory and corresponding .py file are created.
- Placeholder functions are inserted based on the exercise information.

## Usage
```
python crawler.py <output_directory>
```

### Example Output

For a lab containing an exercise `ex1`, the generated file `lab1.py` will contain:

```python
def ex1(param):
    pass
```

