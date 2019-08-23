#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import os
from docx import Document
from datetime import date
import platform

webcams = ['logrono', 'haroo', 'calahorra']
codigosmunicipio= {
    'calahorra' : 26036,
    'logrono' : 26089,
    'alfaro' : 26011,
    'arnedo' : 26018,
    'cervera' : 26047,
    'ezcaray' : 26061,
    'haro' : 26071,
    'domingo' : 26138,
    'torrecilla' : 26151,
    'najera' : 26102,
    }

def descargarwebcams(nombrepoblacion):
    archivopoblacion = open(nombrepoblacion + '.jpg', 'wb')
    urldewebcam = ('https://actualidad.larioja.org/images/webcam/' + nombrepoblacion + '.jpg')
    print('Descargando imagen de webcam desde ' + urldewebcam)
    archivopoblacion.write(requests.get(urldewebcam).content)
    archivopoblacion.close()


def llamadaapipronostico(urldellamada, claveapi):
    payload = ""
    headers = {
        'accept': "application/json",
        'api_key': "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhaHVydGFkb0B0dnJpb2phLmNvbSIsImp0aSI6IjBiYzQxMGQyLTc1NjAtNDYyMS05ZjgxLTEwOWE4N2YxZDE2YSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTY1Njk1OTk2LCJ1c2VySWQiOiIwYmM0MTBkMi03NTYwLTQ2MjEtOWY4MS0xMDlhODdmMWQxNmEiLCJyb2xlIjoiIn0.kykNwBojwUwqO8r16SZ1NfdLxV2Bv-PR1PJUpBhxBMM"
    }
    respuesdeapi = requests.request("GET", urldellamada, data=payload, headers=headers)
    diccionarioderespuesta = json.loads(respuesdeapi.text)
    urlrespuesta = diccionarioderespuesta.get('datos', None)
    # Ahora este rollo porque los de la AEMET no saben utilizar correctamente JSON
    archivoderespuestalocal = open('temp.txt', 'wb')
    print("Descargando archivo de texto temporal desde " + urlrespuesta)
    archivoderespuestalocal.write(requests.get(urlrespuesta).content)
    archivoderespuestalocal.close()
    archivoderespuestalocal = open('temp.txt', 'rt', encoding='windows-1252')
    stringderespuesta = archivoderespuestalocal.read()
    archivoderespuestalocal.close()
    os.remove('temp.txt')
    stringderespuesta = (stringderespuesta.replace('\n', ' '))
    stringderespuesta = (stringderespuesta.translate({ord('\n'): None}))
    anterior, separador, prediccion = stringderespuesta.partition("B.- PREDICCIÓN")
    return prediccion


def creardocxpronostico(hoy, manana):
    documentodesalida = Document()
    nombredocumento = ('guion' + (str(date.today()))+'.docx')
    print(nombredocumento)
    documentodesalida.add_heading('GUIÓN VOZ EN OFF TIEMPO ' + str(date.today()), 0)
    documentodesalida.add_paragraph('Así ha amanecido en Logroño como se aprecia en este time-lapse de Meteo Sojuela.', style=None)
    documentodesalida.add_paragraph(hoy, style=None)
    documentodesalida.add_paragraph(manana, style=None)
    documentodesalida.add_paragraph('Les dejamos con las imágenes que nos envían nuestros colaboradores del tiempo. \n\n\n')
    documentodesalida.add_paragraph('BETA')
    documentodesalida.save(nombredocumento)
    if platform.system == 'Windows':
        os.startfile(nombredocumento, 'print')
    os.remove('Guion_pronosticos.txt')

def importartemperaturas(municipio):
    payload = ''
    headers = {
        'accept': 'application/json',
        'api_key' : 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhaHVydGFkb0B0dnJpb2phLmNvbSIsImp0aSI6IjBiYzQxMGQyLTc1NjAtNDYyMS05ZjgxLTEwOWE4N2YxZDE2YSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTY1Njk1OTk2LCJ1c2VySWQiOiIwYmM0MTBkMi03NTYwLTQ2MjEtOWY4MS0xMDlhODdmMWQxNmEiLCJyb2xlIjoiIn0.kykNwBojwUwqO8r16SZ1NfdLxV2Bv-PR1PJUpBhxBMM'
    }

# Utilizando la función, descarga las imágenes de las webcam
for poblaciones in webcams:
    descargarwebcams(poblaciones)
# Ahora descargaremos en un archivo de texto las predicciones utilizando la API Open Data de AEMET
with open ('Guion_pronosticos.txt', 'w') as archivopronosticos:
    archivopronosticos.write('Pronosticos\n')
    archivopronosticos.write('Así ha amanecido en Logroño como se aprecia en este time-lapse de Meteo Sojuela \n')
    pronosticohoy =llamadaapipronostico('https://opendata.aemet.es/opendata/api/prediccion/ccaa/hoy/rio', '')
    pronosticomanana = llamadaapipronostico('https://opendata.aemet.es/opendata/api/prediccion/ccaa/manana/rio', '')
    archivopronosticos.write('\nHoy,' + pronosticohoy)
    archivopronosticos.write('\nMañana,' + pronosticomanana)
    archivopronosticos.write('\nLes dejamos con las imágenes que nos envían nuestros colaboradores del tiempo')
creardocxpronostico(pronosticohoy, pronosticomanana)


