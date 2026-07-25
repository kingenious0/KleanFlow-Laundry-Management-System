"""
Database Backup Utility Script for KleanFlow Laundry Management System.

Supports MySQL (via mysqldump) and SQLite database snapshots.
Creates timestamped backup files under `backups/` directory.
"""

import os
import sys
import datetime
import subprocess
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import Config


def run_backup():
    backup_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backups'))
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    db_uri = Config.SQLALCHEMY_DATABASE_URI

    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting KleanFlow Database Backup...")

    if db_uri.startswith("sqlite"):
        # SQLite File Copy Backup
        sqlite_path = db_uri.replace("sqlite:///", "")
        if sqlite_path and os.path.exists(sqlite_path):
            dest_filename = f"kleanflow_backup_{timestamp}.db"
            dest_path = os.path.join(backup_dir, dest_filename)
            shutil.copy2(sqlite_path, dest_path)
            print(f"SUCCESS: SQLite database backup created at: {dest_path}")
            return True
        else:
            print(f"NOTICE: SQLite memory database or file not found at '{sqlite_path}'. Backup skipped.")
            return False
    else:
        # MySQL mysqldump Backup
        host = Config.MYSQL_HOST
        port = str(Config.MYSQL_PORT)
        user = Config.MYSQL_USER
        password = Config.MYSQL_PASSWORD
        dbname = Config.MYSQL_DATABASE

        dest_filename = f"kleanflow_backup_{dbname}_{timestamp}.sql"
        dest_path = os.path.join(backup_dir, dest_filename)

        dump_cmd = [
            "mysqldump",
            f"--host={host}",
            f"--port={port}",
            f"--user={user}",
            f"--password={password}",
            "--single-transaction",
            "--quick",
            dbname
        ]

        try:
            with open(dest_path, "w", encoding="utf-8") as outfile:
                res = subprocess.run(dump_cmd, stdout=outfile, stderr=subprocess.PIPE, text=True)

            if res.returncode == 0:
                print(f"SUCCESS: MySQL database backup created successfully at: {dest_path}")
                return True
            else:
                print(f"ERROR: mysqldump failed with error: {res.stderr}")
                if os.path.exists(dest_path) and os.path.getsize(dest_path) == 0:
                    os.remove(dest_path)
                return False
        except FileNotFoundError:
            print("WARNING: 'mysqldump' executable not found on PATH. Ensure MySQL client utilities are installed.")
            return False
        except Exception as e:
            print(f"ERROR: Backup failed due to exception: {str(e)}")
            return False


if __name__ == '__main__':
    run_backup()
