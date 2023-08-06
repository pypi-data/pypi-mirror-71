# Regex Cleaner

This is a simple python package that can be used to clean a verbose regex pattern of the comments and new lines and return the basic underlying pattern.

## Installation

```bash
python -m pip install regex-cleaner
```

## Usage

To clean a regex pattern, simply pass the verbose pattern string to the function `clean_regex`.

```python
pattern = """
    \w\d{3} # Matches any letter followed by 3 digits.
"""
cleaned_regex = clean_regex(pattern)

print(cleaned_regex)
```

```bash
\w\d{3}
```
