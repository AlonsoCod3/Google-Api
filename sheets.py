from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
DOCUMENT_ID = "10-XhAKVGEbLTzjN-KDNc5jVi83itkvi5Brda4PVxZp8"
KEY = "keys/key.json"

creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPE)
service = build("sheets", "v4", credentials=creds)
sheets = service.spreadsheets()

# AÑADE UNA NUEVA HOJA EN UN DOCUMENTO YA CREADO
# body = {
#     "requests":{
#         "addSheet":{
#             "properties": {
#                 "title": "nuevos"
#             }
#         }
#     }
# }
# sheets = service.spreadsheets().batchUpdate(spreadsheetId = DOCUMENT_ID, body = body).execute()

# --------------------------------
body = {"values": [["Hola Fila 1"]]}
body_new = {"values": [["Nuevo"]]}
# --------------------------------

# AÑADIR VALORES A CELL SHEET --------------------------------
# range es la columa, y tomara el ultimo valor para añadirlo al final automaticamente
# result = sheets.values().append(spreadsheetId=DOCUMENT_ID, range='A1', body= body, valueInputOption="USER_ENTERED").execute()
# values = result.get('updates').get("updatedRange")
# print(values)

# ACTUALIZAR VALORES DE CELL SHEET --------------------------------
# range debe ser la celda especifica que se actualizara
# result = sheets.values().update(spreadsheetId=DOCUMENT_ID, range='A1', body= body2, valueInputOption="USER_ENTERED").execute()
# values = result
# print(values)

# ELIMINA VALORES DE CELL SHEETS --------------------------------
# result = sheets.values().clear(spreadsheetId=DOCUMENT_ID, range='A:A').execute()

# OBTENER/LEER VALORES DE CELL SHEET --------------------------------
# result = sheets.values().get(spreadsheetId=DOCUMENT_ID, range=values).execute()
# values = result.get('values', [])
# print(values)

# OBTENER/LEER VALORES DE CELL SHEET ESPECIFICA --------------------------------
# A-
#    1 - se crea una nueva hoja con el atributo oculto(hidden)
# ner = {
#  "requests": [
#   {
#    "addSheet": {
#     "properties": {
#     #  "hidden": True,
#      "title": "LOOKUP_SHEET"
#     }
#    }
#   }
#  ]
# }
# result = sheets.batchUpdate(spreadsheetId=DOCUMENT_ID, body= ner).execute()
# B-
#    2 - en la nueva hoja se crea la formula para encontrar un MATCH con el valor que querramos
#    y obtenemos el numero de la fila en la columna especificada
# valo = {
    # "values": [['=MATCH("sandro", Sheet1!A:A,0)']]
    # [['=ROW(INDIRECT(ADDRESS(MATCH("sandro",Sheet1!A:A,0),1)))']]
# 
# result = (
#     sheets.values()
#     .update(
#         spreadsheetId=DOCUMENT_ID,
#         range="LOOKUP_SHEET!A1",
#         body=valo,
#         valueInputOption="USER_ENTERED",
#         includeValuesInResponse=True,
#     )
#     .execute()
# )
# values = result.get("updatedData").get("values")[0][0]  # valor dentro de la matriz
# print(result.get("updatedData").get("values")[0][0])  # valor dentro de la matriz
# C-
#    2.1 - Opcionalmente podemos elimar el dato de la celda creda
# result = (
#     sheets.values().clear(spreadsheetId=DOCUMENT_ID, range="LOOKUP_SHEET!A1").execute()
# )
# print(result)
# D-
#    3 - ahora solo queda obtener el valor

# result = sheets.values().get(spreadsheetId=DOCUMENT_ID, range=f"Sheet1!A{values}").execute()
# print(values.get("values"))


# result = sheets.create("Finances")
# values = result.getUrl()
# print(values)

# SE CREA UN NUEVO DOCUMENTO QUE TIENE COMO PROPIETARIO EL BOT --------------------------------
# spreadsheet = {"properties": {"title": "mySheets"}}
# spreadsheet = (
#     service.spreadsheets()
#     .create(body=spreadsheet, fields="spreadsheetId")
#     .execute()
# )
# print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
# values = spreadsheet.get("spreadsheetId")
# print(values)

# LISTANDO INFORMACION RELACIONADA CON UNA HOJA DE CALCULO --------------------------------
# result = sheets.get(spreadsheetId=ID_priv).execute()
# print(result)

# ---------
