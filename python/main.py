from flask import Flask#, jsonify, request, Response,send_file
#from flask_pymongo import PyMongo
#from bson import json_util
#from bson.objectid import ObjectId
from flask_cors import CORS
from re_excel import *
#import json

app = Flask(__name__)
import rutas.finca
import rutas.propietarios
import rutas.recibos

#Para permitir la conexion de los datos
CORS(app)
cors=CORS(app,resource={
    r"/*":{
        "origins":"*"
    }
})

#este es el principal. Lo anterior estan en las carpetas rutas y controller
if __name__ == "__main__":
    app.run(debug=True, port=4000, host="0.0.0.0")