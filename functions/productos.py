import os
import uuid
DOCUMENT_ID = os.getenv("DOCUMENT_ID")

sheet= None
sheet_data = "Sheet1!"
sheet_search = "Productos!"
sheet_search_form = "LOOKUP_SHEET!"
sheet_valor = {
    "columna":"B",
    "fila":"C",
    "completo":"D",
}

# Inicializamos el servicio sheet para utilizar en nuestras funciones
def define_sheet(value):
    global sheet
    sheet = value

def obtenerDataResult(rango="B2:B"):
    values = sheet_search + rango
    result = sheet.values().get(spreadsheetId=DOCUMENT_ID, range=values).execute()
    data_res = []
    for product in result.get('values'):
        data_res.append(product[0])
    return data_res

def agregarCelda(valor, rango):
    # body = {"values": [[valor]]}
    body = {"values": [[
        uuid.uuid4,
        valor.name if valor.name else None,
        valor.type if valor.type else None,
        valor.amount if valor.amount else None
        ]]}
    result_rows = sheet.values().get(spreadsheetId=DOCUMENT_ID, range=f"{sheet_search}{rango}:{rango}").execute()
    last_row = len(result_rows.get("values",[])) + 1
    result = sheet.values().update(spreadsheetId=DOCUMENT_ID, range=f'Productos!{rango}{last_row}', body= body, includeValuesInResponse=True, valueInputOption="USER_ENTERED").execute()
    values = result
    print(values.get("updatedData"))
    return values

valor = sheet_valor["fila"]
def buscarDato(value, column_range):
    valo = [
        { "range": sheet_search_form+"A12","values": [[value]] },
        { "range": sheet_search_form+"B12","values": [[column_range]] },
    ]
    result = (
        sheet.values()
        .batchUpdate(
            spreadsheetId=DOCUMENT_ID,
            body={"valueInputOption":"USER_ENTERED", "data": valo, "includeValuesInResponse":True},
        )
        .execute()
    )
    # values = result
    # values = result.get("updatedData").get("values")[0][0]  # valor dentro de la matriz #revisar xq no funciona

    result = sheet.values().get(spreadsheetId=DOCUMENT_ID, range=sheet_search_form+valor+"12").execute()
    values = result.get('values', [])
    print("Se encontro en la celda: ", values[0][0])

    new_value = values[0][0]
    result = sheet.values().get(spreadsheetId=DOCUMENT_ID, range=sheet_search+new_value+":"+new_value).execute()
    values = result.get('values', [])
    print("Se encontro toda la info: ", values)
    return values