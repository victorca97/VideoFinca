from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import sys
import xlsxwriter
from openpyxl.workbook import Workbook
import openpyxl
from openpyxl import Workbook
from openpyxl.chart import ScatterChart, Reference, Series
from recursos_excel import*
from openpyxl.styles import *
from openpyxl.utils import get_column_letter
from recursos_mongoDB import*
import os
from urls import*

if __name__ == "__main__":
    while True:
        #PARA CONECTARSE AL MONGO DB
        MONGO_HOST="localhost"
        MONGO_PUERTO="27017"
        MONGO_TIEMPO_FUERA=1000
        MONGO_URL="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

        client = MongoClient(MONGO_URL)
        
        lista_prueba,collection2=lista_json(client)
        json = urls()
        #GUARDANDO LAS FINCAS Y PROPIETARIOS
        fincas = []
        propietarios=[]
        #tipo_moneda='€'
        cantidad_finca(json,fincas)
        cantidad_propietarios(json,propietarios)

        for f in fincas:
            plantilla2=[
            {
            "$match": {
                "_id": f'{f}'
            }
            },  
            {
            "$lookup": {
                "from": 'Plantilla',
                "localField": '_id',
                "foreignField": 'Finca',
                "as": 'Plantillas'
            }
            },  
            {
            "$lookup": {
                "from": 'Propietario',
                "localField": '_id',
                "foreignField": 'Finca',
                "as": 'Propietarios'
            }
            }
            ]
            resultados2 =collection2.aggregate(plantilla2)
            principalv2(resultados2,propietarios)
        #principalv1(fincas,propietarios,collection2)
        urls()
        sys.exit()