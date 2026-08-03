from functions import customer
from functions.customer import (DOCUMENT_ID, sheet_valor, sheet_search, sheet_data)
from flask import jsonify
import requests

# FIELDS
# id, A
# docType, B
# name, C
# docNumber, D
# phone, E
# createdAt F

valor = sheet_valor["fila"]

# EXPORT FUNC
def get_item(doc):
    try:
        pro = buscarDato(doc, "D")
        return jsonify(pro), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# FUNCIONALIDAD DEL SERVICIO
# Consulta y devuelve toda la informacion de un cliente especifico por su "DOC"
def buscarDato(value, column_range):
    valo = [
        { "range": sheet_search+"A13","values": [[value]] },
        { "range": sheet_search+"B13","values": [[column_range]] },
    ]
    result = (
        customer.sheet.values()
        .batchUpdate(
            spreadsheetId= DOCUMENT_ID,
            body={"valueInputOption":"USER_ENTERED", "data": valo, "includeValuesInResponse":True},
        )
        .execute()
    )
    new_value = encontrarCelda(valor)
    if (new_value == False or new_value == "#N/A"):
        return jsonify({"error", "No se encontro cliente con el N° de documento"}), 409

    result = customer.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=sheet_data+new_value+":"+new_value).execute()
    values = result.get('values', [])
    print("Se encontro toda la info: ", values)

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
        
    return data_res

def encontrarCelda(value_search):
    try:
        result = customer.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=sheet_search+value_search+"13").execute()
        values = result.get('values', [])
        print("Se encontro en la celda: ", values[0][0], flush=True)
        return values[0][0]
    except:
        return False

def buscarCelda(value, column_range):
    print(f"Buscando el dato {value} en {column_range}", flush= True)
    valo = [
        { "range": sheet_search+"A13","values": [[value]] },
        { "range": sheet_search+"B13","values": [[column_range]] },
    ]
    result = (
        customer.sheet.values()
        .batchUpdate(
            spreadsheetId= DOCUMENT_ID,
            body={"valueInputOption":"USER_ENTERED", "data": valo, "includeValuesInResponse":True},
        )
        .execute()
    )