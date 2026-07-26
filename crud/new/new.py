from functions import customer
from flask import jsonify, request
from crud.get.by_id import encontrarCelda
from crud.get.by_id import buscarCelda
import requests
import uuid
from datetime import datetime

from functions.customer import (DOCUMENT_ID, sheet_search, sheet_valor)

def newe():
    try:
        data = request.get_json()
        print("Esta es la información que enviaste:", data,flush=True)
        print("type of data: ", type(data))
        if not data:
            return jsonify({"Error": "JSON inválido o ausente"}), 400

        # if "name" not in data or "type" not in data or "amount" not in data:
        #     return jsonify({"Error": "Faltan campos requeridos: name or type or amount"}), 400

        print("pase los 3 campos")

        errores = validar_producto(data)
        if errores:
            return jsonify({"Error": errores}), 400

        data["docNumber"] = data.get("docNumber")
        buscarCelda(data.get("docNumber"), "D")
        validateProduct = encontrarCelda(sheet_valor["fila"])

        if validateProduct != "#N/A":
            return jsonify({'Error': "Usuario ya registrado con el mismo DOC"}), 500

        pro = agregarCelda(data)
        return pro
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# Crea un nuevo producto en la hoja de calculo
def agregarCelda(valor, rango="A"):
    rang_cell = f"{sheet_search}{rango}:{rango}"
    result_rows = customer.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=rang_cell).execute()
    
    last_row = len(result_rows.get("values",[])) + 1

    body = {"values": [[
        str(uuid.uuid4()),
        valor["typeDoc"].lower(),
        valor["name"].lower(),
        valor["docNumber"].lower(),
        valor["number"] if valor.get("number") else "",
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]]}

    rang_last = f"Clientes!{rango}{last_row}"
    result = customer.sheet.values().append(spreadsheetId=DOCUMENT_ID, range=rang_last, body= body, includeValuesInResponse=True, valueInputOption="USER_ENTERED").execute()

    values = result
    print(values.get("updates").get("updatedData"))
    return values

def validar_producto(item):
    errores = []
    required = ["typeDoc, name, docNumber"]

     # Campos requeridos y no vacíos
    for field in required:
        if field not in item or not str(item.get(field, "")).strip():
            errores.append(f"El campo '{field}' es requerido y no puede estar vacío")

    if not isinstance(item.get("typeDoc"), str):
        errores.append("El 'typeDoc' debe ser una cadena")

    if not isinstance(item.get("name"), str):
        errores.append("El 'name' debe ser una cadena")

    if not isinstance(item.get("docNumber"), (int, float)):
        errores.append("El 'docNumber' debe ser un número")

    
    return False
