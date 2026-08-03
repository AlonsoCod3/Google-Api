import os
from flask import jsonify
# DOCUMENT_ID = os.getenv("DOCUMENT_ID")
DOCUMENT_ID = "10-XhAKVGEbLTzjN-KDNc5jVi83itkvi5Brda4PVxZp8"

sheet= None
sheet_data = "Clientes!"
sheet_search = "LOOKUP_SHEET!"
sheet_delete = "Clientes_Del"
sheet_valor = {
    "columna":"B",
    "fila":"C",
    "completo":"D",
}

# Inicializamos el servicio sheet para utilizar en nuestras funciones
def define_sheet(value):
    global sheet
    sheet = value

# Consulta y devuelve el id de la hoja de cálculo respectiva
def geto(id):
    body = id
    result = sheet.get(spreadsheetId=DOCUMENT_ID).execute()
    names_sheet = {}
    for name in result.get('sheets'):
        names_sheet[(name.get('properties').get('title'))] = (name.get('properties').get('sheetId'))

    if id not in names_sheet:
        return jsonify("No se encontro la hoja de calculo")

    return names_sheet[id]

# fila = encontrarCelda(productos.sheet_valor["fila"])
def getCell():
    result = sheet.values().get(spreadsheetId=DOCUMENT_ID, range=sheet_search_form+sheet_valor["fila"]+"13").execute()
    values = result.get('values', [])
    print("Se encontro en la celda: ", values[0][0])
    return values[0][0]
