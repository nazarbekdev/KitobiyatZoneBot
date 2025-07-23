CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    full_name TEXT,
    username TEXT,
    invite_count INTEGER DEFAULT 0,
    invited_by INTEGER
);
"""

REGISTER_USER = """
INSERT OR IGNORE INTO users (telegram_id, full_name, username, invited_by)
VALUES (?, ?, ?, ?);
"""

INCREMENT_INVITE_COUNT = """
UPDATE users
SET invite_count = invite_count + 1
WHERE telegram_id = ?;
"""

GET_USER_BY_TELEGRAM_ID = """
SELECT * FROM users WHERE telegram_id = ?;
"""

GET_INVITE_COUNT_BY_USER = """
SELECT COUNT(*) FROM users WHERE invited_by = ?;
"""

GET_TOP_15_USERS = """
SELECT full_name, username, invite_count
FROM users
WHERE invite_count > 0
ORDER BY invite_count DESC
LIMIT 15;
"""

GET_USER_STATS = """
SELECT full_name, username, invite_count, invited_by
FROM users
WHERE telegram_id = ?;
"""

GET_ALL_USERS = """
SELECT * FROM users;
"""

GET_REFERRER_INFO = """
SELECT full_name, username
FROM users
WHERE telegram_id = ?;
"""
