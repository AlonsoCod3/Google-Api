from functions import customer
from functions.customer import (DOCUMENT_ID, sheet_valor, sheet_delete)
from flask import jsonify, request
from crud.get.by_id import encontrarCelda
from crud.get.by_id import buscarCelda
import requests
from datetime import datetime

clientes_id = ""

def delet(id):
    try:
        # verificar que id exista
        buscarCelda(id, "A")
        customerDelete = encontrarCelda(sheet_valor["fila"])
        if customerDelete == "#N/A":
            return jsonify({'Error': "Id de Cliente no encontrado"}), 404
        
        # Id de pagina clientes
        global clientes_id
        clientes_id = customer.geto("Clientes")

        # datos de pagina eliminados
        result_rows = customer.sheet.values().get(spreadsheetId=DOCUMENT_ID, range=f"{sheet_delete}!A:A").execute()

        # ultima fila ocupada
        last_row = len(result_rows.get("values",[]))

        # Creacion de timestamp delete
        delete_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Se añade primero el timestamp para que no tome una fila vacia.
        addTimeDelete(delete_date, last_row)

        # mover dato a tabla eliminados
        pro = cortarDato(customerDelete, last_row)
        return pro
        
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
    # Obtener id de tabla eliminados
    delete_id = customer.geto(sheet_delete)

    try:
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
        
        return jsonify({"message": "Recurso eliminado correctamente"}),204
    except:
        return jsonify({"error": "Error en peticion para borrar cliente"}), 409

def addTimeDelete(time, row):
    body = {"values": [[time]]}
    cell = row + 1
    
    customer.sheet.values().append(
        spreadsheetId=DOCUMENT_ID,
        range=f"{sheet_delete}!A{cell}",
        body= body,
        includeValuesInResponse=True,
        valueInputOption="USER_ENTERED"
    ).execute()

    print("Se agrego timeStamp", flush=True)