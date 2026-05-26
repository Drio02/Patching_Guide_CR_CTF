## Concatenacion de Strings

def login_vuln(user, passw):
    # conn = sqlite3.connect("app.db")
    query = "SELECT * FROM users WHERE username = '" + user + "' AND password = '" + passw + "'"
    return conn.execute(query).fetchone()

## f-strings y .format

cursor.execute(f'SELECT * FROM users WHERE id = {id}')

cursor.execute('SELECT * FROM users WHERE id = "{}"'.format(id))

cursor.execute('SELECT * FROM users WHERE id = "%s"' % id)