import sqlite3

# B608: Hardcoded SQL string with possible injection
def get_user(username):
    query = f"SELECT * FROM users WHERE name = '{username}'"
    return query