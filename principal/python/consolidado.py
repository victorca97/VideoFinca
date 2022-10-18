import sys
from re_mongoDB import*

if __name__ == "__main__":
    while True:
        json = urls()
        principalv2(json)
        sys.exit()
        #crear una funcion asincrona