from functions import customer
from flask import jsonify, request
from crud.get.by_id import encontrarCelda
from crud.get.by_id import buscarCelda
import requests
import uuid
from datetime import datetime

from functions.customer import (DOCUMENT_ID, sheet_search, sheet_valor)
# FIELDS
# id,
# typeDoc,
# name,
# docNumber,
# number,
# timestamp

required = ["type", "name", "numDoc"]
verifiqued = ["type", "name", "numDoc", "phoneNumber"]


def newe():
    try:
        data = request.get_json()
        print("Esta es la información que enviaste:", data,flush=True)
        print("type of data: ", type(data), flush=True)
        if not data:
            return jsonify({"Error": "JSON inválido o ausente"}), 400

        # if "name" not in data or "type" not in data or "amount" not in data:
        #     return jsonify({"Error": "Faltan campos requeridos: name or type or amount"}), 400

        print("pase los campos", flush=True)

        errores = validar_producto(data)
        if errores:
            return jsonify({"error": errores}), 400

        buscarCelda(data.get(verifiqued[2]), "D")
        validateDoc = encontrarCelda(sheet_valor["fila"])

        if validateDoc != "#N/A":
            return jsonify({'Error': f"Usuario ya registrado con el mismo {verifiqued[2]}"}), 500

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
        valor[verifiqued[0]].lower(),
        valor[verifiqued[1]].lower(),
        valor[verifiqued[2]],
        valor[verifiqued[3]] if valor.get(verifiqued[3]) else "",
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]]}

    rang_last = f"Clientes!{rango}{last_row}"
    result = customer.sheet.values().append(spreadsheetId=DOCUMENT_ID, range=rang_last, body= body, includeValuesInResponse=True, valueInputOption="USER_ENTERED").execute()

    values = result
    print(values.get("updates").get("updatedData"), flush=True)
    return values

def validar_producto(item):
    errores = []

     # Campos requeridos y no vacíos
    for field in required:
        if field not in item or not str(item.get(field, "")).strip():
            errores.append(f"El campo '{field}' es requerido y no puede estar vacío")

    if not isinstance(item.get(verifiqued[0]), str):
        errores.append(f"El {verifiqued[0]} debe ser una cadena")

    if not isinstance(item.get(verifiqued[1]), str):
        errores.append(f"El {verifiqued[1]} debe ser una cadena")

    if not item.get(verifiqued[2]).isdigit():
        errores.append(f"El {verifiqued[2]} debe ser un número")
    
    if verifiqued[3] in item:
        if not item.get(verifiqued[3]).isdigit():
            errores.append(f"El {verifiqued[3]} debe ser un número")

    
    return errores
