from __main__ import app
from flask import jsonify, request, Response
from re_excel import *
from bson import json_util
from controller.c_finca import *

@app.route("/finca", methods=["GET"])#F1 FUNCIONA EN POSTMAN
def ruta_listar_finca():
    response =listar_finca()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

"""@app.route("/finca", methods=["DELETE"])#F2 a eliminar
def ruta_eliminar_finca():
    response = eliminar_finca()
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}
"""
@app.route("/finca", methods=["DELETE"])#F3 IMPLEMENTADO
def ruta_eliminar_finca_ID():
    response = eliminar_finca_ID()
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/finca/<id>", methods=["GET"])#F4 NO ES NECESARIO
def ruta_listar_finca_ID(id):
    response = listar_finca_ID(id)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/finca", methods=["POST"])#YA FUNCIONA EN EL POSTMAN
def ruta_crear_finca():
    response = crear_finca()
    response = json_util.dumps(response)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/finca", methods=["PUT"])#P6
def ruta_actualizar_finca_ID():#funciona
    response = actualizar_finca_ID()
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    return response