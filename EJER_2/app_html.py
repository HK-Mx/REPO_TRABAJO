from flask import Flask, jsonify, request
from sqlalchemy import create_engine
import joblib
import numpy as np
import pandas as pd
import datetime

host = "35.241.178.229"
port = 5432
user = "postgres"
password = "postgres"
protocolo = "postgresql"
bbdd = "postgress"

churro = f"{protocolo}://{user}:{password}@{host}:{port}/{bbdd}"
engine = create_engine(churro)

model = joblib.load("model.pkl")

app = Flask(__name__)
app.config["DEBUG"] = True

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Predicción de Flor Iris</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        form {{ background-color: #f4f4f4; padding: 20px; border-radius: 8px; max-width: 500px; margin: auto; }}
        label {{ display: block; margin-bottom: 8px; font-weight: bold; }}
        input[type="number"] {{ width: calc(100% - 22px); padding: 10px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 4px; }}
        input[type="submit"] {{ background-color: #4CAF50; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }}
        input[type="submit"]:hover {{ background-color: #45a049; }}
        .prediction-result {{ margin-top: 20px; padding: 15px; background-color: #e9ffe9; border: 1px solid #4CAF50; border-radius: 8px; }}
    </style>
</head>
<body>
    <h1>Predicción de Flor Iris</h1>
    <form action="/predict" method="post">
        <label for="sepal_length">Longitud del Sépalo (cm):</label>
        <input type="number" step="0.01" id="sepal_length" name="sepal_length" required><br>

        <label for="sepal_width">Ancho del Sépalo (cm):</label>
        <input type="number" step="0.01" id="sepal_width" name="sepal_width" required><br>

        <label for="petal_length">Longitud del Pétalo (cm):</label>
        <input type="number" step="0.01" id="petal_length" name="petal_length" required><br>

        <label for="petal_width">Ancho del Pétalo (cm):</label>
        <input type="number" step="0.01" id="petal_width" name="petal_width" required><br>

        <input type="submit" value="Predecir">
    </form>

    {prediction_result}
</body>
</html>
"""

@app.route('/')
def home():
    return "<h1>Bienvenido!</h1><p>Añade los datos de tu flor para predecir su tipo. Dirígete a /predict</p>"


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction_result_html = ""

    if request.method == 'POST':
        sepal_length = float(request.form["sepal_length"])
        sepal_width = float(request.form["sepal_width"])
        petal_length = float(request.form["petal_length"])
        petal_width = float(request.form["petal_width"])

        features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

        prediction_id = model.predict(features)[0]
        iris_species_names = ['setosa', 'versicolor', 'virginica']
        predicted_species = iris_species_names[prediction_id]
        fecha_predict = str(datetime.datetime.now())
        input_str = str(features[0].tolist())
        
        data_to_store = {
            "fecha_prediccion": [fecha_predict],
            "input_features": [input_str],
            "prediccion": [predicted_species]
        }
        df = pd.DataFrame(data_to_store)
        df.to_sql("postgress", con=engine, if_exists="append", index=False)

        prediction_result_html = f"""
        <div class="prediction-result">
            <h2>Resultado de la Predicción:</h2>
            <p><strong>Especie predicha:</strong> {predicted_species}</p>
            <p><strong>Longitud Sépalo:</strong> {sepal_length} cm</p>
            <p><strong>Ancho Sépalo:</strong> {sepal_width} cm</p>
            <p><strong>Longitud Pétalo:</strong> {petal_length} cm</p>
            <p><strong>Ancho Pétalo:</strong> {petal_width} cm</p>
            <p><strong>Fecha de Predicción:</strong> {fecha_predict}</p>
        </div>
        """

    return HTML.format(prediction_result=prediction_result_html)


@app.route('/historial')
def hist():
    query = """ SELECT * FROM postgress"""
    response = pd.read_sql(query, con=engine)
    return jsonify(response.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)