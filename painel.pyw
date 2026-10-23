"""Painel simples: execute este arquivo com dois cliques no Windows."""

import json
import math
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from irrigacao import calcular_irrigacao


def criar_painel(janela, dados):
    janela.title("Irrigação Inteligente")
    janela.geometry("620x620")
    janela.minsize(560, 600)
    painel = ttk.Frame(janela, padding=24)
    painel.pack(fill="both", expand=True)

    ttk.Label(painel, text="Irrigação Inteligente", font=("Segoe UI", 21, "bold")).pack(anchor="w")
    ttk.Label(painel, text=f"{dados['cultura']} • {dados['local']} • Solo {dados['solo']}").pack(anchor="w", pady=(4, 16))

    entradas = {}
    formulario = ttk.LabelFrame(painel, text="Dados da simulação", padding=14)
    formulario.pack(fill="x")
    formulario.columnconfigure(1, weight=1)
    campos = [
        ("Umidade do solo (%)", "umidade_solo"),
        ("Chuva prevista em 24h (mm)", "chuva_24h"),
        ("Área de cultivo (m²)", "area"),
    ]
    for linha, (rotulo, chave) in enumerate(campos):
        ttk.Label(formulario, text=rotulo).grid(row=linha, column=0, sticky="w", pady=5)
        entrada = ttk.Entry(formulario, width=18)
        entrada.insert(0, str(dados[chave]))
        entrada.grid(row=linha, column=1, sticky="ew", padx=(16, 0), pady=5)
        entradas[chave] = entrada

    decisao = tk.Label(painel, font=("Segoe UI", 16, "bold"), anchor="w")
    motivo = ttk.Label(painel, wraplength=500)
    valores = ttk.Label(painel, font=("Segoe UI", 11), justify="left")

    # O botão lê os campos e chama a mesma função usada na versão de terminal.
    def simular():
        try:
            numeros = [float(entradas[chave].get().strip().replace(",", "."))
                       for _, chave in campos]
            if not all(math.isfinite(numero) for numero in numeros):
                raise ValueError("Preencha os campos com números finitos.")
            resultado = calcular_irrigacao(dados, *numeros)
        except ValueError as erro:
            # Limpa o resultado anterior para evitar confusão com dados inválidos.
            decisao.config(text="Confira os campos", fg="#a52a2a")
            motivo.config(text="Corrija os valores e clique em Simular novamente.")
            valores.config(text="")
            messagebox.showerror("Entrada inválida", str(erro), parent=janela)
            return

        cores = {"IRRIGAR": "#1769aa", "AGUARDAR CHUVA": "#946200", "NÃO IRRIGAR": "#24733d"}
        decisao.config(text=resultado["decisao"], fg=cores[resultado["decisao"]])
        motivo.config(text=resultado["motivo"])
        texto = (
            f"Volume recomendado: {resultado['volume']:.2f} litros\n"
            f"Lâmina recomendada: {resultado['lamina']:.2f} mm\n\n"
            f"ETc estimada: {resultado['etc']:.2f} mm/dia\n"
            f"Déficit estimado: {resultado['deficit_mm']:.2f} mm\n"
            f"Chuva efetiva: {resultado['chuva_efetiva']:.2f} mm"
        )
        valores.config(text=texto.replace(".", ","))

    ttk.Button(painel, text="Simular", command=simular).pack(fill="x", pady=16)
    decisao.pack(fill="x")
    motivo.pack(anchor="w", pady=(6, 14))
    valores.pack(anchor="w")
    ttk.Label(painel, text="Demonstração acadêmica • Dados simulados\nModelo simplificado com parâmetros ilustrativos.",
              foreground="#666666").pack(anchor="w", side="bottom", pady=(16, 0))
    janela.bind("<Return>", lambda evento: simular())
    simular()


def main():
    janela = tk.Tk()
    janela.withdraw()
    try:
        caminho = Path(__file__).resolve().parent / "dados_painel.json"
        with open(caminho, encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        criar_painel(janela, dados)
    except (OSError, ValueError, KeyError, TypeError) as erro:
        messagebox.showerror("Não foi possível abrir o painel",
                             f"Confira o arquivo dados_painel.json.\n\n{erro}", parent=janela)
        janela.destroy()
        return
    janela.deiconify()
    janela.mainloop()


if __name__ == "__main__":
    main()
