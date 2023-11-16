import csv
import os

import click
import dbf
from dbfread import DBF
from sqlite_utils import Database


def find_dbf_files(directory):
    if os.path.isfile(directory) and directory.lower().endswith('.dbf'):
        return [directory]
    elif os.path.isdir(directory):
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith('.dbf')]
    else:
        return []


@click.group(help='Load and transfer DBF file')
def dbf_cli():
    pass


@dbf_cli.command(help='Loading the DBF file to sqlite database')
@click.argument("dbf_paths", type=click.Path(exists=True), nargs=-1, required=True)
@click.argument("sqlite_db", nargs=1)
@click.option("--table", help="Table name to use (only valid for single files)")
def to_sqlite(dbf_paths, sqlite_db, table):
    if table and len(dbf_paths) > 1:
        raise click.ClickException("--table only works with a single DBF file")
    db = Database(sqlite_db)
    dbf_files = find_dbf_files(dbf_paths[0])
    for path in dbf_files:
        if table:
            table_name = table
        else:
            table_name = os.path.basename(path)

        dbf_load = dbf.Table(str(path))
        dbf_load.open()
        # columns = dbf_load.field_names
        print("Schema: \n", dbf_load)
        dbf_load.close()

        dbfread_load = DBF(path)

        data_list = []
        with click.progressbar(
                iterable=dbfread_load,
                label=f'Loading record from {path}',
        ) as rows:
            count = 0
            for row in rows:
                count += 1
                data_list.append(row)

        with click.progressbar(
                iterable=dbfread_load.deleted,
                label=f'Loading deleted record from {path}',
        ) as rows:
            count = 0
            for row in rows:
                count += 1
                data_list.append(row)

        try:
            print("Start dumping all records into the database. Please wait!")
            db[table_name].insert_all(data_list)
            print(f"Dump all records to the {table_name} table successfully!")
        except Exception as e:
            print(f"\nSkipping row due to error: {e}")

    db.vacuum()


@dbf_cli.command(help='Loading the DBF file to csv')
@click.argument("dbf_paths", type=click.Path(exists=True), nargs=-1, required=True)
@click.argument("csv_out_dir", nargs=1)
@click.option("--name", help="Table name to use (only valid for single files)")
def to_csv(dbf_paths, csv_out_dir, name):
    if name and len(dbf_paths) > 1:
        raise click.ClickException("--table only works with a single DBF file")
    dbf_files = find_dbf_files(dbf_paths[0])
    for path in dbf_files:
        if name:
            csv_name = name
        else:
            csv_name = os.path.basename(path)

        table = DBF(path)

        # Open (or create) a CSV file and write data to it
        csv_fn = csv_name[:-4] + ".csv"
        csv_file_path = os.path.join(csv_out_dir, csv_fn)

        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file, escapechar='\\', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(table.field_names)  # header row
            with click.progressbar(
                    iterable=table,
                    label=f'Loading record from {path}',
            ) as records:
                for record in records:
                    writer.writerow(list(record.values()))
