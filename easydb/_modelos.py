Guild = """
    CREATE TABLE IF NOT EXISTS Guild (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        lang TEXT,
        created_at TEXT
    )
"""

User = """
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        lang TEXT,
        prefix TEXT,
        nick TEXT,
        birthday TEXT,
        created_at TEXT
    )
"""
