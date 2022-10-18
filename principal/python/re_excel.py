import pandas as pd
from openpyxl.workbook import Workbook
import openpyxl
#from openpyxl import Workbook
from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.styles import *
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
import xlwings as xw
import time
from PyPDF2 import PdfFileWriter, PdfFileReader
from openpyxl.drawing.spreadsheet_drawing import AnchorMarker, TwoCellAnchor, OneCellAnchor
from openpyxl.utils.units import pixels_to_EMU, cm_to_EMU
from openpyxl.drawing.xdr import XDRPoint2D, XDRPositiveSize2D
from PIL import Image
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

def bordear_celdasv1(sheet,celda_ini,celda_final):#A1 , E8
    letra_ini_col = celda_ini[0]#string
    letra_ini_col = ord(letra_ini_col)-64#letra a numero

    letra_final_col = celda_final[0]#string
    letra_final_col = ord(letra_final_col)-64#letra a numero

    letra_ini_fil = int(celda_ini[1])#int
    letra_final_fil = int(celda_final[1])#int

    for fila in range(letra_ini_fil,letra_final_fil):
        for columna in range(letra_ini_col,letra_final_col):
            sheet.cell(fila,columna).border = Border(left=Side(border_style='thin', color='000000'),
                                                    right=Side(border_style='thin', color='000000'),
                                                    top=Side(border_style='thin', color='000000'),
                                                    bottom=Side(border_style='thin', color='000000'))

def bordear_celdasv2(sheet,iterable,ultima_fila,centrado=False):#cuando tienes la posicion de las celdas en numeros
    for i in range(iterable,ultima_fila+1):
            for j in range(1,6):
                sheet.cell(i,j).border = Border(left=Side(border_style='thin', color='000000'),
                                                right=Side(border_style='thin', color='000000'),
                                                top=Side(border_style='thin', color='000000'),
                                                bottom=Side(border_style='thin', color='000000'))
                if centrado:
                    letra=get_column_letter(j)
                    celda=f'{letra}{i}'
                    sheet[celda].alignment=Alignment(horizontal='center')

def izquierda(sheet,fila,columna):
    sheet.cell(fila,columna).border = Border(left=Side(border_style='thin', color='000000'),
                                                right=Side(border_style=None, color='000000'),
                                                top=Side(border_style=None, color='000000'),
                                                bottom=Side(border_style=None, color='000000'))
    #print('izquierda')

def derecha(sheet,fila,columna):
    sheet.cell(fila,columna).border = Border(left=Side(border_style=None, color='000000'),
                                                right=Side(border_style='thin', color='000000'),
                                                top=Side(border_style=None, color='000000'),
                                                bottom=Side(border_style=None, color='000000'))
    #print('derecha')

def arriba(sheet,fila,columna):
    sheet.cell(fila,columna).border = Border(left=Side(border_style=None, color='000000'),
                                                right=Side(border_style=None, color='000000'),
                                                top=Side(border_style='thin', color='000000'),
                                                bottom=Side(border_style=None, color='000000'))
    #print('arriba')

def abajo(sheet,fila,columna):
    sheet.cell(fila,columna).border = Border(left=Side(border_style=None, color='000000'),
                                                right=Side(border_style=None, color='000000'),
                                                top=Side(border_style=None, color='000000'),
                                                bottom=Side(border_style='thin', color='000000'))
    #print('abajo')

def bordear_lado(lado,sheet,fila,columna):
    {
        'izquierda': izquierda(sheet,fila,columna),
        'derecha':derecha(sheet,fila,columna),
        'arriba':derecha(sheet,fila,columna),
        'abajo':derecha(sheet,fila,columna)
    }.get(lado)

def getColumnName(n):#vota string
    # inicializa la string de salida como vacía
    result = ''
    while n > 0:

        # encontrar el índice de la siguiente letra y concatenar la letra
        # a la solución
 
        # aquí el índice 0 corresponde a `A`, y 25 corresponde a `Z`
        index = (n - 1) % 26
        result += chr(index + ord('A'))
        n = (n - 1) // 26
    return result[::-1]

def ancho_col(sheet):
    lista_ancho_columnas=[17,18,14,10,17]
    anchos=0
    for columna in range(1,6):
        col_letter = get_column_letter(columna)
        medida=lista_ancho_columnas[anchos]
        sheet.column_dimensions[col_letter].width = medida #NO ESTA EN PIXELES
        anchos=anchos+1

