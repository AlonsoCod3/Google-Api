import os
DOCUMENT_ID = os.getenv("DOCUMENT_ID")
# DOCUMENT_ID = "10-XhAKVGEbLTzjN-KDNc5jVi83itkvi5Brda4PVxZp8"

sheet= None
sheet_data = "Sheet1!"
sheet_search = "LOOKUP_SHEET!"

# Inicializamos el servicio sheet para utilizar en nuestras funciones
def define_sheet(value):
    global sheet
    sheet = value

#formulas para busqueda de datos
# busca el primer valor especifico dentro de una columna
# [['=MATCH("sandro", Sheet1!A:A,0)']]
# [['=ROW(INDIRECT(ADDRESS(MATCH("sandro",Sheet1!A:A,0),1)))']]

# Busca un valor en una columna determinada
def buscarDato(value, column_range):
    valo = [
        { "range": sheet_search+"A12","values": [[value]] },
        { "range": sheet_search+"B12","values": [[column_range]] },
    ]
    result = (
        sheet.values()
        .batchUpdate(
            spreadsheetId=DOCUMENT_ID,
            body={"valueInputOption":"USER_ENTERED", "data": valo, "includeValuesInResponse":True},
        )
        .execute()
    )
    values = result
    # values = result.get("updatedData").get("values")[0][0]  # valor dentro de la matriz
    print("Valor buscado", values)  # valor dentro de la matriz}


# Busca un id en la hoja de datos
def buscarCelda(telegram_id_group):
    valo = {
    "values": [[telegram_id_group]]
    }
    result = (
        sheet.values()
        .update(
            spreadsheetId=DOCUMENT_ID,
            range= sheet_search+"A2",
            body=valo,
            valueInputOption="USER_ENTERED",
            includeValuesInResponse=True,
        )
        .execute()
    )
    values = result.get("updatedData").get("values")[0][0]  # valor dentro de la matriz
    print("Valor buscado", values)  # valor dentro de la matriz}
    result = obtenerResultado()
    if result:
        return obtenerDataResult()
    else:
        print("no hubo coincidencias")
        return False


def obtenerDataResult(rango="C1:G2"):
    values = sheet_search + rango
    result = sheet.values().get(spreadsheetId=DOCUMENT_ID, range=values).execute()
    values = result.get('values')
    print("Valores obtenidos: ", values)
    return values

def obtenerReferencia(rango="A5"):
    values = sheet_search + rango
    result = sheet.values().get(spreadsheetId=DOCUMENT_ID, range=values).execute()
    print(result)
    return result.get('values')[0][0]

def obtenerResultado():
    values = sheet_search + "B2"
    result = sheet.values().get(spreadsheetId=DOCUMENT_ID, range=values).execute()
    values = result.get('values')
    print("Resultado Obtenido: ", values)
    return int(values[0][0])

def actualizarCelda(valor, rango):
    body = {"values": [[valor]]}
    result = sheet.values().update(spreadsheetId=DOCUMENT_ID, range=rango, body= body, valueInputOption="USER_ENTERED").execute()
    values = result
    print(values)
    return True