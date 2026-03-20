
from functions import productos
from functions.productos import (sheet_search, DOCUMENT_ID)
from flask import jsonify
import requests

# EXPORT FUNC
def get_all():
    try:
        pro = obtenerDataResult()
        return pro
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# FUNCIONALIDAD DEL SERVICIO
# Consulta y devuelve todos los nombres de los productos
def obtenerDataResult(rango="A2:F"):
    values = sheet_search + rango
    result = productos.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=values).execute()
    if not result.get('values'):
        return jsonify({'error': "No products found"}), 400
    print("RESPUESTA: ",result)
    data_res = []
    for product in result.get('values'):
        item = {}
        item["id"] = product[0]
        item["code"] = product[1]
        item["name"] = product[2]
        item["description"] = product[3]
        item["price"] = product[4]
        item["variants"] = product[5]
        data_res.append(item)

    return jsonify(data_res)