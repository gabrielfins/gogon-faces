import cv2
import statistics
import firebase
from pyfirmata import Arduino, SERVO
from time import sleep
from datetime import datetime

print('Carregando...')

porta = 'COM3'
servo = 13
arduino = Arduino(porta)
led_verde = 2
led_amarelo = 3
led_vermelho = 4

arduino.digital[servo].mode = SERVO

def girar_servo(angulo):
    arduino.digital[servo].write(angulo)
    sleep(0.015)

camera = cv2.VideoCapture(0)
classificador = cv2.CascadeClassifier('classificador/haarcascade_frontalface_default.xml')

print('Classificador carregado!')

reconhecedor = cv2.face.EigenFaceRecognizer_create()
reconhecedor.read('classificadorEigen.yml')

print('Reconhecedor carregado!')

def capturar():
    print('Capturando rosto...')
    ids = []

    i = 0
    while i <= 100:
        ok, imagem = camera.read()
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        faces = classificador.detectMultiScale(imagem_cinza, scaleFactor=1.5, minSize=(50, 50))
        
        for x, y, largura, altura in faces:
            imagem_face = cv2.resize(imagem_cinza[y: y + altura, x: x + largura], (220, 220))
            cv2.rectangle(imagem, (x, y), (x + largura, y + altura), (1, 237, 0), 2)

            id, confianca = reconhecedor.predict(imagem_face)
            ids.append(id)
        
        cv2.imshow('Face', imagem)
        cv2.waitKey(1)

        i += 1

    cv2.destroyAllWindows()

    if ids:
        return statistics.mode(ids)
    else:
        return -1
    
def monitorar():
    while True:
        ok, imagem = camera.read()
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        faces = classificador.detectMultiScale(imagem_cinza, scaleFactor=1.5, minSize=(100, 100))

        if len(faces) > 0:
            print('Rosto detectado!')
            arduino.digital[led_amarelo].write(1)
            return True
        else:
            return False

def main():
    girar_servo(0)

    while True:
        arduino.digital[led_verde].write(0)
        arduino.digital[led_amarelo].write(0)
        arduino.digital[led_vermelho].write(0)

        print('Aguardando rosto...')
        
        numero = 0
        rosto_detectado = monitorar()

        if rosto_detectado:
            numero = capturar()

            if numero == 0:
                pass
            if numero >= 1:
                print('Rosto reconhecido!')
                arduino.digital[led_verde].write(1)
                arduino.digital[led_amarelo].write(0)

                girar_servo(90)
                sleep(5)
                girar_servo(0)

                firebase.ref.push({
                    'date': datetime.now().isoformat(),
                    'method': 0,
                    'room': 'Sala de Entrada',
                    'type': 0
                })
            elif numero == -1:
                print('Rosto não reconhecido!')
                arduino.digital[led_vermelho].write(1)
                arduino.digital[led_amarelo].write(0)
                sleep(5)

main()
