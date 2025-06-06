from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import bcrypt


app = Flask(__name__)
app.secret_key = 'clave-secreta'

DB_PATH = 'users.db'

# Crear la base de datos si no existe
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

# Verifica si un usuario existe
def validar_usuario(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result:
        hashed = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    return False


# Crea un nuevo usuario
def registrar_usuario(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        clave = request.form['password']
        if validar_usuario(usuario, clave):
            session['usuario'] = usuario
            return redirect(url_for('convert'))
        else:
            return render_template('login.html', error="Credenciales incorrectas")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form['username']
        clave = request.form['password']
        if registrar_usuario(usuario, clave):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="El usuario ya existe.")
    return render_template('register.html')

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    resultado = None
    if request.method == 'POST':
        tipo = request.form['tipo']
        valor = float(request.form['valor'])

        if tipo == 'm_km':
            resultado = f"{valor} metros = {valor / 1000:.3f} kilómetros"
        elif tipo == 'lb_kg':
            resultado = f"{valor} libras = {valor * 0.453592:.3f} kilogramos"
        elif tipo == 'c_f':
            resultado = f"{valor} °C = {(valor * 9/5) + 32:.2f} °F"
    
    return render_template('convert.html', resultado=resultado)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

