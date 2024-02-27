import os
import cv2
import numpy

eigenface = cv2.face.EigenFaceRecognizer_create(threshold=10000)

def carregar_imagens():
    caminhos = [os.path.join('fotos', foto) for foto in os.listdir('fotos')]
    faces = []
    ids = []

    for caminho in caminhos:
        imagem_face = cv2.cvtColor(cv2.imread(caminho), cv2.COLOR_BGR2GRAY)
        ids.append(1)
        faces.append(imagem_face)

    return numpy.array(ids), faces

ids, faces = carregar_imagens()

print('Treinando...')

eigenface.train(faces, ids)
eigenface.write('classificadorEigen.yml')

print('Treinamento realizado com sucesso!')