def convertir_a_pdf(ruta_excel,nombre_archivo):#FALLA SI EL PDF YA EXISTE
    excel_app = xw.App(visible=False)
    print('Iniciando ...')
    # Initialize new excel workbook
    #book = load_workbook(ruta_excel+'/'+nombre_archivo+'.xlsx')
    #book = xw.Book(ruta_excel)#RUTA
    excel_book = excel_app.books.open(ruta_excel)
    ruta_pdf='C:/Users/DELL/Desktop/angular/mongodb/principal/excels/pruebas/'
    nombre_pdf = nombre_archivo+'.pdf'
    pdf_path = ruta_pdf+nombre_pdf
    # Save excel workbook to pdf file
    print(f"Saving workbook as '{pdf_path}' ...")
    excel_book.api.ExportAsFixedFormat(0, pdf_path)
    print('conversion exitosa')

    excel_book.close()
    excel_app.quit()

def poner_imagenes(sheet):
    #insertando la imagen
        #logo = openpyxl.drawing.image.Image('C:/Users/DELL/Desktop/angular/mongodb/principal/LOGOVIDEOFINCA_ORIGINAL.png')
        logo_pil = Image.open('C:/Users/DELL/Desktop/angular/mongodb/principal/LOGOVIDEOFINCA_ORIGINAL.png')
        finca_pil = Image.open('C:/Users/DELL/Desktop/angular/mongodb/principal/FINCA.jpg')
        
        #establecer dimensiones
        proporcion = 3
        alto = 40
        ancho = int(proporcion * alto)

        #editar la imagen
        logo_pil = logo_pil.resize((ancho,alto+5))#140 80 solo acepta enteros
        logo_pil.save('C:/Users/DELL/Desktop/angular/mongodb/principal/LOGOVIDEOFINCA_MODIFICADO.png')

        finca_pil = finca_pil.resize((ancho+3,alto))
        finca_pil.save('C:/Users/DELL/Desktop/angular/mongodb/principal/FINCA_MODIFICADO.jpg')
    
        logo = openpyxl.drawing.image.Image('C:/Users/DELL/Desktop/angular/mongodb/principal/LOGOVIDEOFINCA_MODIFICADO.png')
        
        p2e = pixels_to_EMU
        c2e = cm_to_EMU
        h, w = logo.height, logo.width
        size = XDRPositiveSize2D(p2e(w), p2e(h))
        # Calculated number of cells width or height from cm into EMUs
        cellh = lambda x: c2e((x * 49.77)/99)
        cellw = lambda x: c2e((x * (18.65-1.71))/10)

        # Want to place image in row 5 (6 in excel), column 2 (C in excel)
        # Also offset by half a column.
        column = 0
        coloffset = cellw(0.05)
        row = 1
        rowoffset = cellh(0.05)

        marker = AnchorMarker(col=column, colOff=coloffset, row=row, rowOff=rowoffset)
        logo.anchor = OneCellAnchor(_from=marker, ext=size)

        sheet.add_image(logo)
        

        finca = openpyxl.drawing.image.Image('C:/Users/DELL/Desktop/angular/mongodb/principal/FINCA_MODIFICADO.jpg')
        p2e = pixels_to_EMU
        c2e = cm_to_EMU
        h, w = finca.height, finca.width
        size = XDRPositiveSize2D(p2e(w), p2e(h))
        # Calculated number of cells width or height from cm into EMUs
        cellh = lambda x: c2e((x * 49.77)/99)
        cellw = lambda x: c2e((x * (18.65-1.71))/10)

        # Want to place image in row 5 (6 in excel), column 2 (C in excel)
        # Also offset by half a column.
        column = 4
        coloffset = cellw(0.05)
        row = 1
        rowoffset = cellh(0.05)

        marker = AnchorMarker(col=column, colOff=coloffset, row=row, rowOff=rowoffset)
        finca.anchor = OneCellAnchor(_from=marker, ext=size)

        sheet.add_image(finca) 

def ancho_columnas_parametros(sheet):
    lista_ancho_columnas=[17,20,15,20,17]
    anchos=0
    for columna in range(1,6):
        col_letter = get_column_letter(columna)
        medida=lista_ancho_columnas[anchos]
        sheet.column_dimensions[col_letter].width = medida #NO ESTA EN PIXELES
        anchos=anchos+1

