''' 
Reproduzca el video durante 10s e inmediatamente despues
reproduce en bucle infinito cada imagen de muestra por 3s
se detiene al insertar una USB y se reproducen las imágenes
de este medio

@Author:
	-Castillo Montes Pamela
	-Cruz Cedillo Daniel Alejandro
	-Hernández Jaimes Rogelio Yael

@Date: 2023.09.26
'''

# Librerias
import vlc
from time import sleep
import os
import pyudev
import subprocess as sp

# Ruta de medios
home = '/home/pi'

# Creación de objetos video e imágenes
def create_media():
	# Definición de video
  video = vlc.Media(f'{home}/videos/video.mp4')

  # Definición de imágenes
  pics = []
    # i = Cantidad de imágenes
  for i in range(1,5):
    pics.append(vlc.Media(f'{home}/pictures/pic0{i}.jpg'))

  return video, pics

# Cosas de USB
def auto_mount(path):
	args = ["udisksctl", "mount", "-b", path]
	sp.run(args)

def get_mount_point(path):
	args = ["findmnt", "-unl", "-S", path]
	cp = sp.run(args, capture_output=True, text=True)
	out = cp.stdout.split(" ")[0]
	return out

# === Carga las imágenes dentro de la USB ===
def load_img_USB(path):
  photos = []
  for file in os.listdir(path):
    if file.endswith(".jpg") \
    or file.endswith(".png"):
      photos.append(file)
  return photos


# === Reproduce el video durante 10 segundos ===
def play_video(player, video):
  player.set_media(video)
  player.play()
  sleep(10)


# === Muestras las imágenes, cada una 3 segundos ===
def loop_pics(player, pics):
  # Loop infinito
  i = 0
  while(True):
    player.set_media(pics[i])
    player.play()
    sleep(3)
    i = (i + 1) % len(pics)



def main():
  # Definición de player
  player = vlc.MediaPlayer()

  # Creación de objetos video e imágenes
  video, pics = create_media()
  context = pyudev.Context()
  monitor = pyudev.Monitor.from_netlink(context)
  monitor.filter_by(subsystem="block", device_type="partition")
  
  # Espera actividad de detección
  while True:
    action, device = monitor.receive_device()

    # No se ha detectado USB
    if action != "add":
      # Reproducción y loop de imágenes
      play_video(player, video)
      loop_pics(player, pics)

    # Se detecto USB
    auto_mount("/dev/" + device.sys_name)
    mp = get_mount_point("/dev/" + device.sys_name)

    # Carga y muestran imágenes
    photos = load_img_USB(mp)
    loop_pics(player,photos)
    break


if __name__ == '__main__':
	main()











