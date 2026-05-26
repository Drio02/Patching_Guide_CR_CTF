## Concatenacion de Strings

def login_safe(user, passw):
    # conn = sqlite3.connect("app.db")
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    return conn.execute(query, (user, passw)).fetchone()

## f-strings y .format

cursor.execute('SELECT * FROM users WHERE id = ?', (id,))