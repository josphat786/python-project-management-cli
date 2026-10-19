# Project & Task Management CLI Tool

A modular, object-oriented programming Command-Line Interface (CLI) Tool application built in Python for managing users, projects, and tasks with local JSON data persistence.

## 📁 Project Structure

```text
my_cli_project/
│
├── main.py                  # Entry point using 'argparse' and 'sys' to manage commands
├── requirements.txt         # Lists external package dependencies (rich, pytest)
├── test_app.py              # Suite for testing models, utilities, and CLI validation
├── LICENSE                  # MIT License file
├── README.md                # Application documentation
│
├── data/                    # Contains persistent storage flat files
│   ├── projects.json        # Saved records of all Project objects
│   ├── tasks.json           # Saved records of all Task objects
│   └── users.json           # Saved records of all User objects
│
├── models/
│   ├── __init__.py
│   ├── person.py            # 'Person' base class with name/email properties & re validation
│   ├── user.py              # 'User' class (inherits from Person)
│   ├── project.py           # 'Project' class (manages ALL_PROJECTS registry & serialization)
│   └── task.py              # 'Task' class (handles individual actionable items)
│
└── utils/
    ├── __init__.py
    └── storage.py           # 'Storage' utility for local file reading and writing
```

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have **Python 3.13** installed on your system.

### 2. Installation & Setup

Clone or navigate to your project directory and run the following commands:

```bash
# Create a virtual environment (optional but recommended)
python3.13 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install the required dependencies
pip install -r requirements.txt
```

### 3. Initialize Data Directory

The application expects a `data/` folder in the root directory to store its JSON databases. If it does not exist, create it:

```bash
mkdir data
```

---

## 🛠️ Usage Instructions

The tool uses `argparse` to handle terminal parameters. You can interact with it using various subcommands from your root folder.

### View Available Commands

To look up the global usage guide and see what options are available:

```bash
python main.py --help
```

### Example Commands (Concept Flow)

* **Add a Project:**

    ```bash
    python main.py add-project --title "App Launch" --description "CLI Project Buildout" --due_date "2026-12-31" --user_id 1
    ```

* **List Projects:**

    ```bash
    python main.py list-projects
    ```

---

## 🧪 Running Tests

The application uses `pytest` to validate internal structures, such as email syntax patterns via `re` and collection serialization states (`to_dict` / `from_dict`).

To run the complete test suite, execute:

```bash
pytest test_app.py
```

---

## 📦 Core Architecture Features

* **Data Encapsulation:** The `Person` class enforces read-only attributes for identity properties using Python `@property` patterns.
* **Shared Class Registry:** The `Project` model utilizes a class-level `ALL_PROJECTS` array to retain records inside working memory before serializing down to disk.
* **Visual Formatting:** Features clean, human-scannable console rendering tables and error highlights powered natively by the `rich` ecosystem.

---

## 📄 License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
