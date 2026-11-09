# Library Manager CLI

[![tests](https://github.com/Enricosi/Library-Manager/actions/workflows/tests.yml/badge.svg)](https://github.com/Enricosi/Library-Manager/actions/workflows/tests.yml)

**English** · [Español](README.es.md)

A command-line tool to manage a library's books, physical copies, users and loans, backed by MySQL.

Built with Python, `argparse` and PyMySQL. All queries are parameterized, multi-step writes (like a loan, which inserts the loan and marks the copy as loaned) are committed together, and the rules below are enforced in code and backed by foreign keys and `CHECK` constraints.

## Requirements

- Python 3.8+
- MySQL 8.0.13+

## Setup

```bash
pip install -r requirements.txt

mysql -u <user> -p -e "CREATE DATABASE library_manager"
mysql -u <user> -p library_manager < schema.sql

cp .env.example .env   # then fill in your own values
```

```env
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=library_manager
```

## Usage

```bash
python library_manager.py <command> [arguments]
```

## Commands

### Books

| Command | What it does |
|---|---|
| `add_book TITLE AUTHOR GENRE [-y YEAR] [-n ISBN]` | Add a book (ISBN must be unique) |
| `remove_book ID` | Remove a book. Only if it has no copies |
| `list_book [-t TITLE] [-g GENRE] [-a AUTHOR]` | List books, filters use partial matches |

### Copies

| Command | What it does |
|---|---|
| `add_copy BOOK_ID [-l LOCATION]` | Add a physical copy of an existing book |
| `remove_copy ID` | Remove a copy. Not allowed while it is `loaned` |
| `change_copy_status ID NEW_STATUS` | Set `damaged`, `lost` or `available` (see transitions below) |
| `list_copies [-t TITLE] [-s STATUS]` | List copies with their book title |

Allowed status transitions:

- `available` → `damaged`, `lost`
- `loaned` → `damaged`, `lost` (closes the active loan automatically)
- `damaged` → `available`, `lost`
- `lost` → `available`

A copy only becomes `loaned` through `loan_copy`.

### Users

| Command | What it does |
|---|---|
| `add_user USERNAME FIRST_NAME LAST_NAME` | Register a user (username must be unique) |
| `remove_user USERNAME` | Remove a user. Not allowed with active loans |
| `change_user_activity USERNAME` | Toggle active/inactive. Can't deactivate a user with active loans |
| `list_users [-a \| -i] [-l]` | List users: active, inactive, or only those with active loans |

### Loans

| Command | What it does |
|---|---|
| `loan_copy COPY_ID USERNAME DAYS` | Lend an available copy to an active user for 1 to 60 days |
| `return_copy COPY_ID` | Close the active loan and mark the copy `available` |
| `list_loans [-a \| -t]` | List loans: active or historical (returned) |

```bash
python library_manager.py add_book "1984" "George Orwell" "Dystopia" -y 1949 -n 9780451524935
python library_manager.py add_copy 1 -l "Shelf A3"
python library_manager.py add_user jdoe John Doe
python library_manager.py loan_copy 1 jdoe 14
python library_manager.py list_loans --active
```

## Data model

Four tables: `book`, `copy`, `library_user` and `loan`. A copy belongs to a book, and a loan links a copy to a user. An open loan has no `return_date`. See [`schema.sql`](schema.sql).

## Tests

The tests use a fake database connection, so they run without MySQL:

```bash
pip install -r requirements-dev.txt
pytest
```

They run automatically on every push and pull request with GitHub Actions.

## Project structure

```
library_manager.py   entry point: parse args, open the connection, dispatch
parser.py            argparse subcommands and validation
dispatch.py          maps each command to its handler
commands_book.py     book commands
commands_copy.py     copy commands and status transitions
commands_users.py    user commands
commands_loan.py     loan commands
connect.py           reads .env and opens the MySQL connection
exceptions.py        LibraryManagerError for expected business-rule errors
schema.sql           database schema
tests/               pytest suite
```
