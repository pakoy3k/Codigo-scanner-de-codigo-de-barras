import cv2
from pyzbar.pyzbar import decode
import time

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

if not cam.isOpened():
    print("Error con la camara")
    exit()

print("Sistema listo")

i = 0
while True:
    ret, frame = cam.read()
    if not ret:
        print("Error de lectura")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)
    
    for b in barcodes:
        code = b.data.decode("utf-8").strip()
        print(f"\nID: {code}")

    i += 1
    if i % 20 == 0:
        print(".", end="", flush=True)

    time.sleep(0.05)