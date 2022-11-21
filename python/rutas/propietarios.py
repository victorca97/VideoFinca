from __main__ import app
from flask import Flask, jsonify, request, Response
from re_excel import *
from bson import json_util
from controller.c_propietarios import *

#ACTUALZIAR ESTO!!!1

@app.route("/propietarios", methods=["GET"])#P1 listo
def ruta_listar_propietario():
    response = listar_propietario()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/propietario", methods=["POST"])#P2 listo
def ruta_registrar_propietario():
    response = registrar_propietario()
    response = json_util.dumps(response)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

"""@app.route("/propietario", methods=["DELETE"])#P3 
def ruta_eliminar_propietario():
    response = eliminar_propietario()
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}"""

@app.route("/propietario/<id>", methods=["GET"])#P4 falta
def ruta_listar_propietario_ID(id):
    response = listar_propietario_ID(id)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/propietario", methods=["DELETE"])#P5 no se usa 
def ruta_eliminar_propietario_ID():
    response = eliminar_propietario_ID()
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/propietarios/<id>", methods=["PUT"])#P6 falta
def ruta_actualizar_propietario_ID(id):
    response = actualizar_propietario_ID(id)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    return response