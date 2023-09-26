'''
Reproduzca el video durante 10s e inmediatamente despues
reproduce en bucle infinito cada imagen de muestra por 3s

@Author:
	-Castillo Montes Pamela
	-Cruz Cedillo Daniel Alejandro
	-Hernández Jaimes Rogelio Yael

@Date: 2023.09.26
'''

# Librerias
import vlc
from time import sleep

# Ruta de medios
home = '/home/pi'

# Definición de video
player = vlc.MediaPlayer()
video = vlc.Media(f'{home}/videos/video.mp4')

# Definición de imágenes
pics = []
	# i = Cantidad de imágenes
for i in range(1,5):
	pics.append(vlc.Media(f'{home}/pictures/pic0{i}.jpg'))


# === Reproduce el video durante 10 segundos ===
player.set_media(video)
player.play()
sleep(10)

# === Muestras las imágenes, cada una 3 segundos ===
# Loop infinito
while(True):
	i = 0
	for i in range(1,5):
		player.set_media(pics[i])
		player.play()
		sleep(3)
