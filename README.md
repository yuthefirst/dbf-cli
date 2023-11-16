# dbf-cli

CLI tool for converting DBF files (dBase, FoxPro etc) to SQLite.

## Installation

    pip install -e .

## Usage

    $ dbf-cli --help
    Usage: dbf-cli [OPTIONS] COMMAND [ARGS]...

    Load and transfer DBF file

    Options:
      --help  Show this message and exit.

    Commands:
      to-csv     Loading the DBF file to csv
      to-sqlite  Loading the DBF file to sqlite database

Example usage:

    $ dbf-cli to_csv path/to/dbf-file path/to/output/csv

or

    $ dbf-cli to_csv path/to/file.dbf path/to/output/csv

This will create a new `csv` file for each of the `.DBF` or `.dbf` files in the current directory with the same name of the `dbf` file.

    $ dbf-cli to_sqlite path/to/dbf-file path/to/output/database.db

or

    $ dbf-cli to_csv path/to/file.dbf path/to/output/database.db

This will create a new SQLite database called `database.db` containing one table for each of the `.DBF` or `.dbf` files in the current directory.

Looking for DBF files to try this out on? Try downloading the [Himalayan Database](http://himalayandatabase.com/) of all expeditions that have climbed in the Nepal Himalaya.
