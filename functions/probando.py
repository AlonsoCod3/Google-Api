import os
columnas = {
    "nombre":"C:C",
    "hastags":"D:D",
    "topic":"E:E",
    "type":"F:F",
}
DOCUMENT_ID = os.getenv("DOCUMENT_ID")
def buscarCelda(sheet,telegram_id_group ):
    valo = {
    # busca el primer valor especifico dentro de una columna
    # "values": [['=MATCH("sandro", Sheet1!A:A,0)']]
    # [['=ROW(INDIRECT(ADDRESS(MATCH("sandro",Sheet1!A:A,0),1)))']]
    "values": [[telegram_id_group]]
    }
    result = (
        sheet.values()
        .update(
            spreadsheetId=DOCUMENT_ID,
            range="LOOKUP_SHEET!A2",
            body=valo,
            valueInputOption="USER_ENTERED",
            includeValuesInResponse=True,
        )
        .execute()
    )
    values = result.get("updatedData").get("values")[0][0]  # valor dentro de la matriz
    print("Valor buscado", values)  # valor dentro de la matriz}
    result = obtenerResultado(sheet)
    if result:
        return obtenerCelda(sheet)
    else:
        print("no hubo coincidencias")
        return False

def obtenerCelda(sheet, rango="C:F"):
    if rango != "C:F":
        rango = columnas[rango]
    values = "LOOKUP_SHEET!" + rango
    result = sheet.values().get(spreadsheetId=DOCUMENT_ID, range=values).execute()
    values = result.get('values')
    print("Valores obtenidos: ", values)
    return values[1:]

def obtenerReferencia(sheet, rango="C:F"):
    if rango != "C:F":
        rango = columnas[rango]
    values = "LOOKUP_SHEET!C2"
    result = sheet.get(spreadsheetId=DOCUMENT_ID, ranges=values, fields="sheets").execute()
    print(result)

def obtenerResultado(sheet):
    values = "LOOKUP_SHEET!B2"
    result = sheet.values().get(spreadsheetId=DOCUMENT_ID, range=values).execute()
    values = result.get('values')
    print("Resultado Obtenido: ", values)
    return int(values[0][0])

def actualizarCelda(sheet, valor):
    #proximo
    return True