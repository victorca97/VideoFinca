import pandas as pd
import xlsxwriter
from openpyxl.workbook import Workbook
import openpyxl
from openpyxl import Workbook
import time
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.styles import *

def combinar_celdas(sheet,celda_inicial,celda_final,texto=''):
    sheet.merge_cells(f'{celda_inicial}:{celda_final}')
    if texto!='':
        sheet[celda_inicial]=texto

def formato_celdas(sheet,celda,fuente,tamaño,negrita=False,curva=False,color_texto='000000',subrayado=False):
    if (subrayado):
        tipo_subrayado='single'
    else:
        tipo_subrayado=None
    sheet[celda].font = Font(fuente,
                 size=tamaño,
                 bold=negrita,
                 italic=curva,
                 underline=tipo_subrayado,
                 color=color_texto)