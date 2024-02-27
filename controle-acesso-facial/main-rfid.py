import cv2
import statistics
import firebase
from datetime import datetime
from pyfirmata import Arduino, SERVO
from serial import Serial
from time import sleep

print('Carregando...')

porta = 'COM3'
servo = 13
arduino = Arduino(porta)
led_verde = 2
led_amarelo = 3
led_vermelho = 4

serial = Serial()
serial.baudrate = 9600
serial.port = 'COM4'
serial.open()

arduino.digital[servo].mode = SERVO

def girar_servo(angulo):
    arduino.digital[servo].write(angulo)
    sleep(0.01)

def liberar_acesso(method: int, type: int, room: str):
    arduino.digital[led_verde].write(1)
    arduino.digital[led_amarelo].write(0)
    arduino.digital[led_vermelho].write(0)

    girar_servo(90)
    sleep(5)
    girar_servo(0)

    firebase.ref.push({
        'date': datetime.now().isoformat(),
        'method': method,
        'room': room,
        'type': type
    })

def bloquear_acesso():
    arduino.digital[led_verde].write(0)
    arduino.digital[led_amarelo].write(0)
    arduino.digital[led_vermelho].write(1)

    sleep(5)

def resetar_leds():
    arduino.digital[led_verde].write(0)
    arduino.digital[led_amarelo].write(0)
    arduino.digital[led_vermelho].write(0)

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
        try:
            return statistics.mode(ids)
        except:
            return -1
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

def rfid():
    rfid_data = serial.readline()
    
    if rfid_data:
        try:
            rfid_data = rfid_data.decode()
            rfid_data = rfid_data.strip()
            return rfid_data
        except:
            return False
    
def main():
    girar_servo(0)

    fallback = 0

    while True:
        resetar_leds()

        if fallback < 3:
            print('Aguardando rosto...')
        
            numero = 0
            rosto_detectado = monitorar()

            if rosto_detectado:
                numero = capturar()
                
                if numero >= 1:
                    print('Rosto reconhecido!')
                    liberar_acesso(0, 0, 'Sala de Entrada')
                elif numero == -1:
                    print('Rosto não reconhecido!')
                    bloquear_acesso()
                    fallback += 1
        else:
            print('Aguardando RFID...')

            rfid_data = rfid()
            
            if rfid_data:
                print(f'RFID detectado! {rfid_data}')
                liberar_acesso(1, 0, 'Sala de Entrada')                
                fallback = 0

main()
