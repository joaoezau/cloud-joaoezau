"""Treina o LoRA de estilo lendo os parâmetros de parametros.json.

Rode de dentro da pasta treino/, com o ambiente do sd-scripts ativado:
    python treinar.py            # treina
    python treinar.py --mostrar  # só mostra o comando, sem rodar

Regras do JSON: true vira a opção sozinha (--fp8_base), false é ignorado,
listas viram vários valores (--optimizer_args a b c).
"""
import json
import subprocess
import sys
from pathlib import Path

PASTA = Path(__file__).parent

def montar_comando(params: dict) -> list[str]:
    cmd = [
        sys.executable, "-m", "accelerate.commands.launch",
        "--mixed_precision", params.get("mixed_precision", "bf16"),
        "--num_cpu_threads_per_process", "1",
        str(PASTA / "sd-scripts" / "flux_train_network.py"),
    ]
    for chave, valor in params.items():
        if valor is False or valor is None:
            continue
        cmd.append(f"--{chave}")
        if valor is True:
            continue
        if isinstance(valor, list):
            cmd.extend(str(v) for v in valor)
        else:
            cmd.append(str(valor))
    return cmd

def main() -> None:
    params = json.loads((PASTA / "parametros.json").read_text(encoding="utf-8"))
    cmd = montar_comando(params)
    print(" ".join(cmd), "\n")
    if "--mostrar" in sys.argv:
        return
    sys.exit(subprocess.call(cmd, cwd=PASTA))

if __name__ == "__main__":
    main()
