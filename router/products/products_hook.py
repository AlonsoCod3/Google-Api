import os
from crud.get.get_all import get_all
from crud.get.by_id import get_item
from crud.new.new import newe
from crud.delete.eliminate import delet
from crud.edit.pathc_user import edito
from functions import productos

from flask import Blueprint
routing = Blueprint("products", __name__)

# producto = {
#     id: number,
#     code: string, // 4 digitos
#     name: string,
#     description: string,
#     price: float,
#     variants: [
#         codigo: string; // 2 dígitos
#         nombre: string;
#         precio: number;
#     ]
# }


@routing.route("/data/<id>") #GET
def geta(id):
    return productos.geto(id)

@routing.route("/data") #GET_CELL
def geto():
    return productos.getCell()

@routing.route("/") #GET
def get():
    return get_all()

@routing.route("/<id>") #GET_ID
def by_id(id):
    return get_item(id)

@routing.route("/", methods=["POST"]) #NEW
def new():
    return newe()

@routing.route("/<id>", methods=["PATCH"]) #EDIT
def edit(id):
    return edito(id)

@routing.route("/<id>", methods=["PUT"]) #UPDATE
def update(id):
    return edit_product(id, ruta)

@routing.route("/<id>", methods=['DELETE']) #DELETE
def delete(id):
    return delet(id)
