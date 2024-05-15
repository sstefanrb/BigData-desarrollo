from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from flask_session import Session
import pandas as pd
import pickle

app = Flask(__name__)
app.secret_key = 'bigdata'  
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

with open('modelo.pkl', 'rb') as file:
    modelo = pickle.load(file)
datos_procesados = pd.read_csv('datos_procesados.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ml')
def machine_learning():
    return render_template('ml.html')

@app.route('/eda')
def exploratory_data_analysis():
    if 'logged_in' not in session or not session['logged_in']:
        flash("Debes iniciar sesión para acceder a esta página.")
        return redirect(url_for('login'))
    return render_template('eda.html')

@app.route('/empresascolaboradoras')
def empresascolaboradoras():
    return render_template('empresascolaboradoras.html')

@app.route('/sobrenosotros')
def sobrenosotros():
    return render_template('sobrenosotros.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        try:
            with open("users.txt", "r") as file:
                users = file.readlines()
                for user in users:
                    uname, upass = user.strip().split(',')
                    if uname == username and upass == password:
                        session['logged_in'] = True
                        session['username'] = username
                        return redirect(url_for('exploratory_data_analysis'))
        except Exception as e:
            print(e)
        flash("Usuario o contraseña incorrectos.")
        return redirect(url_for('login'))

    if 'logged_in' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None) 
    session.pop('username', None) 
    flash("Has cerrado sesión correctamente.")
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        if password != confirm_password:
            flash("Las contraseñas no coinciden.")
            return redirect(url_for('register'))
        
        with open("users.txt", "a") as file:
            file.write(f"{username},{password}\n")
        
        return render_template('index.html')
    return render_template('register.html')


@app.route('/get_unique_values/<field>', methods=['GET'])
def get_unique_values(field):
    if field not in datos_procesados.columns:
        return jsonify({"error": "Field not found"}), 404
    
    if field == "model":
        make = request.args.get('make')
        if make:
            unique_values = datos_procesados[datos_procesados['make'] == make]['model'].dropna().unique().tolist()
        else:
            unique_values = datos_procesados['model'].dropna().unique().tolist()
    else:
        unique_values = datos_procesados[field].dropna().unique().tolist()
    
    return jsonify(unique_values)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    X_nuevo = pd.DataFrame(data, index=[0])
    
    y_pred = modelo.predict(X_nuevo)
    
    return jsonify({'prediction': y_pred.tolist()})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
