
from functions import customer
from functions.customer import (DOCUMENT_ID)
from flask import jsonify
import requests

# EXPORT FUNC
def get_all_names(name):
    try:
        pro = obtenerDataResult(name)
        return pro
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# FUNCIONALIDAD DEL SERVICIO
# Consulta y grupos de dni o ruc
type = {
"dni":"H:M",
"ruc":"A:F"
}

def obtenerDataResult(name):
    values = "Clientes_Search!" + type[name]
    result = customer.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=values).execute()
    if not result.get('values'):
        return jsonify({'error': "No customer found"}), 400
    print("RESPUESTA: ",result)
    data_res = []
    for client in result.get('values'):
        item = {}
        item["id"] = client[0]
        item["typeDoc"] = client[1]
        item["name"] = client[2]
        item["docNumber"] = client[3]
        item["number"] = client[4]
        item["createdDate"] = client[5]
        data_res.append(item)

    return jsonify(data_res)