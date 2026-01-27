from functions import productos
from flask import jsonify, request
from crud.get.by_id import encontrarCelda
from crud.get.by_id import buscarCelda
import requests
import uuid

from functions.productos import (DOCUMENT_ID, sheet_search, sheet_valor)

def newe():
    try:
        data = request.get_json()
        print("Esta es la información que enviaste:", data,flush=True)
        print("type of data: ", type(data))
        if not data:
            return jsonify({"Error": "JSON inválido o ausente"}), 400

        if "name" not in data or "type" not in data or "amount" not in data:
            return jsonify({"Error": "Faltan campos requeridos"}), 400

        print("pase los 3 campos")

        if not isinstance(data.get("name"), str):
            return ("El 'name' debe ser una cadena")
        data["name"] = data.get("name").lower()
        buscarCelda(data.get("name"), "B")
        validateProduct = encontrarCelda(sheet_valor["fila"])

        if validateProduct != "#N/A":
            return jsonify({'Error': "Producto ya creado"}), 500
        
        if not isinstance(data.get("type"), str):
            return ("El 'type' debe ser una cadena")
        data["type"] = data.get("type").lower()
        
        if not data.get("amount").isdigit():
            return ("El 'amount' debe ser un valor numerico")

        pro = agregarCelda(data)
        return pro
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# Crea un nuevo producto en la hoja de calculo
def agregarCelda(valor, rango="A"):
    body = {"values": [[
        str(uuid.uuid4()),
        valor.get("name"),
        valor.get("type"),
        valor.get("amount")
        ]]}
    print(sheet_search,flush=True)

    rang_cell = f"{sheet_search}{rango}:{rango}"
    result_rows = productos.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=rang_cell).execute()
    
    last_row = len(result_rows.get("values",[])) + 1

    rang_last = f"Productos!{rango}{last_row}"
    result = productos.sheet.values().append(spreadsheetId=DOCUMENT_ID, range=rang_last, body= body, includeValuesInResponse=True, valueInputOption="USER_ENTERED").execute()

    values = result
    print(values.get("updates").get("updatedData"))
    return values