def cabecera(sheet,prop,json,i):
    combinar_celdas(sheet,'B1','D1','JUNTA DE PROPIETARIOS')
    sheet['B1'].alignment=Alignment(horizontal="center")

    combinar_celdas(sheet,'B2','D2','EDIFICIO GALLITO DE LAS ROCAS')
    sheet['B2'].alignment=Alignment(horizontal="center")
    
    #DIRECCION
    id = prop[i]['_id']
    direccion=json[0]['Direccion']

    combinar_celdas(sheet,'B3','D3',direccion)
    sheet['B3'].alignment=Alignment(horizontal="center")

    combinar_celdas(sheet,'B4','D4','RECIBO POR CUOTA DE MANTENIMIENTO')
    sheet['B4'].alignment=Alignment(horizontal="center")
    formato_celdas(sheet,'B1','Arial',9,True,True,'000000',True)
    combinar_celdas(sheet,'A1','A4')
    combinar_celdas(sheet,'E1','E4')

    sheet['A5']='Departamento:'
    sheet['A6']='Propietario:'
    sheet['A7']='Periodo:'

    #DEPARTAMENTO y PORC. PARTICIPACION
    #departamento
    departamentos = prop[i]['Departamentos']
    id_departamento = departamentos[0]['ID_Departamentos']
    porcentaje_participacion = departamentos[0]['Porcentaje_Participacion']
    
    sheet['B5']=id_departamento
    sheet['B5'].alignment=Alignment(horizontal='center')

    sheet['B7']='SETIEMBRE 2022'
    sheet['B7'].alignment=Alignment(horizontal='center')
    
    estacionamientos = prop[0]['Estacionamientos']

    #por cada estacionamiento
    for j in range(len(estacionamientos)):
        num_estacionamiento = estacionamientos[j]['Numero_Estacionamiento']
    
    sheet['C5']='Estacionamiento:'
    sheet.merge_cells('B6:E6')

    #Datos del propietario

    nombres_completos = prop[i]['Nombres_y_Apellidos']

    sheet['B6']=nombres_completos
    sheet['B6'].alignment=Alignment(horizontal='center')
    sheet['C7']='Total Porc. Part.'

    sheet.merge_cells('D5:E5')
    sheet['D5']=num_estacionamiento
    sheet['D5'].alignment=Alignment(horizontal='center')

    sheet.merge_cells('D7:E7')
    sheet['D7']=porcentaje_participacion
    sheet['D7'].alignment=Alignment(horizontal='center')

    sheet['D8']='Total'
    formato_celdas(sheet,'D8','Calibri',11,False,True,'000000',True)
    sheet['D8'].alignment=Alignment(horizontal='center')

    sheet['E8']='Importe'
    formato_celdas(sheet,'E8','Calibri',11,False,True,'000000',True)
    sheet['E8'].alignment=Alignment(horizontal='center')

    return porcentaje_participacion,nombres_completos

