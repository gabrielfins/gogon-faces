# Gogon Faces

Sistema de **controle de acesso por reconhecimento facial e RFID**, com Arduino, visão computacional em Python e painel web de registros de acesso.

Projeto de Extensão da disciplina *Cloud, IoT e Indústria 4.0 em Python* (2023.1) — Universidade Estácio de Sá.

## Como funciona

1. **Cadastro:** a câmera captura amostras do rosto da pessoa (`cadastro.py`).
2. **Treinamento:** as imagens são usadas para treinar um classificador de faces (`treinamento.py`).
3. **Reconhecimento:** ao detectar um rosto (`main.py`) ou ler uma tag RFID (`main-rfid.py`), o sistema decide se o acesso é permitido.
4. **Atuação:** um Arduino aciona um servo (fechadura) e LEDs verde/amarelo/vermelho que indicam o estado.
5. **Registro:** cada acesso é gravado no Firebase Realtime Database e exibido no painel web.

## Estrutura

```
gogon-faces/
├── controle-acesso-facial/   # Python + Arduino
│   ├── cadastro.py           # Captura de fotos do rosto
│   ├── treinamento.py        # Treino do reconhecedor (Eigenfaces / OpenCV)
│   ├── main.py               # Acesso por reconhecimento facial
│   ├── main-rfid.py          # Acesso por RFID
│   ├── firebase.py           # Integração com o Firebase
│   ├── classificador/        # Haar Cascade para detecção de faces
│   ├── StandardFirmata/      # Sketch Arduino (Firmata) usado via pyfirmata
│   └── RFID/                 # Sketch Arduino do leitor RFID (RC522)
├── registo-de-acesso/        # Painel web (React + TypeScript + Vite)
└── CH341SER.ZIP              # Driver USB-serial para placas Arduino com chip CH340/CH341
```

## Tecnologias

- **Python:** OpenCV (`cv2`), NumPy, pyFirmata, pySerial, firebase-admin
- **Hardware:** Arduino, servo motor, LEDs, leitor RFID RC522, câmera
- **Painel web:** React 18, TypeScript, Vite, Sass, Firebase

## Como executar

### Reconhecimento facial (Python)

```bash
cd controle-acesso-facial
pip install opencv-contrib-python numpy pyfirmata pyserial firebase-admin
```

1. Grave o sketch `StandardFirmata` no Arduino e ajuste a porta serial (por padrão `COM3`) em `main.py`.
2. Substitua `firebase-secret.json` pela chave de serviço **do seu próprio projeto Firebase** (o arquivo do repositório é apenas um placeholder) e ajuste a URL do banco em `firebase.py`.
3. Cadastre um rosto, treine e execute:
   ```bash
   python cadastro.py
   python treinamento.py
   python main.py        # ou main-rfid.py para RFID
   ```

### Painel de registros (web)

```bash
cd registo-de-acesso
npm install
npm run dev
```

Configure as credenciais do seu projeto Firebase em `src/services/firebase-service.ts`.

> **Segurança:** nunca faça commit de chaves reais do Firebase. Mantenha o `firebase-secret.json` verdadeiro fora do controle de versão.
