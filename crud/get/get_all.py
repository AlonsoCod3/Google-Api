
from functions import customer
from functions.customer import (sheet_data, DOCUMENT_ID)
from flask import jsonify
import requests

# FIELDS
# id, A
# docType, B
# name, C
# docNumber, D
# phone, E
# createdAt F

# EXPORT FUNC
def get_all():
    try:
        pro = obtenerDataResult()
        return pro
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# FUNCIONALIDAD DEL SERVICIO
# Consulta y devuelve todos los nombres de los productos
def obtenerDataResult(rango="A2:G"):
    values = sheet_data + rango
    result = customer.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=values).execute()
    if not result.get('values'):
        return jsonify({'error': "No customer found"}), 404
    print("RESPUESTA: ",flush=True)
    print(result, flush=True)

    data_res = []
    for client in result.get('values'):
        item = {}
        item["id"] = client[0]
        item["docType"] = client[1]
        item["name"] = client[2]
        item["docNumber"] = client[3]
        item["phone"] = client[4]
        item["createdDate"] = client[5]
        item["updateDate"] = client[6] if len(client) > 6 else ""
        data_res.append(item)

    return jsonify(data_res), 200