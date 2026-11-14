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
2. Copie `firebase-secret.example.json` para `firebase-secret.json` e substitua o conteúdo pela chave de serviço **do seu próprio projeto Firebase** (o arquivo real é ignorado pelo Git via `.gitignore`), e ajuste a URL do banco em `firebase.py`.
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

Crie um arquivo `.env` em `registo-de-acesso/` com as variáveis `VITE_API_KEY`, `VITE_PROJECT_ID` e as demais lidas em `src/services/firebase-service.ts` (o `.env` é ignorado pelo Git).

> **Segurança:** o `.gitignore` já impede o commit de `firebase-secret.json` e de arquivos `.env`. Nunca faça commit de chaves reais do Firebase; se uma chave vazar, revogue-a no console do Firebase.
