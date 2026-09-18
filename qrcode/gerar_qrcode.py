#!/usr/bin/env python3
"""Gerador de QR Codes - TCC Grupo 6"""
import argparse
import csv
import json
import sys
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont


PASTA_ATUAL = Path(__file__).parent.resolve()
ENTRADA_PADRAO = PASTA_ATUAL / "exemplos" / "madeiras_exemplo.csv"
SAIDA_PADRAO = PASTA_ATUAL / "output"


def gerar_qrcode(dados, pasta_saida):
    codigo = dados["codigo_qr"]
    payload = json.dumps({
        "codigo_qr": codigo,
        "especie": dados.get("especie", ""),
        "procedencia": dados.get("procedencia", ""),
        "certificacao": dados.get("certificacao", ""),
    }, ensure_ascii=False)

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(payload)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = _adicionar_legenda(img, codigo)

    arquivo = pasta_saida / f"{codigo}.png"
    img.save(arquivo)
    return arquivo


def _adicionar_legenda(img, texto):
    largura, altura = img.size
    altura_legenda = 60
    nova = Image.new("RGB", (largura, altura + altura_legenda), "white")
    nova.paste(img, (0, 0))
    draw = ImageDraw.Draw(nova)
    try:
        fonte = ImageFont.truetype(
            "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 28
        )
    except (OSError, IOError):
        fonte = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), texto, font=fonte)
    largura_texto = bbox[2] - bbox[0]
    x = (largura - largura_texto) // 2
    y = altura + (altura_legenda - (bbox[3] - bbox[1])) // 2 - bbox[1] // 2
    draw.text((x, y), texto, fill="black", font=fonte)
    return nova


def ler_csv(caminho):
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {caminho}")
    with caminho.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ler_api(url):
    import urllib.request
    endpoint = f"{url.rstrip('/')}/api/madeiras"
    with urllib.request.urlopen(endpoint, timeout=10) as resposta:
        return json.loads(resposta.read().decode("utf-8"))


def main():
    parser = argparse.ArgumentParser(
        description="Gera QR Codes para as madeiras do sistema do TCC."
    )
    parser.add_argument("--entrada", type=Path, default=ENTRADA_PADRAO)
    parser.add_argument("--saida", type=Path, default=SAIDA_PADRAO)
    parser.add_argument("--api", type=str, default=None)
    args = parser.parse_args()
    args.saida.mkdir(parents=True, exist_ok=True)

    if args.api:
        print(f"Buscando madeiras de: {args.api}/api/madeiras")
        try:
            madeiras = ler_api(args.api)
        except Exception as e:
            print(f"Erro ao acessar a API: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Lendo CSV: {args.entrada}")
        madeiras = ler_csv(args.entrada)

    if not madeiras:
        print("Nenhuma madeira encontrada.", file=sys.stderr)
        sys.exit(1)

    print(f"Gerando {len(madeiras)} QR Code(s)...\n")
    for m in madeiras:
        try:
            arquivo = gerar_qrcode(m, args.saida)
            print(f"  OK  {arquivo.name}")
        except Exception as e:
            print(f"  ERRO em '{m.get('codigo_qr', '???')}': {e}",
                  file=sys.stderr)
    print(f"\nPronto! Arquivos em: {args.saida}")


if __name__ == "__main__":
    main()
