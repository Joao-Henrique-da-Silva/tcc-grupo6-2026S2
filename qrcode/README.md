# Gerador de QR Codes - TCC Grupo 6

Script Python que gera QR Codes em PNG para as madeiras cadastradas.

## Instalacao

    cd qrcode
    python3.13 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Uso

A partir do CSV padrao:

    python gerar_qrcode.py

A partir de um CSV customizado:

    python gerar_qrcode.py --entrada meu_arquivo.csv --saida ./meus_qrcodes

Direto da API do backend (Flask rodando):

    python gerar_qrcode.py --api http://localhost:5000

## Formato do CSV

    codigo_qr,especie,procedencia,certificacao
    MOG-001,Mogno,Para - Brasil,FSC

## Formato do QR Code

Cada QR Code contem um JSON com codigo_qr, especie, procedencia e certificacao.

## Saida

Os PNGs sao salvos em output/ com o nome do codigo.

## Estrutura

    qrcode/
    ├── gerar_qrcode.py
    ├── requirements.txt
    ├── README.md
    ├── .gitignore
    ├── exemplos/
    │   └── madeiras_exemplo.csv
    └── output/
