import requests
import json
import os

webcams = ['logrono', 'haroo', 'calahorra']


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
    # Ahora todo este rollo para que lea el texto de la url porque en la AEMET no saben cómo utilizar JSON
    archivoderespuestalocal = open('temp.txt', 'wb')
    print("Descargando archivo de texto temporal desde " + urlrespuesta)
    archivoderespuestalocal.write(requests.get(urlrespuesta).content)
    archivoderespuestalocal.close()
    archivoderespuestalocal = open('temp.txt', 'rt')
    stringderespuesta = archivoderespuestalocal.read()
    archivoderespuestalocal.close()
    os.remove('temp.txt')
    stringderespuesta = (stringderespuesta.replace('\n', ''))
    stringderespuesta = (stringderespuesta.translate({ord('\n'): None}))
    anterior, separador, prediccion = stringderespuesta.partition("B.- PREDICCIÓN")
    return prediccion


# Utilizando la función, descarga las imágenes de las webcam
for poblaciones in webcams:
    descargarwebcams(poblaciones)
# Ahora descargaremos en un archivo de texto las predicciones utilizando la API Open Data de AEMET
print(llamadaapipronostico('https://opendata.aemet.es/opendata/api/prediccion/ccaa/hoy/rio', ''))
print(llamadaapipronostico('https://opendata.aemet.es/opendata/api/prediccion/ccaa/manana/rio', ''))
