from __main__ import app
from flask import Flask, jsonify, request, Response,send_file
from re_excel import *
from bson import json_util
from controller.c_propietarios import *

@app.route("/propietario", methods=["GET"])#P1
def ruta_listar_propietario():
    response = listar_propietario()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/propietario", methods=["POST"])#P2
def ruta_registrar_propietario():
    response = registrar_propietario()
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/propietario", methods=["DELETE"])#P3
def ruta_eliminar_propietario():
    response = eliminar_propietario()
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/propietario/<id>", methods=["GET"])#P4
def ruta_listar_propietario_ID(id):
    response = listar_propietario_ID(id)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/propietario/<id>", methods=["DELETE"])#P5
def ruta_eliminar_propietario_ID(id):
    response = eliminar_propietario_ID(id)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/propietario/<id>", methods=["PUT"])#P6
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