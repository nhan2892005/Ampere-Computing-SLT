import os
import sqlite3

from contextlib import contextmanager

DB_PATH = os.environ.get("DB_PATH", "initial.db")

_memory_conn = None


def _get_memory_conn():
    global _memory_conn
    if _memory_conn is None:
        _memory_conn = sqlite3.connect(":memory:", check_same_thread=False)
        _memory_conn.row_factory = sqlite3.Row
    return _memory_conn

@contextmanager
def get_db():
    if DB_PATH == ":memory:":
        yield _get_memory_conn()
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

def query_db(sql, params={}):
    with get_db() as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]

def init_db():
    with get_db() as conn:
        with open("initial_db.sql") as f:
            conn.executescript(f.read())

        if conn.execute("SELECT COUNT(*) FROM facility").fetchone()[0]:
            return

        conn.executescript("""
            INSERT OR IGNORE INTO facility (id, name, location) VALUES
                (1, 'HN',  'Ha Noi'),
                (2, 'DN',  'Da Nang'),
                (3, 'HCM', 'Ho Chi Minh');

            INSERT OR IGNORE INTO supplier (id, name, location) VALUES
                (1, 'North',   'Ha Noi'),
                (2, 'Central', 'Da Nang'),
                (3, 'South',   'Ho Chi Minh');

            INSERT OR IGNORE INTO product (id, name, category_name, supplier_id) VALUES
                (1, 'APW',     'Watch', 1),
                (2, 'APW Pro', 'Watch', 1),
                (3, 'AA',      'CPU',   2),
                (4, 'AAM',     'CPU',   2),
                (5, 'VNM',     'Milk',  3),
                (6, 'TH',      'Milk',  3);

            INSERT OR IGNORE INTO warehouse
                (id, facility_id, product_id, quantity, import_date, exp_date) VALUES
                (1, 1, 5, 100, '2026-03-01', '2026-06-01'),
                (2, 1, 6, 200, '2026-03-01', '2026-06-01'),
                (3, 3, 5, 200, '2026-03-01', '2026-06-01'),
                (4, 3, 6, 100, '2026-03-01', '2026-06-01'),
                (5, 2, 5, 500, '2025-09-01', '2026-01-01'),
                (6, 2, 5, 100, '2026-02-01', '2026-05-01');

            INSERT OR IGNORE INTO consumption
                (id, facility_id, product_id, quantity, order_date) VALUES
                (1, 1, 5,  50,  '2026-03-01'),
                (2, 1, 6,  50,  '2026-03-01'),
                (3, 3, 5,  50,  '2026-04-01'),
                (4, 3, 6,  50,  '2026-04-01'),
                (5, 2, 5,  200, '2025-11-01'),
                (6, 2, 5,  300, '2026-04-01'),
                (7, 2, 5,  50,  '2025-12-01');
        """)
        conn.commit()