def parte_central(sheet,total_monto,tipo_moneda,nombres_completos,mensaje_extra,book,iterable,n_excel):
    #La suma total
        total_monto_float="{:.2f}".format(total_monto)
        if (tipo_moneda!='€'):
            celda_suma_expresion=tipo_moneda +' '+str(total_monto_float)
        else:
            celda_suma_expresion=str(total_monto_float)+' '+tipo_moneda
        celda_total=f'A{iterable}'
        celda_total_valor=f'E{iterable}'
        sheet[celda_total] = 'TOTAL'

        formato_celdas(sheet,celda_total,'Calibri',11,True,False,'000000')
        sheet[celda_total_valor]=celda_suma_expresion
        sheet[celda_total_valor].alignment=Alignment(horizontal='center')
        formato_celdas(sheet,celda_total_valor,'Calibri',11,True,False,'000000')

        bordear_celdasv1(sheet,'A1','F8')#por alguna razon lo corre aunq marque error gaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

        iterable= iterable + 1
        #----------------------------------------------------------------

        #ultimos datos de abajo
        #----------------------------------------------------------------
        #Fechas emision
        celda_fecha_emision=f'A{iterable}'
        sheet[celda_fecha_emision]='Fecha de emision' #inicial
        
        celda_fecha_emision=f'A{iterable+1}'
        valor_fecha_emision='01/09/2022'
        sheet[celda_fecha_emision]=valor_fecha_emision
        sheet[celda_fecha_emision].alignment=Alignment(horizontal='center')

        #fecha vencimiento
        celda_fecha_vencimento=f'B{iterable}'
        sheet[celda_fecha_vencimento]='Fecha de vencimiento'

        celda_fecha_vencimento=f'B{iterable+1}'
        valor_fecha_vencimento='07/07/2022'
        sheet[celda_fecha_vencimento]=valor_fecha_vencimento
        sheet[celda_fecha_vencimento].alignment=Alignment(horizontal='center')

        #N° de cuenta
        celda_ncuenta=f'C{iterable}'
        sheet[celda_ncuenta]='N° Cuenta'

        celda_CCI=f'C{iterable+1}'
        sheet[celda_CCI]='CCI'
        sheet[celda_CCI].alignment=Alignment(horizontal='center')

        valor_ini_ncuenta=f'D{iterable}'
        ncuenta='194-123456789'
        sheet[valor_ini_ncuenta]=ncuenta
        
        valor_fin_ncuenta=f'E{iterable}'
        #CCI
        valor_ini_CCI=f'D{iterable+1}'
        cci="0021194132456789" #final
        sheet[valor_ini_CCI]=cci

        valor_fin_CCI=f'E{iterable+1}'
        ultima_fila=sheet.max_row
        bordear_celdasv2(sheet,iterable,ultima_fila-1,True)
        combinar_celdas(sheet,valor_ini_ncuenta,valor_fin_ncuenta)
        combinar_celdas(sheet,valor_ini_CCI,valor_fin_CCI)
        sheet[valor_ini_CCI].alignment=Alignment(horizontal='center')

        for fila in range(8,iterable):
            for columna in range(1,6):
                if (columna==1):
                    sheet.cell(fila,columna).border = Border(left=Side(border_style='thin', color='000000'),
                                                            right=Side(border_style=None, color='000000'),
                                                            top=Side(border_style=None, color='000000'),
                                                            bottom=Side(border_style=None, color='000000'))
                if (fila==8):
                    sheet.cell(fila,columna).border = Border(left=Side(border_style=None, color='000000'),
                                                            right=Side(border_style=None, color='000000'),
                                                            top=Side(border_style='thin', color='000000'),
                                                            bottom=Side(border_style=None, color='000000'))
                if (columna==5):
                    bordear_lado('derecha',sheet,fila,columna)
                    
                if (fila==(iterable)):
                    bordear_lado('abajo',sheet,fila,columna)
        
        #fila del titular ultima_fila+1
        celda_vacia_ini=f'A{ultima_fila+1}'
        celda_vacia_fin=f'B{ultima_fila+1}'
        combinar_celdas(sheet,celda_vacia_ini,celda_vacia_fin)

        #ultimas celdas
        celda_titular_ini = f'C{ultima_fila+1}'
        celda_titular_fin = f'E{ultima_fila+1}'
        titular=nombres_completos
        texto_titular = 'BCP - Titular: '+titular
        combinar_celdas(sheet,celda_titular_ini,celda_titular_fin,texto_titular)
        sheet[celda_titular_ini].alignment=Alignment(horizontal='center')

        #ultimas celdas de texto
        celdaini_mensaje =f'A{ultima_fila+2}'
        celdafin_mensaje =f'E{ultima_fila+3}'
        end = ultima_fila+3
        bordear_celdasv2(sheet,ultima_fila,end)
        
        combinar_celdas(sheet,celdaini_mensaje,celdafin_mensaje,mensaje_extra)
        sheet.cell(ultima_fila+2,1).alignment = Alignment(horizontal='center',vertical='center')
        poner_imagenes(sheet)

        sheet.cell(1,5).alignment = Alignment(horizontal='center',vertical='center')

        sheet.cell(8,1).border = Border(left=Side(border_style='thin', color='000000'),
                                        right=Side(border_style=None, color='000000'),
                                        top=Side(border_style=None, color='000000'),
                                        bottom=Side(border_style=None, color='000000'))

        ruta_excel='C:/Users/DELL/Desktop/angular/mongodb/principal/excels/pruebas'

        nombre_excel = f'propietarioV4_{id}_{n_excel}'

        extension_excel = '.xlsx'
        #nombre del excel
        excel_guardar = ruta_excel+'/'+nombre_excel+extension_excel

        #guardando el libro
        book.save(excel_guardar)
        convertir_a_pdf(excel_guardar,nombre_excel)

        #aumentando el numero del excel a guardar
        n_excel=n_excel+1
        
        #si se ve esto en pantalla, se genero el excel con exito
        print('Excel creado del propietario '+nombres_completos)