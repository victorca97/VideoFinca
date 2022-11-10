from flask import jsonify, request
from re_excel import *
from bson import json_util
from bson.objectid import ObjectId
from libs.database import conexion

#su tabla provisional se llamara 'admins'

def listar_admins():#F1
    finca = conexion('admins').find()
    response = json_util.dumps(finca)
    return response

def eliminar_admins():
    conexion('admins').drop()
    response = jsonify({"status": 201,'message':' se elimino satisfactoriamente'})
    return response

def eliminar_admins_ID(id):
    conexion('admins').delete_one({'_id': id})
    response = jsonify({"status": 201,'message': 'El admin ' + id + ' se elimino satisfactoriamente'})
    return response 