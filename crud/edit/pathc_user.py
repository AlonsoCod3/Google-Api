from functions import customer
from flask import jsonify, request
from crud.get.by_id import (buscarCelda, encontrarCelda)
import requests
from datetime import datetime

from functions.customer import (DOCUMENT_ID, sheet_data, sheet_valor)
# FIELDS
# id, A
# docType, B
# name, C
# docNumber, D
# phone, E
# createdAt F

posible_edit = [ {"name":"name", "cell":"C"},{"name": "phone", "cell": "E"} ]

def edito(id):
    try:
        data = request.get_json()
        print(data, flush=True)
        print("Esta es la información que enviaste:", flush=True)
        if not data:
            return jsonify({"error": "Missing fields for edit"}), 400
        
        buscarCelda(id, "A")
        usuario_encontrado = encontrarCelda(sheet_valor["fila"])
        if usuario_encontrado == "#N/A":
            print("Error de usuario no encontrado:", flush=True)
            return jsonify({'error': "Id de productos no encontrado"}), 404
        
        pro = edit_user(data, usuario_encontrado)
        return pro
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


def edit_user(data_values, fila):
    valo = []

    for field in posible_edit:
        print(field, flush=True)
        if field.get("name") in data_values:
            valo.append({ "range": f'{sheet_data}{field.get("cell")}{fila}',"values": [[data_values[field.get("name")].lower()]] })
    
    updateValue = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    valo.append({ "range": f'{sheet_data}G{fila}',"values": [[updateValue]] })
    print("valores posibles añadidos para actualizar", flush=True)
    print(valo, flush=True)

    try:
        result = (
            customer.sheet.values()
            .batchUpdate(
                spreadsheetId= DOCUMENT_ID,
                body={"valueInputOption":"USER_ENTERED", "data": valo, "includeValuesInResponse":True},
            )
            .execute()
        )
        return jsonify({'message': "Recurso actualizado con éxito"}), 204
    except:
        return jsonify({'error': "Error en peticion para actualizar el recurso"}), 409