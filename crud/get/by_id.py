from functions import productos
from functions.productos import (DOCUMENT_ID, sheet_valor, sheet_search_form, sheet_search)
from flask import jsonify
import requests
from sheets import columnas_data

valor = sheet_valor["fila"]

# EXPORT FUNC
def get_item(id):
    try:
        pro = buscarDato(id, columnas_data["nombre"])
        return jsonify(pro)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# FUNCIONALIDAD DEL SERVICIO
# Consulta y devuelve toda la informacion de un producto especifico
def buscarDato(value, column_range):
    valo = [
        { "range": sheet_search_form+"A12","values": [[value]] },
        { "range": sheet_search_form+"B12","values": [[column_range]] },
    ]
    result = (
        productos.sheet.values()
        .batchUpdate(
            spreadsheetId= DOCUMENT_ID,
            body={"valueInputOption":"USER_ENTERED", "data": valo, "includeValuesInResponse":True},
        )
        .execute()
    )
    new_value = encontrarCelda(valor)

    result = productos.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=sheet_search+new_value+":"+new_value).execute()
    values = result.get('values', [])
    print("Se encontro toda la info: ", values)
    return values

def encontrarCelda(value_search):
    result = productos.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=sheet_search_form+value_search+"12").execute()
    values = result.get('values', [])
    print("Se encontro en la celda: ", values[0][0])
    return values[0][0]

def buscarCelda(value, column_range):
    valo = [
        { "range": sheet_search_form+"A12","values": [[value]] },
        { "range": sheet_search_form+"B12","values": [[column_range]] },
    ]
    result = (
        productos.sheet.values()
        .batchUpdate(
            spreadsheetId= DOCUMENT_ID,
            body={"valueInputOption":"USER_ENTERED", "data": valo, "includeValuesInResponse":True},
        )
        .execute()
    )