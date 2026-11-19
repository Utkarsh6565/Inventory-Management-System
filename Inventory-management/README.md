# Inventory Management System

A menu-driven Inventory Management System developed using **Python** and **SQLite** as a BCA Fifth Semester academic project.

The application helps users maintain product records and perform common inventory-management operations through a simple terminal interface.

## Features

- **Add products:** Add new products with their name, price and available stock.
- **View inventory:** Display the products stored in the database.
- **Update products:** Modify existing product information.
- **Delete a product:** Remove an individual product from the inventory.
- **Delete multiple products:** Select and delete multiple products in one operation using their product IDs, with a confirmation step.
- **Search products:** Find products by name, including partial-name searches.
- **Low-stock report:** Display products whose stock quantity is at or below the program's configured low-stock limit (currently 5).
- **Total inventory value:** Calculate the total value of the inventory using the product prices and quantities.

## Technologies Used

- **Programming language:** Python
- **Database:** SQLite
- **Database library:** Python's built-in `sqlite3` module
- **Development environment:** Visual Studio Code
- **Interface:** Command-line / terminal

## Project Structure

Your repository may look similar to this:

```text
Inventory-management/
├── main.py              # Main Python program (change this name if yours differs)
├── inventory.db         # SQLite database (optional; see note below)
└── README.md            # Project documentation
```

The exact filenames may differ depending on how the project is organised.

## Requirements

- Windows, macOS or Linux
- Python 3 installed

SQLite support is provided through Python's built-in `sqlite3` module, so a separate SQLite package is normally not required.

## How to Run

1. Download or clone this repository to your computer.
2. Open the project folder in Visual Studio Code or a terminal.
3. Run the Python program:

   ```bash
   python main.py
   ```

   Replace `main.py` with the actual name of your Python file if it is different.

4. Follow the on-screen menu to manage the inventory.

## Database

The application uses SQLite to store product records persistently. The database file is named `inventory.db` in the current project setup. If the program creates the database automatically, the file will be generated when the application is run.

**Important:** If you are sharing the project publicly, do not upload private information or any database containing real personal or confidential business data. For an academic demonstration, you may include a sample database only if it contains non-sensitive sample records. Otherwise, leave the database file out; the application can create a fresh one when run, provided the program is written to do so.

## Academic Project

- **Project title:** Inventory Management System
- **Course:** Bachelor of Computer Applications (BCA)
- **Semester:** Fifth Semester
- **Project author:** Utkarsh Bharti

## Disclaimer

This project was developed for academic and learning purposes. It demonstrates basic Python programming, database operations and inventory-management concepts.
