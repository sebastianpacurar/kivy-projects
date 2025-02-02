import os
import sqlite3
from utils import find_project_root

saved_colors_db_path = os.path.join(find_project_root(), 'backend', 'color_picker_project', 'dbs', 'saved_colors.db')


def create_db():
    with sqlite3.connect(saved_colors_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Colors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rgb TEXT,
            hex TEXT
        )
        ''')
        conn.commit()


def insert_color(rgb, hex_val):
    with sqlite3.connect(saved_colors_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Colors (rgb, hex) VALUES (?, ?)", (rgb, hex_val))
        conn.commit()


def select_all_colors():
    with sqlite3.connect(saved_colors_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Colors")
        return cursor.fetchall()