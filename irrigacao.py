"""Demonstração acadêmica de irrigação inteligente, sem bibliotecas externas."""

import json
from pathlib import Path


def calcular_irrigacao(dados, umidade, chuva, area):
    """Aplica as regras e as fórmulas simplificadas da documentação."""
    if not 0 <= umidade <= 100 or chuva < 0 or area <= 0:
        raise ValueError("Use umidade de 0 a 100, chuva >= 0 e área > 0.")
    if not 0 < dados["eficiencia_irrigacao"] <= 1:
        raise ValueError("A eficiência deve ser maior que 0 e no máximo 1.")

    # Todas as umidades estão em porcentagem. A eficiência é decimal.
    if umidade >= dados["umidade_ideal"]:
        decisao = "NÃO IRRIGAR"
        motivo = "A umidade do solo já está no nível ideal ou acima dele."
    elif chuva >= dados["chuva_minima"]:
        decisao = "AGUARDAR CHUVA"
        motivo = "A chuva prevista atingiu o limite definido para aguardar."
    elif umidade < dados["umidade_minima"]:
        decisao = "IRRIGAR"
        motivo = "O solo está abaixo da umidade mínima e há pouca chuva prevista."
    else:
        decisao = "IRRIGAR"
        motivo = "O solo está abaixo da umidade ideal e há pouca chuva prevista."

    # Estimativa didática: o fator 0.10 não é uma conversão física universal.
    deficit = max(0, dados["umidade_ideal"] - umidade)
    fator_raiz = min(1.5, max(0.5, dados["profundidade_raiz"] / 100))
    deficit_mm = deficit * 0.10 * fator_raiz
    etc = dados["et0"] * dados["kc"]
    chuva_efetiva = min(chuva, deficit_mm)
    necessidade = max(0, deficit_mm + etc - chuva_efetiva)

    # Só recomendar aplicação de água quando a decisão for IRRIGAR.
    lamina = 0
    if decisao == "IRRIGAR":
        lamina = necessidade / dados["eficiencia_irrigacao"]
    volume = lamina * area  # 1 mm sobre 1 m² corresponde a 1 litro.

    return {
        "decisao": decisao,
        "motivo": motivo,
        "etc": etc,
        "deficit_mm": deficit_mm,
        "chuva_efetiva": chuva_efetiva,
        "necessidade": necessidade,
        "lamina": lamina,
        "volume": volume,
    }


def ler_numero(pergunta, padrao, minimo, maximo):
    """Enter mantém o exemplo; aceita tanto vírgula quanto ponto decimal."""
    while True:
        texto = input(f"{pergunta} [{padrao}]: ").strip()
        try:
            valor = float(texto.replace(",", ".")) if texto else padrao
            if minimo <= valor <= maximo:
                return valor
        except ValueError:
            pass
        print(f"Digite um número entre {minimo} e {maximo}.")


def main():
    # No Colab, o JSON deve estar na pasta atual; no PC, ao lado deste código.
    pasta = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    with open(pasta / "dados_painel.json", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    print("IRRIGAÇÃO INTELIGENTE — DEMONSTRAÇÃO ACADÊMICA")
    print(f"{dados['cultura']} | {dados['local']} | Solo {dados['solo']}")
    print("Dados simulados. Chuva = previsão para as próximas 24 horas.")
    print("Pressione Enter para usar os valores do exemplo.\n")

    umidade = ler_numero("Umidade do solo (%)", dados["umidade_solo"], 0, 100)
    chuva = ler_numero("Chuva prevista (mm)", dados["chuva_24h"], 0, 500)
    area = ler_numero("Área de cultivo (m²)", dados["area"], 1, 1000000)
    resultado = calcular_irrigacao(dados, umidade, chuva, area)

    print(f"\nDecisão: {resultado['decisao']}")
    print(f"Motivo: {resultado['motivo']}")
    print(f"ETc estimada: {resultado['etc']:.2f} mm/dia")
    print(f"Déficit estimado: {resultado['deficit_mm']:.2f} mm")
    print(f"Chuva efetiva: {resultado['chuva_efetiva']:.2f} mm")
    print(f"Necessidade líquida estimada: {resultado['necessidade']:.2f} mm")
    print(f"Lâmina recomendada: {resultado['lamina']:.2f} mm")
    print(f"Volume recomendado: {resultado['volume']:.2f} litros")
    print("\nModelo didático simplificado; os parâmetros são ilustrativos.")


if __name__ == "__main__":
    main()
