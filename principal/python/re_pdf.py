#import os
import xlwings as xw

print('Iniciando ...')
# Initialize new excel workbook
book = xw.Book('C:/Users/DELL/Desktop/angular/mongodb/principal/excels/pruebas/modificado.xlsx')#RUTA

# Construct path for pdf file
#current_work_dir = os.getcwd()
#pdf_path = os.path.join(current_work_dir, "workbook_printout.pdf")

ruta_pdf='C:/Users/DELL/Desktop/angular/mongodb/principal/excels/pruebas/'
nombre_pdf = 'pruebapdf_excel.pdf'
pdf_path = ruta_pdf+nombre_pdf
# Save excel workbook to pdf file
print(f"Saving workbook as '{pdf_path}' ...")
book.api.ExportAsFixedFormat(0, pdf_path)
print('conversion exitosa')
# Open the created pdf file
#print(f"Opening pdf file with default application ...")
#os.startfile(pdf_path)