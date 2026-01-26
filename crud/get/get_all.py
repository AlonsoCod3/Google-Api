
from functions import productos
from functions.productos import (sheet_search, DOCUMENT_ID)
from flask import jsonify
import requests

# EXPORT FUNC
def get_all():
    try:
        pro = obtenerDataResult()
        return jsonify(pro)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# FUNCIONALIDAD DEL SERVICIO
# Consulta y devuelve todos los nombres de los productos
def obtenerDataResult(rango="B2:B"):
    values = sheet_search + rango
    result = productos.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=values).execute()
    data_res = []
    for product in result.get('values'):
        data_res.append(product[0])
    return data_res