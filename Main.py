import requests
webcams= ['logrono', 'haroo', 'calahorra']
def descargarwebcams(nombrepoblacion):
    archivopoblacion = open(nombrepoblacion + '.jpg','wb')
    urldewebcam = ('https://actualidad.larioja.org/images/webcam/' + nombrepoblacion +'.jpg')
    print('Descargando imagen de webcam desde ' + urldewebcam)
    archivopoblacion.write(requests.get(urldewebcam).content)
    archivopoblacion.close()

for poblaciones in webcams:
    descargarwebcams(poblaciones)

