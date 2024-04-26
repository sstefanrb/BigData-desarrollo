from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle

app = Flask(__name__)

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
    return render_template('eda.html')

@app.route('/empresascolaboradoras')
def empresascolaboradoras():
    return render_template('empresascolaboradoras.html')

@app.route('/sobrenosotros')
def sobrenosotros():
    return render_template('sobrenosotros.html')

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
