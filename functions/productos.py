import os
# DOCUMENT_ID = os.getenv("DOCUMENT_ID")
DOCUMENT_ID = "10-XhAKVGEbLTzjN-KDNc5jVi83itkvi5Brda4PVxZp8"

sheet= None
sheet_data = "Sheet1!"
sheet_search = "Productos!"

# Inicializamos el servicio sheet para utilizar en nuestras funciones
def define_sheet(value):
    global sheet
    sheet = value

def obtenerDataResult(rango="A2:A"):
    values = sheet_search + rango
    result = sheet.values().get(spreadsheetId=DOCUMENT_ID, range=values).execute()
    data_res = []
    for product in result.get('values'):
        data_res.append(product[0])

    print("Valores obtenidos: ", data_res)
    return values