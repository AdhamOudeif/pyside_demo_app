# Multi-Tool Application

This is a PySide6-based desktop application that provides two main functionalities:
- **Text Editor**: A simple text editor where users can open, edit, and save text files.
- **Student List Creator**: A tool to manage a list of students, including adding and removing student entries. The data is saved to a local JSON file.

## Features

1. **Text Editor**:
   - Open and edit text files.
   - Save text files to your local system.

2. **Student List Creator**:
   - Add student names and addresses.
   - Remove selected students from the list.
   - Data is saved to a local JSON file (`students.json`).

## Requirements

- Python 3.x
- PySide6

To install the required Python packages, run:

```bash
pip install -r requirements.txt
```
## How to Package into a standalone executable that can be run on any computer
```bash
pip install pyinstaller
```

Run the command:
```bash
pyinstaller --onefile --windowed --clean --icon=sample-icon.ico main.py
```



