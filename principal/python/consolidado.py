from re_mongoDB import*
from re_excel import convertir_pdf
from urls import get_informacion
"""if __name__ == "__main__":
    while True:
        json = urls()
        principalv2(json)
        sys.exit()"""
        #crear una funcion asincrona

def generar_doc_finca(tipo): #devuelve una matriz con los sgtes datos
    # estado: si se genero correctamente el excel
    # propietario: nombre del propietario
    # excel: excel codificado del propietario
    # pdf : pdf codificado del propietario

    path = 'C:/Users/DELL/Desktop/angular/mongodb/principal/excels/pruebas'#ruta donde se guardaran los excels y pdfs
    json = get_informacion()#jala el JSON con toda la informacion
    varbuffer,cantidad_propietarios = generar_excel(json) #devuelve la lista con estado,propietario,excel codificado
    if (tipo == 'xlsx'):
        #convertir_pdf(path,tipo)#genera los pdfs
        return varbuffer
    elif (tipo == 'pdf'):
        varbuffer_con_pdfs = convertir_pdf(varbuffer,cantidad_propietarios,path)
        #retornar el status
        return varbuffer_con_pdfs
    else:
        print('tipo de extension incorrecto (poner xlsx o pdf)')

#PRUEBA
tipo = 'pdf'       
matriz = generar_doc_finca(tipo)
#print(matriz)
"""
    {
        nombre: "nombre",
        tipo: "tipo" (xlsx o pdf)
    }
"""