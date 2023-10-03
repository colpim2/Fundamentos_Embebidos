# Reproduce un video durante 10 segundos y luego muestra imágenes de muestra en bucle.
# Autor: Mauricio Matamoros
# Licencia: MIT

# Modificado por:
#   - Castillo Montes Pamela
#   - Cruz Cedillo Daniel Alejandro
#   - Hernández Jaimes Rogelio Yael
# Fecha: 2023.09.26

# Importación de librerías
import vlc
from time import sleep

# Ruta del directorio principal
home = '/home/pi'

# Definición del reproductor de medios
player = vlc.MediaPlayer()

# Definición del video a reproducir
video = vlc.Media(f'{home}/videos/video.mp4')

# Definición de imágenes de muestra
pics = []

# Cargar imágenes de muestra en la lista
for i in range(1, 5):
    pics.append(vlc.Media(f'{home}/pictures/pic0{i}.jpg'))

# === Reproducir el video durante 10 segundos ===
# Configurar el reproductor para el video
player.set_media(video)
player.play()
sleep(10)

# === Mostrar las imágenes en bucle, cada una durante 3 segundos ===
while True:
    for i in pics:
        # Configurar el reproductor para la imagen
        player.set_media(i)
        player.play()
        sleep(3)