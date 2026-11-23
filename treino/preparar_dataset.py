"""Prepara as imagens de referência para o treino do LoRA.

Uso:
    python preparar_dataset.py <pasta_com_as_imagens_originais>

O script:
- copia cada imagem para treino/dataset/ como PNG, com nome numerado;
- reduz o lado maior para no máximo 1536 px (o treino não precisa de mais);
- cria um arquivo .txt de legenda ao lado de cada imagem, começando com a
  palavra-gatilho. Depois, edite cada .txt descrevendo a cena.

Regra das legendas: descreva a CENA (pessoa, pose, roupa, lugar, luz), nunca
nomes de jogo, marca, personagem ou logo. O estilo é aprendido pela
palavra-gatilho; o que você descreve na legenda o modelo NÃO grava como estilo.
"""
import sys
from pathlib import Path

from PIL import Image

GATILHO = "lnd4 style"
LADO_MAX = 1536
EXTENSOES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".dds", ".tga"}

def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    origem = Path(sys.argv[1])
    destino = Path(__file__).parent / "dataset"
    destino.mkdir(exist_ok=True)

    arquivos = sorted(p for p in origem.rglob("*") if p.suffix.lower() in EXTENSOES)
    if not arquivos:
        sys.exit(f"Nenhuma imagem encontrada em {origem}")

    for i, arq in enumerate(arquivos, start=1):
        try:
            img = Image.open(arq).convert("RGB")
        except Exception as erro:  # arquivo corrompido ou formato não suportado
            print(f"Pulando {arq.name}: {erro}")
            continue
        img.thumbnail((LADO_MAX, LADO_MAX), Image.LANCZOS)
        nome = f"{i:03d}"
        img.save(destino / f"{nome}.png")
        legenda = destino / f"{nome}.txt"
        if not legenda.exists():
            legenda.write_text(f"{GATILHO}, DESCREVA A CENA AQUI\n", encoding="utf-8")
        print(f"{arq.name} -> {nome}.png ({img.width}x{img.height})")

    print(f"\nPronto: {len(arquivos)} imagens em {destino}")
    print("Agora edite cada .txt trocando 'DESCREVA A CENA AQUI' pela descrição.")

if __name__ == "__main__":
    main()
