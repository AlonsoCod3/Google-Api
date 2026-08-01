import os
from crud.get.get_all import get_all
from crud.get.by_id import get_item
from crud.get.get_names import get_all_names
from crud.new.new import newe
from crud.delete.eliminate import delet
# from crud.edit.pathc_user import edito
from functions import customer

from flask import Blueprint
routing = Blueprint("customers", __name__)

# producto = {
#     id: number,
#     name: string,
#     docType: string,
#     docNumber: number,
#     phone: number,
#     createdDate: string
#     updatedAt: string
# }

# -------------------------------------------------
@routing.route("/data/<id>") #GET
def geta(id):
    return customer.geto(id)

@routing.route("/data") #GET_CELL
def geto():
    return customer.getCell()
# -------------------------------------------------

@routing.route("/") #GET
def get():
    return get_all()

@routing.route("/<id>") #GET_ID
def by_id(id):
    return get_item(id)

@routing.route("/name/<name>") #GET_NAMES
def get_names(name):
    return get_all_names(name)

@routing.route("/", methods=["POST"]) #NEW
def new():
    return newe()

# @routing.route("/<id>", methods=["PATCH"]) #EDIT
# def edit(id):
#     return edito(id)

# @routing.route("/<id>", methods=["PUT"]) #UPDATE
# def update(id):
#     return edit_customer(id, ruta)

@routing.route("/<id>", methods=['DELETE']) #DELETE
def delete(id):
    return delet(id)
