from functions import customer
from functions.customer import (DOCUMENT_ID, sheet_valor, sheet_search_form, sheet_search)
from flask import jsonify
import requests
from sheets import columnas_data

valor = sheet_valor["fila"]

# EXPORT FUNC
def get_item(id):
    try:
        pro = buscarDato(id, columnas_data["doc"])
        return jsonify(pro)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# FUNCIONALIDAD DEL SERVICIO
# Consulta y devuelve toda la informacion de un cliente especifico por su "DOC"
def buscarDato(value, column_range):
    valo = [
        { "range": sheet_search_form+"A13","values": [[value]] },
        { "range": sheet_search_form+"B13","values": [[column_range]] },
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

    result = customer.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=sheet_search+new_value+":"+new_value).execute()
    values = result.get('values', [])
    print("Se encontro toda la info: ", values)
    return values

def encontrarCelda(value_search):
    result = customer.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=sheet_search_form+value_search+"13").execute()
    values = result.get('values', [])
    print("Se encontro en la celda: ", values[0][0], flush=True)
    limpiar()
    return values[0][0]

def buscarCelda(value, column_range):
    print(f"Buscando el dato {value} en {column_range}", flush= True)
    valo = [
        { "range": sheet_search_form+"A13","values": [[value]] },
        { "range": sheet_search_form+"B13","values": [[column_range]] },
    ]
    result = (
        customer.sheet.values()
        .batchUpdate(
            spreadsheetId= DOCUMENT_ID,
            body={"valueInputOption":"USER_ENTERED", "data": valo, "includeValuesInResponse":True},
        )
        .execute()
    )

def limpiar():
    print("Se limpio el campo de busqueda", flush= True)
    valo = [
        { "range": sheet_search_form+"A13","values": [[]] },
        { "range": sheet_search_form+"B13","values": [[]] },
    ]
    result = (
        customer.sheet.values()
        .batchUpdate(
            spreadsheetId= DOCUMENT_ID,
            body={"valueInputOption":"USER_ENTERED", "data": valo, "includeValuesInResponse":True},
        )
        .execute()
    )