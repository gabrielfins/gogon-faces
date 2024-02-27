import cv2


def capturar():
    classificador = cv2.CascadeClassifier('classificador/haarcascade_frontalface_default.xml')
    camera = cv2.VideoCapture(0)
    amostra = 1
    
    nome = input('Digite seu nome: ')

    ok = True
    while ok:
        ok, imagem = camera.read()
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        
        faces = classificador.detectMultiScale(imagem_cinza, scaleFactor=1.5, minSize=(50, 50))

        for x, y, largura, altura in faces:
            cv2.rectangle(imagem, (x, y), (x + largura, y + altura), (1, 237, 0), 2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                imagem_face = cv2.resize(imagem_cinza[y: y + altura, x: x + largura], (220, 220))
                cv2.imwrite(f'fotos/{nome}{amostra}.jpg', imagem_face)
                
                print(f'Foto {amostra} capturada com sucesso!')
                
                amostra +=1

        cv2.imshow('Face', imagem)

        if cv2.waitKey(1) == 27:
            ok = False

    camera.release()
    cv2.destroyAllWindows()

capturar()
