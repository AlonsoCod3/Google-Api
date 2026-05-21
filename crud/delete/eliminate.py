from functions import customer
from functions.customer import (DOCUMENT_ID, sheet_valor)
from flask import jsonify, request
from crud.get.by_id import encontrarCelda
from crud.get.by_id import buscarCelda
import requests
from datetime import datetime
from sheets import columnas_data

sheet_delete = "Clientes_Del"
clientes_id = ""

def delet(id):
    try:
        buscarCelda(id, "A")
        fila = encontrarCelda(sheet_valor["fila"])
        if fila == "#N/A":
            return jsonify({'Error': "Id de Cliente no encontrado"}), 500
        
        # pro = eliminarDato(fila)
        global clientes_id
        clientes_id = customer.geto("Clientes")
        result_rows = customer.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=f"{sheet_delete}!A:A").execute()
        last_row = len(result_rows.get("values",[]))

        delete_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Se añade primero el timestamp para que no tome una fila vacia.
        addTimeDelete(delete_date, last_row)
        pro = cortarDato(fila, last_row)
        
        return jsonify(pro)
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    

def eliminarDato(fila_eliminar:int):
    
    ner = {
        "requests": [
            {
                "deleteDimension": {
                    "range": {
                    "sheetId": clientes_id,
                    "dimension": "ROWS",
                    "startIndex": int(fila_eliminar) - 1,
                    "endIndex": int(fila_eliminar)
                    }
                }
            }
        ]
    }
    result = customer.sheet.batchUpdate(spreadsheetId=DOCUMENT_ID, body= ner).execute()
    print("RESULATADO : ",result)
    return result

def cortarDato(fila_corte:int, last):
    delete_id = customer.geto(sheet_delete)
    print("eliminados ID", delete_id)

    ner = {
        "requests": [
            {
                "cutPaste": {
                    "source": {
                        "sheetId": clientes_id,
                        "startRowIndex": int(fila_corte) - 1,
                        "endRowIndex": int(fila_corte),
                        "startColumnIndex": 0,
                        "endColumnIndex": 6
                    },
                    "destination":{
                        "sheetId": delete_id,
                        "rowIndex": last,
                        "columnIndex": 1
                    },
                    "pasteType": "PASTE_NORMAL"
                }

            }
        ]
    }
    result = customer.sheet.batchUpdate(spreadsheetId=DOCUMENT_ID, body= ner).execute()
    print("RESULATADO : ",result)
    return result

def addTimeDelete(time, row):
    body = {"values": [[time]]}
    
    customer.sheet.values().append(
        spreadsheetId=DOCUMENT_ID,
        range=f"{sheet_delete}!A{row}",
        body= body,
        includeValuesInResponse=True,
        valueInputOption="USER_ENTERED"
    ).execute()

    print("Se agrego timeStamp")