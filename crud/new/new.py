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

        # if "name" not in data or "type" not in data or "amount" not in data:
        #     return jsonify({"Error": "Faltan campos requeridos: name or type or amount"}), 400

        print("pase los 3 campos")

        errores = validar_producto(data)
        if errores:
            return jsonify({"Error": errores}), 400

        data["name"] = data.get("name").lower()
        buscarCelda(data.get("name"), "B")
        validateProduct = encontrarCelda(sheet_valor["fila"])

        if validateProduct != "#N/A":
            return jsonify({'Error': "Producto ya creado"}), 500

        pro = agregarCelda(data)
        return pro
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# Crea un nuevo producto en la hoja de calculo
def agregarCelda(valor, rango="A"):
    rang_cell = f"{sheet_search}{rango}:{rango}"
    result_rows = productos.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=rang_cell).execute()
    
    last_row = len(result_rows.get("values",[])) + 1

    body = {"values": [[
        str(uuid.uuid4()),
        str(len(result_rows.get("values",[])) - 1).zfill(3),
        valor["name"].lower(),
        valor["description"].lower(),
        valor["price"],
        len(valor["variants"]) if valor.get("variants") else 0
        ]]}

    rang_last = f"Productos!{rango}{last_row}"
    result = productos.sheet.values().append(spreadsheetId=DOCUMENT_ID, range=rang_last, body= body, includeValuesInResponse=True, valueInputOption="USER_ENTERED").execute()

    values = result
    print(values.get("updates").get("updatedData"))
    return values

def validar_producto(item):
    errores = []

    if not isinstance(item.get("name"), str):
        return ("El 'name' debe ser una cadena")

    if not isinstance(item.get("description"), str):
        return ("El 'description' debe ser una cadena")

    if not isinstance(item.get("price"), (int, float)):
        return ("El 'price' debe ser un número")

    # Validar variants
    if item.get("variants"):
        variants = item.get("variants")

        if not isinstance(variants, list):
            return ("El 'variants' debe ser una lista")
        else:
            for i, variant in enumerate(variants):
                
                if not isinstance(variant.get("name"), str):
                    return (f"Variant[{i}]: 'nombre' debe ser una cadena")
                if not isinstance(variant.get("price"), (int, float)):
                    return (f"Variant[{i}]: 'precio' debe ser un número")
    else:
        print("not hay variantes")
    return False
