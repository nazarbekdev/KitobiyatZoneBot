from database import db

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER UNIQUE,
    full_name TEXT,
    username TEXT,
    invited_by INTEGER,
    invite_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

if __name__ == "__main__":
    db.execute(CREATE_USERS_TABLE)
    print("✅ Users jadvali yaratildi.")
