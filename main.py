import os
import sheets
from sheets import columnas_busqueda, columnas_data

from functions import probando
# function list [
#   buscarDato(value, columm_range)
#   buscarCelda(telegram_id)
#   obtenerDataResult(rango)
#   obtenerReferencia(rango)
#   obtenerResultado()
#   actualizarCelda(valor, rango)
# ]
sheets.initcializacion()

pro = probando.buscarDato("Pepe", columnas_data["nombre"])
