Este es un pequeño proyecto sobre filtros faciales. Hay tres filtros y un menú para cambiar de uno a otro, o dejar la cámara normal.
El proyecto utiliza la cámara de tu ordenador/portátil para grabar y poner los filtros sobre las caras que detecte.
El programa solo detecta caras que miren de frente a la cámara, aunque se puede inclinar la cabeza (mirando de frente) y los filtros rotarán con ella.

INSTALACIONES NECESARIAS
Este proyecto se basa enteramente en OpenCV, y la librería math que viene con python para calcular la rotación de los filtros al inclinar la cabeza. Así pues, es necesario un entorno que pueda ejecutar código python, así como la librería de OpenCV que se instala con el siguiente comando: pip3 install opencv-python

EJECUCIÓN
Con el proyecto descargado y abierto en tu entorno python, ejecuta "main.py". En consola aparecerá un menú en el que se indican las teclas que hay que pulsar para elegir un filtro u otro, y también para cerrar el programa (tecla q), y se abrirá una nueva ventana con lo que esté grabando la cámara de tu equipo. IMPORTANTE: las teclas hay que pulsarlas teniendo seleccionada la ventana en la que aparece tu cámara (el menú también te lo dirá). No intentes pulsar las teclas en consola porque no fucionará xd

Esto era un proyecto de universidad, aunque por cuestiones de tiempo y restricciones del profesor es bastante simple. Se podría mejorar con otras librerías como MediaPipe para mejorar la detección de las caras, e incluso hacer una web con él en vez de un menú python.
A lo mejor algún día lo intento mejorar, pero de momento aquí se queda la cosa xdd
- Nuria Rivas Chávez, estudiante de Ingeniería del Software :3

-------------------------------------------------------------------------------
FUNCIONES DE OPENCV UTILIZADAS
Gestión de la cámara
-cv2.VideoCapture(nº): abrir una cámara conectada al equipo
-camara.get(cv2.CAP_PROP_FRAME_WIDTH), camara.get(cv2.CAP_PROP_FRAME_HEIGHT): obtener el tamaño de la ventana de la cámara abierta
-cv2.waitKey(10): recoger input del usuario en la ventana de la cámara abierta
-cv2.imshow('nombre', imagen): mostrar cada frame grabado por la cámara abierta
-cv2.destroyAllWindows(): cerrar la ventana de la cámara

Gestión de los filtros
-cv2.imread('imagen'): leer una imagen (que se usará como filtro)
-cv2.imread('imagen', cv2.IMREAD_UNCHANGED): leer una imagen (filtro) PNG junto con su canal alfa de transparencia

-cv2.CascadeClassifier('haarcascade'): obtener los clasificadores que se usan para detectar caras y ojos mediante detectMultiScale

-cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY): cambiar un frame a color para pasarlo a blanco y negro
-cv2.GaussianBlur(imagen, ksize, sigmaX): difuminar un frame mediante desenfoque gaussiano
-cv2.addWeighted(imagen, peso_imagen, imagen_difuminada, peso_imagen_difuminada, beta): tras difuminar un frame, usar esa copia para aumentar la nitidez del frame original
-cv2.resize(imagen, (nuevo_ancho, nuevo_alto)): hacer una imagen más grande o pequeña (escalar una imagen)

*cv2.rectangle(imagen, (x_up_left, y_up_left), (x_down_right, y_down_right), color, grosor_líneas): pintar un rectángulo en una imagen
*cv2.putText(imagen, 'texto', (x, y), fuente, tamaño_fuente, color, grosor_texto): escribir texto en una imagen
**Estas dos funciones se usan principalmente para comprobaciones; en una versión final no aparecerían

-cv2.getRotationMatrix2D((x_eje_rotación, y_eje_rotación), ángulo, escala): generar matriz de rotación para poder rotar una imagen un cierto ángulo. En mi caso, el eje de rotación de la imagen es su centro
-cv2.warpAffine(imagen, matriz_rotación, (ancho_imagen, alto_imagen), flags=cv2.INTER_LINEAR): usar la matriz de rotación creada para una imagen para rotar esa imagen

-cv2.split(imagen): permite almacenar en variables independientes los distintos canales de una imagen
-cv2.merge(canales): permite volver a juntar varios canales de una imagen (de entre los que obtenemos con split)
-cv2.bitwise_and(imagen, imagen, máscara): permite aplicar una máscara a una imagen
*cv2.bitwise_not(máscara): lo utilizo para aplicar una máscara inversa, en algunos de los bitwise_and
-cv2.add(imagen, imagen): combinar dos imágenes en una