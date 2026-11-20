import cv2
import math

def filtroCuernos(frame, ancho_ventana, alto_ventana):
    calabaza_original = cv2.imread('imagenes/horns2.jpg') #como no es png, no hay que leer alfa de transparencia

    alto_calabaza, ancho_calabaza, _ = calabaza_original.shape

    tam_calabaza = 1

    proporciones_calabaza = ancho_calabaza/alto_calabaza

    area_min = 9000

    clasificadorFrontal = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    clasificadorOjos = cv2.CascadeClassifier('haarcascade_eye.xml')

    
    #1:blanco y negro
    frame_byn = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('blancoYnegro',frame_byn)
    #2:aumentar contraste
    #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    #frame_byn = clahe.apply(frame_byn)
    #cv2.imshow('contraste',frame_byn)
    #la img sigue siendo bastante borrosa, asi que...
    #3:sharpen shadows
    blur = cv2.GaussianBlur(frame_byn,(0, 0),sigmaX=1.5)
    frame_byn = cv2.addWeighted(frame_byn,1.5,blur,-0.5,0)
    #cv2.imshow('definicion',frame_byn)



    caras = list(clasificadorFrontal.detectMultiScale(frame_byn, 1.2, 5)) #añadimos parametros para detectar mejor
    for (x_cara, y_cara, ancho_cara, alto_cara) in caras:

        if ancho_cara*alto_cara > area_min:
            ancho_calabaza = int(ancho_cara*tam_calabaza)
            alto_calabaza = int(ancho_calabaza/proporciones_calabaza)
            calabazaNueva = cv2.resize(calabaza_original, (ancho_calabaza, alto_calabaza))

            y_calabaza = int(y_cara-alto_calabaza/1.3) #bajamos los cuernos para que se ajusten a la cabeza
            x_calabaza = int(x_cara+ancho_cara/2-ancho_calabaza/2)





            #EN LA CARA DETECTADA, DETECTAMOS LOS OJOS (en blanco y negro tmb)
            roiCara = frame_byn[y_cara:y_cara+alto_cara, x_cara:x_cara+ancho_cara]
            #cv2.rectangle(frame, (x_cara, y_cara), (x_cara+ancho_cara,y_cara+alto_cara), (255,0,0), 2)
            ojos = clasificadorOjos.detectMultiScale(roiCara) #no list porque solo hay un par de ojos por cara

            #SE COMPRUEBA SI LA CARA ESTA ROTADA MEDIANTE LA INCLINACION DE LOS OJOS
            #PERO SOLO SI DETECTA LOS DOS OJOS, SINO EL FILTRO SE PONE NORMAL SIN INCLINACION
            for (x_ojo, y_ojo, ancho_ojo, alto_ojo) in ojos:
                cv2.rectangle(frame[y_cara:y_cara+alto_cara, x_cara:x_cara+ancho_cara], (x_ojo, y_ojo), (x_ojo+ancho_ojo,y_ojo+alto_ojo), (0,255,0), 2)
            if len(ojos) >= 2:
                xOjo1, yOjo1, anchoOjo1, altoOjo1 = ojos[0]
                xOjo2, yOjo2, anchoOjo2, altoOjo2 = ojos[1]
                xCentroOjo1 = (xOjo1 + anchoOjo1) / 2
                yCentroOjo1 = (yOjo1 + altoOjo1) / 2
                xCentroOjo2 = (xOjo2 + anchoOjo2) / 2
                yCentroOjo2 = (yOjo2 + altoOjo2) / 2

                #guia: angulo = atan( (leftEye.y - rightEye.y) / (leftEye.x - rightEye.x) ) ((asi es como se calcula la pendiente de una linea))
                angulo = math.atan((yCentroOjo1 - yCentroOjo2) / (xCentroOjo1-xCentroOjo2))
                angulo = angulo*100 #es que lo de antes te devuelve 0,... y no el angulo tal cual
                cv2.putText(frame, "Angulo de la cabeza:  " + str(round(angulo,5)), (20,30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2) #comprobacion
                
                #si angulo es mayor que 5 por ejemplo (porque suele detectar un ojo un poquito por debajo del otro) se rota el filtro, sino no
                if (angulo > 15 or angulo < -15):
                    rot_mat = cv2.getRotationMatrix2D((ancho_calabaza/2, alto_calabaza/2), -angulo, 0.9) #IMPORTANTE PONER -ANGULO PARA QUE LA CALABAZA ROTE HACIA DONDE TIENE QUE ROTAR Y NO AL LADO CONTRARIO
                    calabazaNueva = cv2.warpAffine(calabazaNueva, rot_mat, (ancho_calabaza, alto_calabaza), flags=cv2.INTER_LINEAR)





            if x_calabaza >= 0 and y_calabaza>= 0 and x_calabaza+ancho_calabaza <= ancho_ventana and y_calabaza+alto_calabaza <= alto_ventana :

                roi = frame[y_calabaza:y_calabaza+alto_calabaza, x_calabaza:x_calabaza+ancho_calabaza]

                roi = cv2.bitwise_and(calabazaNueva, roi) #aqui si se puede porque los cuernos son completamente negros y el fondo es blanco

                frame[y_calabaza:y_calabaza+alto_calabaza, x_calabaza:x_calabaza+ancho_calabaza] = roi


    return frame