# Treino do LoRA de estilo (RTX 3060 12 GB)

Kit para treinar o LoRA da Fase 1 do `PLANO.md` no **FLUX.1-dev**, usando o
[kohya sd-scripts](https://github.com/kohya-ss/sd-scripts).

As pastas `dataset/`, `modelos/`, `saida/`, `cache/` e `sd-scripts/` ficam
**fora do Git** (estão no `.gitignore`).

## Requisitos

- RTX 3060 12 GB, com driver NVIDIA atualizado
- **32 GB de RAM** (com 16 GB pode travar ao carregar o T5)
- ~60 GB livres em disco (SSD de preferência)
- Python 3.10 ou 3.11, Git

## 1. Instalar o sd-scripts

Dentro da pasta `treino/`:

```
git clone https://github.com/kohya-ss/sd-scripts
cd sd-scripts
python -m venv venv
```

Ative o ambiente: `venv\Scripts\activate` no Windows, ou `source venv/bin/activate` no Linux.

```
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
accelerate config default
cd ..
```

Confira se existe `sd-scripts/flux_train_network.py`. Se não existir, rode
`git checkout sd3` dentro de `sd-scripts/` e repita o `pip install -r requirements.txt`.

## 2. Baixar os modelos para `treino/modelos/`

| Arquivo | Onde baixar |
|---|---|
| `flux1-dev.safetensors` | huggingface.co/black-forest-labs/FLUX.1-dev (aceite a licença no site antes) |
| `ae.safetensors` | mesmo repositório acima |
| `clip_l.safetensors` | huggingface.co/comfyanonymous/flux_text_encoders |
| `t5xxl_fp16.safetensors` | mesmo repositório acima |

Com pouca RAM, use `t5xxl_fp8_e4m3fn.safetensors` e ajuste o caminho em `parametros.json`.

## 3. Preparar as imagens

Junte as 20 a 30 artes numa pasta qualquer e rode:

```
python preparar_dataset.py C:\caminho\das\imagens
```

Depois edite cada `.txt` em `dataset/`. Exemplo:

```
lnd4 style, a woman in a red bikini leaning on a white convertible, palm trees, sunset, ocean in the background
```

- Comece sempre com `lnd4 style` (palavra-gatilho)
- Descreva a cena, a pessoa, a roupa e o lugar. **Nada de nomes de jogo, marca, personagem ou logo.**
- Escolha variedade: personagens de corpo inteiro, retratos, cenas de cidade, praia, noite

## 4. Treinar

```
python treinar.py --mostrar
python treinar.py
```

Na primeira execução, o script gera o cache de latentes e textos e só depois começa o treino.
Com 25 imagens, são ~2.000 passos. Na 3060, conte **algumas horas** (por volta de 3 a 6 h).

A cada 2 épocas é salvo um arquivo em `saida/` (`lnd4-style-000002.safetensors`, ...).
Teste os intermediários também: às vezes uma época do meio fica melhor que a final.

## Ajustes no `parametros.json`

| Sintoma | O que mudar |
|---|---|
| Erro de memória (CUDA out of memory) | `blocks_to_swap` para 20 ou 24; `resolution` em `dataset.toml` para 640 |
| Estilo fraco | `max_train_epochs` para 12, ou `network_dim` para 32 |
| Imagens todas iguais, "decoradas" | Use uma época anterior, ou `learning_rate` para 0.00005 |
| Muito lento | `blocks_to_swap` menor (12), se a memória deixar |

## 5. Testar

Carregue o `.safetensors` no ComfyUI ou no Forge com o FLUX.1-dev e use prompts como
`lnd4 style, a man in a hawaiian shirt standing next to a sports car at night, neon lights`.

Depois suba o melhor arquivo no fal.ai ou no Replicate para usar no site.
