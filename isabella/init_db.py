import sqlite3

conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Crear tabla
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Agregar un usuario demo
cursor.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', ('admin', 'admin123'))

conn.commit()
conn.close()
