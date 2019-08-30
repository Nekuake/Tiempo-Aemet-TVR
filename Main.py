
#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import os
from docx import Document
from datetime import date
import platform
import pprint
print('Script de generación automatica de predicción utilizando datos generados por la API de la AEMET, programado por Alejandro Hurtado, para TV Rioja')
webcams = ['logrono', 'haroo', 'calahorra']
codigosmunicipio = {
    'calahorra': '26036',
    'logrono': '26089',
    'alfaro': '26011',
    'arnedo': '26018',
    'cervera': '26047',
    'ezcaray': '26061',
    'haro': '26071',
    'domingo': '26138',
    'torrecilla': '26151',
    'najera': '26102',
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
    nombredocumento = ('guion' + (str(date.today())) + '.docx')
    print('El nombre del docx que se creará como guión es ' + nombredocumento)
    documentodesalida.add_heading('GUIÓN VOZ EN OFF TIEMPO ' + str(date.today()), 0)
    documentodesalida.add_paragraph('Así ha amanecido en Logroño como se aprecia en este time-lapse de Meteo Sojuela.',
                                    style=None)
    documentodesalida.add_paragraph(hoy, style=None)
    documentodesalida.add_paragraph(manana, style=None)
    documentodesalida.add_paragraph(
        'Les dejamos con las imágenes que nos envían nuestros colaboradores del tiempo. \n\n\n')
    documentodesalida.save(nombredocumento)
    print('Está usando un sistema ' + platform.system() + ' si no es Windows es probable que falle el intento de impresión.')
    try:
        #os.startfile(nombredocumento, 'print')
        print('Aquí se imprimiría, pero de momento está desactivado para favorecer el debug.')
    except:
        print("Error de impresión")
    os.remove('Guion_pronosticos.txt')


def importarprediccionesespecificas(municipio, nombremunicipio):
    payload = ''
    headers = {
        'accept': 'application/json',
        'api_key': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhaHVydGFkb0B0dnJpb2phLmNvbSIsImp0aSI6IjBiYzQxMGQyLTc1NjAtNDYyMS05ZjgxLTEwOWE4N2YxZDE2YSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTY1Njk1OTk2LCJ1c2VySWQiOiIwYmM0MTBkMi03NTYwLTQ2MjEtOWY4MS0xMDlhODdmMWQxNmEiLCJyb2xlIjoiIn0.kykNwBojwUwqO8r16SZ1NfdLxV2Bv-PR1PJUpBhxBMM'
    }
    urldeprediccion = ('https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/' + municipio)
    respuesdeapi = requests.request("GET", urldeprediccion, data=payload, headers=headers)
    diccionarioderespuesta = json.loads(respuesdeapi.text)
    urlrespuesta = diccionarioderespuesta.get('datos', None)
    archivojsonderespuesta = open('temp.json', 'wb')
    print("Descargando archivo de texto temporal desde " + urlrespuesta)
    archivojsonderespuesta.write(requests.get(urlrespuesta).content)
    archivojsonderespuesta.close()
    with open('temp.json', 'r', encoding= 'windows-1252') as archivojson:
        datos=archivojson.read()
    #A partir de aquí el código se vuelve raro, pero es fácil de entender. Adjunto documentación, así que tranquilidad. Hago muchas variables y doy muchas vueltas porque he ido aprendiendo cómo iba su API a la vez que programaba. Todo quedará claro en la doc. 
    diccionariodeprediccion = json.loads(datos)
    diossabequeestoyhaciendo= (diccionariodeprediccion[0])
    predicciondiccionario = diossabequeestoyhaciendo['prediccion']
    predicciondiccionario=predicciondiccionario['dia']
    diauno = predicciondiccionario[0]
    diados = predicciondiccionario[1]
    diatres = predicciondiccionario[2]
    diacuatro = predicciondiccionario[3]
    diacinco = predicciondiccionario[4]
    #Importa en variable la probabilidad de precipitación general del primer día
    precipitacionuno = diauno['probPrecipitacion']
    precipitacionuno = precipitacionuno[0]
    cantidadprecipitacionuno = precipitacionuno['value']
    print('Hoy, el porcentaje de probabilidad de precipitacion en ' + nombremunicipio + '  es ' + str(cantidadprecipitacionuno) + '%')
    #Importa en variable la probabilidad de precipitación general del segundo día
    precipitaciondos = diados['probPrecipitacion']
    precipitaciondos = precipitaciondos [0]
    cantidadprecipitaciondos = precipitaciondos['value']
    print('Mañana, el porcentaje de probabilidad de precipitacion en ' + nombremunicipio + ' es ' + str(cantidadprecipitaciondos) + '%')
    #Importa en variable la probabilidad de precipitación general del tercer día
    precipitaciontres = diatres['probPrecipitacion']
    precipitaciontres = precipitaciontres [0]
    cantidadprecipitaciontres = precipitaciontres ['value']
    print ('Pasado-mañana, el porcentaje de probabilidad de precipitacion en ' + nombremunicipio + ' es ' + str(cantidadprecipitaciontres) + '%')
    #Importa en variable la probabilidad de precipitación general del cuarto día
    precipitacioncuatro = diacuatro['probPrecipitacion']
    precipitacioncuatro = precipitacioncuatro [0]
    cantidadprecipitacioncuatro = precipitacioncuatro ['value']
    #Importa en variable la probabilidad de precipitación general del quinto día
    precipitacioncinco = diacinco['probPrecipitacion']
    precipitacioncinco = precipitacioncinco [0]
    cantidadprecipitacioncinco = precipitacioncinco ['value']
    #Una vez importadas las probabilidades de lluvia, ahora iremos a las posibles temperaturas.
    tempuno = diauno['temperatura']
    tempmaxuno = tempuno['maxima']
    tempminuno = tempuno['minima']
    print('La mínima de hoy en ' + nombremunicipio + ' ' + str(tempminuno) + 'º y la máxima es de ' + str(tempmaxuno) + 'º')
    #La temperatura de mañana...
    tempdos = diados['temperatura']
    tempmaxdos = tempdos['maxima']
    tempmindos = tempdos['minima']
    print('La mínima de mañana en ' + nombremunicipio + ' ' + str(tempmindos) + 'º y la máxima es de ' + str(tempmaxdos) + 'º')
    #La temperatura de pasadomañana...
    temptres = diatres['temperatura']
    tempmaxtres = temptres['maxima']
    tempmintres = temptres['minima']
    print('La mínima de pasadomañana en ' + nombremunicipio + ' ' + str(tempmintres) + 'º y la máxima es de ' + str(tempmaxtres) + 'º')
    #And so on... 
    tempcuatro = diacuatro['temperatura']
    tempmaxcuatro = tempcuatro['maxima']
    tempmincuatro = tempcuatro['minima']
    #Por ultimo, la temperatura del dia cinco
    tempcinco = diacinco['temperatura']
    tempmaxcinco = tempcinco['maxima']
    tempmincinco = tempcinco['minima']
    #Ahora el estado del cielo, que este tiene más intringulis. La AEMET devuelve un código y una descre


# Utilizando la función, descarga las imágenes de las webcam
for poblaciones in webcams:
    descargarwebcams(poblaciones)
# Ahora descargaremos en un archivo de texto las predicciones utilizando la API Open Data de AEMET
with open('Guion_pronosticos.txt', 'w') as archivopronosticos:
    archivopronosticos.write('Pronosticos\n')
    archivopronosticos.write('Así ha amanecido en Logroño como se aprecia en este time-lapse de Meteo Sojuela \n')
    pronosticohoy = llamadaapipronostico('https://opendata.aemet.es/opendata/api/prediccion/ccaa/hoy/rio', '')
    pronosticomanana = llamadaapipronostico('https://opendata.aemet.es/opendata/api/prediccion/ccaa/manana/rio', '')
    archivopronosticos.write('\nHoy,' + pronosticohoy)
    archivopronosticos.write('\nMañana,' + pronosticomanana)
    archivopronosticos.write('\nLes dejamos con las imágenes que nos envían nuestros colaboradores del tiempo')
creardocxpronostico(pronosticohoy, pronosticomanana)
importarprediccionesespecificas(codigosmunicipio['calahorra'], 'Calahorra')
importarprediccionesespecificas(codigosmunicipio['logrono'], 'Logroño')
importarprediccionesespecificas(codigosmunicipio['haro'], 'Haro')

terminarscript = input('Pulse Intro para terminar...')
