from functions import productos
from flask import jsonify, request
import requests
from sheets import columnas_data
from crud.get.by_id import (buscarCelda, encontrarCelda)

from functions.productos import (DOCUMENT_ID, sheet_search, sheet_valor)

def edito(id):
    try:
        data = request.get_json()
        print("Datos recibidos: ",data)
        if not data or ("name" not in data) and ("type" not in data) and ("amount" not in data):
            return jsonify({"error": "Missing fields for edit"}), 400
        
        buscarCelda(id, columnas_data['id'])
        fila = encontrarCelda(sheet_valor["fila"])
        if fila == "#N/A":
            return jsonify({'Error': "Id de productos no encontrado"}), 500
        
        pro = edit_user(data, fila)
        return pro
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


def edit_user(data_values, fila):
    
    valo = []
    if "name" in data_values:
        valo.append({ "range": f'{sheet_search}{columnas_data["nombre"]}{fila}',"values": [[data_values["name"]]] })
    if "amount" in data_values:
        valo.append({ "range": f'{sheet_search}{columnas_data["amount"]}{fila}',"values": [[data_values["amount"]]] })
    if "type" in data_values:
        valo.append({ "range": f'{sheet_search}{columnas_data["type"]}{fila}',"values": [[data_values["type"]]] })
    

    result = (
        productos.sheet.values()
        .batchUpdate(
            spreadsheetId= DOCUMENT_ID,
            body={"valueInputOption":"USER_ENTERED", "data": valo, "includeValuesInResponse":True},
        )
        .execute()
    )
            
    return jsonify("User partially updated via PATCH")