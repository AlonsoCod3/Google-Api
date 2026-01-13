import os
import sheets
from sheets import columnas_busqueda, columnas_data

from functions import probando, productos

# API
import os
from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# function list [
#   buscarDato(value, columm_range)
#   buscarCelda(telegram_id)
#   obtenerDataResult(rango)
#   obtenerReferencia(rango)
#   obtenerResultado()
#   actualizarCelda(valor, rango)
# ]
sheets.initcializacion()

# pro = probando.buscarDato("Pepe", columnas_data["nombre"])
# pro = productos.obtenerDataResult()
# print(pro)

@app.route('/', methods=['GET'])
def index():
  return "HOLA"

@app.route('/products', methods=['GET']) #GET_ALL
def get_all():
    try:
        pro = productos.obtenerDataResult()
        return jsonify(pro)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/product/<id>', methods=['GET']) #GET_BY_ID
def get_item(id):
    try:
        pro = productos.buscarDato(id, columnas_data["nombre"])
        return jsonify(pro)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/product/', methods=['POST']) #NEW
def newe(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"Error": "JSON inválido o ausente"}), 400
        if not isinstance(item.get("name"), str):
            return ("El 'name' debe ser una cadena")

        result = productos.agregarCelda(data["name"], columnas_data["nombre"])
        print(result)
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/product/<id>', methods=['PUT']) #EDIT
def edit(id):
    try:
        pro = productos.obtenerDataResult()
        print(pro)
        return jsonify(pro)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/product/<id>', methods=['DELETE']) #DELETE
def delete(id):
    try:
        pro = productos.obtenerDataResult()
        print(pro)
        return jsonify(pro)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':  
  app.run(host='0.0.0.0')