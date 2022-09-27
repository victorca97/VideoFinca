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
        json = urls()#el json listo
        principalv2(json)
        sys.exit()