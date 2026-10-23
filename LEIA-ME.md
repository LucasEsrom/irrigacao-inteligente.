# Irrigação Inteligente — demonstração inicial

Exemplo em Python baseado na documentação enviada. Usa dados simulados de milho em Rio Branco, solo argiloso e irrigação por aspersão. Não consulta a Open-Meteo nem aciona equipamentos. Não precisa instalar bibliotecas.

## Como executar

### Painel sem terminal (Windows)

Dê dois cliques em `painel.pyw`. Mantenha esse arquivo, `irrigacao.py` e `dados_painel.json` na mesma pasta. Se o Windows pedir um aplicativo, selecione o Python. A extensão `.pyw` abre a janela sem o console na instalação padrão do Python para Windows.

O painel mostra o exemplo inicial automaticamente. Altere os três campos e clique em **Simular**, ou pressione Enter. Os valores aceitam ponto ou vírgula decimal.

O painel usa Tkinter, incluído na instalação padrão do Python para Windows, e funciona localmente no computador. O Colab pode executar a versão de texto abaixo, mas não essa janela.

Para explicar a interface: `Entry` cria os campos, `Button` cria o botão e `Label` mostra os resultados. A função `simular()` lê os campos e chama `calcular_irrigacao()`, reaproveitando a lógica existente.

### Versão de texto e Colab

No computador com Python instalado, mantenha `irrigacao.py` e `dados_painel.json` juntos, abra o terminal nessa pasta e execute:

```text
python irrigacao.py
```

Se o Windows usar o comando `py`, execute `py irrigacao.py`.

No Google Colab, envie `dados_painel.json` pelo painel de arquivos à esquerda. Cole o conteúdo de `irrigacao.py` em uma célula de código e execute. O arquivo enviado fica temporariamente no ambiente do Colab.

Digite a umidade, a chuva prevista e a área quando solicitado. Enter usa o valor do exemplo. São aceitos ponto ou vírgula decimal. Para testar outro cenário, execute novamente.

## Três cenários para apresentar

| Umidade (%) | Chuva prevista (mm) | Área (m²) | Resultado esperado |
|---|---|---|---|
| 20 | 0 | 100 | IRRIGAR; 3,4375 mm e 343,75 litros |
| 20 | 5 | 100 | AGUARDAR CHUVA; aplicação recomendada de 0 litros |
| 35 | 0 | 100 | NÃO IRRIGAR; aplicação recomendada de 0 litros |

## Como explicar ao professor

“O programa lê um arquivo JSON com os dados do cultivo e os parâmetros. Depois recebe umidade, chuva prevista e área. Compara a umidade com o nível ideal e verifica a previsão de chuva. Se precisar irrigar, estima a falta de água, considera a demanda da cultura, corrige as perdas da irrigação e calcula o volume para a área.”

- `json.load()` transforma o arquivo JSON em um dicionário Python.
- Uma variável guarda um valor, como a área de cultivo.
- A função `calcular_irrigacao()` reúne a lógica e devolve os resultados.
- `if`, `elif` e `else` escolhem a regra aplicável, em ordem.
- `max(0, ...)` impede valores negativos no déficit e na necessidade.
- `return` devolve os resultados; `print()` os mostra na tela.

## Cálculo do primeiro cenário

1. ETc = ET₀ × Kc = 4 × 0,5 = **2 mm/dia**.
2. Diferença de umidade = 35 − 20 = **15 pontos percentuais**.
3. Fator de raiz = 50 / 100 = **0,5**, limitado entre 0,5 e 1,5.
4. Déficit estimado = 15 × 0,10 × 0,5 = **0,75 mm**.
5. Chuva efetiva = menor valor entre 0 e 0,75 = **0 mm**.
6. Necessidade líquida = 0,75 + 2 − 0 = **2,75 mm**.
7. Lâmina = 2,75 / 0,80 = **3,4375 mm**.
8. Volume = 3,4375 × 100 = **343,75 litros**.

O cálculo considera um dia de ETc. A necessidade estimada pode aparecer positiva mesmo quando a regra manda aguardar ou não irrigar; nesses casos a lâmina e o volume recomendados são zero, conforme o roteiro.

## Escolhas e limites desta versão

Todos os valores de umidade usam porcentagem: 35 significa 35%, e não 0,35. A eficiência usa decimal: 0,8 significa 80%. A profundidade das raízes está em centímetros; a área, em m².

Nesta demonstração, `chuva_24h` significa chuva **prevista para as próximas 24 horas**, para dar sentido à decisão de aguardar chuva. Não misture esse valor com chuva já ocorrida.

Os parâmetros do JSON são exemplos escolhidos para demonstrar as regras; a documentação não fornece uma calibração completa. O fator 0,10 e a chuva efetiva seguem as simplificações do roteiro. O programa demonstra decisões e cálculos, mas não representa um modelo agronômico validado para irrigação real.

Gráficos, controles deslizantes e integração meteorológica ficam para uma próxima etapa, mantendo esta primeira versão curta e fácil de explicar.
