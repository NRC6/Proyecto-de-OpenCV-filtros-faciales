import cv2
from filtros.pumpkinFace import filtroCalabaza
from filtros.monocle import filtroMonoculo
from filtros.horns import filtroCuernos

exit = False
filtroActual = 0
camara = cv2.VideoCapture(0)

if not camara.isOpened():
    print("No es posible abrir la cámara")
    exit()

ancho_ventana = int(camara.get(cv2.CAP_PROP_FRAME_WIDTH))
alto_ventana = int(camara.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("=== MENÚ - SpookyFilters ===")
print("~ ¡Elige tu filtro desde la ventana de la cámara! ~")
print("0 - Cámara normal")
print("1 - Calabaza")
print("2 - Monóculo")
print("3 - Cuernos")
print("Q - Salir")

while (exit != True):
    # Recogemos el input del usuario
    tecla = cv2.waitKey(10)

    # El usuario habrá elegido un filtro
    if tecla == ord('0'):
        filtroActual = 0
    elif tecla == ord('1'):
        filtroActual = 1
    elif tecla == ord('2'):
        filtroActual = 2
    elif tecla == ord('3'):
        filtroActual = 3
    elif tecla == ord('q'):
        exit = True
    

    # Leemos un frame de la cámara
    ret, frame = camara.read()

    if not ret:
        print("No es posible obtener la imagen")
        break

    # Aplicamos el filtro al frame
    if (filtroActual == 0):
        nuevoFrame = frame
    elif (filtroActual == 1):
        nuevoFrame = filtroCalabaza(frame, ancho_ventana, alto_ventana)
    elif (filtroActual == 2):
        nuevoFrame = filtroMonoculo(frame, ancho_ventana, alto_ventana)
    elif (filtroActual == 3):
        nuevoFrame = filtroCuernos(frame, ancho_ventana, alto_ventana)

    # Mostramos el frame con filtro
    cv2.imshow('SpookyFilters',nuevoFrame)


camara.release()
cv2.destroyAllWindows()