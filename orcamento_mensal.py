import pandas as pd

print("=== Analisador de Orçamento Mensal ===")

def ler_valor(msg):
    while True:
        entrada = input(msg).strip()
        try:
            if "," in entrada:
                partes = entrada.split(",")
                if len(partes[-1]) == 3:
                    valor_limpo = entrada.replace(",", "")
                else:
                    valor_limpo = entrada.replace(".", "").replace(",", ".")
            else:
                valor_limpo = entrada
                
            return float(valor_limpo)
        except ValueError:
            print("Erro! Digite apenas números.")

mes = input("Digite o mês do orçamento: ")
renda = ler_valor("Digite sua renda mensal: R$ ")

gastos = {}


print("\nDigite seus gastos fixos:\n")

gastos["Aluguel/Imóvel"] = ler_valor("Aluguel ou parcela do imóvel: R$ ")
gastos["Carro"] = ler_valor("Parcela do carro (0 se não tiver): R$ ")
gastos["Seguro do Carro"] = ler_valor("Seguro do carro: R$ ")
gastos["Luz"] = ler_valor("Conta de luz: R$ ")
gastos["Água"] = ler_valor("Conta de água: R$ ")
gastos["Internet"] = ler_valor("Internet: R$ ")
gastos["Plano de Saúde"] = ler_valor("Plano de saúde: R$ ")
gastos["Streaming"] = ler_valor("Streaming: R$ ")

print("\nDigite outros gastos mensais (0 para parar)\n")

contador = 1

while True:

    valor = ler_valor(f"Outro gasto {contador}: R$ ")

    if valor == 0:
        break

    gastos[f"Outro Gasto {contador}"] = valor
    contador += 1

total_gastos = sum(gastos.values())
saldo = renda - total_gastos

df_gastos = pd.DataFrame(list(gastos.items()), columns=["Despesa", "Valor (R$)"])

df_gastos["Mês"] = mes

linha_total = pd.DataFrame({
    "Despesa": ["TOTAL"],
    "Valor (R$)": [total_gastos],
    "Mês": [mes]
})

df_gastos = pd.concat([df_gastos, linha_total], ignore_index=True)

df_resumo = pd.DataFrame({
    "Descrição": ["Mês", "Renda Mensal", "Total de Gastos", "Saldo Restante"],
    "Valor": [mes, renda, total_gastos, saldo]
})

with pd.ExcelWriter("orcamento_mensal.xlsx") as writer:

    df_gastos.to_excel(writer, sheet_name="Gastos", index=False)

    df_resumo.to_excel(writer, sheet_name="Resumo", index=False)


print("\n=== RESUMO ===")

print(f"Renda mensal: R$ {renda:.2f}")
print(f"Total de gastos: R$ {total_gastos:.2f}")
print(f"Saldo restante: R$ {saldo:.2f}")

print("\nPlanilha criada: orcamento_mensal.xlsx")