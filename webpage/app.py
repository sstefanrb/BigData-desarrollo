from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle

app = Flask(__name__)

# Cargar el modelo entrenado y los datos procesados
modelo = pickle.load(open('modelo.pkl', 'rb'))
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

# Endpoint para obtener valores únicos para los dropdowns
@app.route('/get_unique_values/<field>', methods=['GET'])
def get_unique_values(field):
    if field not in datos_procesados.columns:
        return jsonify({"error": "Field not found"}), 404
    
    # Si se solicita 'model', revisar si hay un parámetro 'make' dado
    if field == "model":
        make = request.args.get('make')
        if make:
            # Filtrar los modelos basados en la marca seleccionada
            unique_values = datos_procesados[datos_procesados['make'] == make]['model'].dropna().unique().tolist()
        else:
            unique_values = datos_procesados['model'].dropna().unique().tolist()
    else:
        unique_values = datos_procesados[field].dropna().unique().tolist()
    
    return jsonify(unique_values)

# Endpoint para realizar predicciones
@app.route('/predict', methods=['POST'])
def predict():
    content = request.json
    # Aquí deberías procesar 'content' para que coincida con el formato esperado por tu modelo
    # y luego hacer una predicción con el modelo.
    # Por ejemplo, si tu modelo espera un DataFrame con ciertas columnas:
    input_df = pd.DataFrame([content])
    prediction = modelo.predict(input_df)[0]  # Asumiendo que el modelo retorna un array
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
