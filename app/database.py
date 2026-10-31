
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "sales.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            transaction_id TEXT PRIMARY KEY,
            order_date TEXT NOT NULL,
            product TEXT NOT NULL,
            category TEXT NOT NULL,
            region TEXT NOT NULL,
            sales_channel TEXT NOT NULL,
            quantity INTEGER,
            unit_price REAL,
            discount_amount REAL,
            status TEXT NOT NULL,
            data_quality_issue TEXT
        )
    """)

    conn.commit()
    conn.close()
