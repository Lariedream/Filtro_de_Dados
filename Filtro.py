import os
import csv
import re
import pandas as pd

nome_arquivo = input("Digite o nome inteiro do seu arquivo desejado. Exemplo: Arquivo.csv / Arquivo.xlsx: ")

arquivo_presente = nome_arquivo in os.listdir("dados")

if arquivo_presente:
    nome, extensao = os.path.splitext(nome_arquivo)
    extensao = extensao[1:]  # Remover o ponto da extensão
    if extensao == "csv":    
        with open(os.path.join("dados", nome_arquivo), newline="") as file:     # Lendo os dados do arquivo
            reader = csv.DictReader(file)
            dados = list(reader)
    elif extensao == "xlsx":
        df = pd.read_excel(os.path.join("dados", nome_arquivo), engine="openpyxl", dtype={
    })
    else:
        print("extensão de arquivo não encontrado.")
else:
    print("O arquivo especificado não está presente no diretório 'dados'.")

idadeMinima= int(input("Digite a idade minima: "))

idadeMaxima = int(input("Digite a idade maxima: "))

taxaMinima = input("Digite a taxa mínima: ")
taxaMinima = float(re.sub("[^0-9.]", "", taxaMinima).replace(",", "."))  # Convertendo para float

taxaMaxima = input("Digite a taxa máxima: ")
taxaMaxima = float(re.sub("[^0-9.]", "", taxaMaxima).replace(",", "."))  # Convertendo para float


parcelaMinima = input("Digite o valor mínimo da parcela: ")
parcelaMinima = float(re.sub("[^0-9.]", "", parcelaMinima).replace(",", "."))  # Convertendo para float

parcelaMaxima = input("Digite o valor máximo da parcela: ")
parcelaMaxima = float(re.sub("[^0-9.]", "", parcelaMaxima).replace(",", "."))  # Convertendo para float

if extensao == "csv":
    filtro = []
    for linha in dados:
        if int(linha["Idade"]) >= idadeMinima and int(linha["Idade"]) <= idadeMaxima and float(linha["Taxa"].replace(",", ".")) >= taxaMinima and float(linha["Taxa"].replace(",", ".")) <= taxaMaxima and float(linha["Parcela"].replace(",", ".")) >= parcelaMinima and float(linha["Parcela"].replace(",", ".")) <= parcelaMaxima:
            filtro.append(linha)
    with open("Results.csv", "w", newline="") as file: #abrindo o arquivo csv e inserindo uma linha nova no arquivo
        header= ["Idade", "Taxa", "Parcela"]
        writer= csv.DictWriter(file, fieldnames = header)
        writer.writeheader()
        writer.writerows(filtro)
elif extensao == "xlsx":
    filtro = df[
        (df["Idade"] >= idadeMinima) & (df["Idade"] <= idadeMaxima) &
        (df["Taxa"] >= taxaMinima) & (df["Taxa"] <= taxaMaxima) &
        (df["Parcela"].replace(",", ".") >= parcelaMinima) & 
        (df["Parcela"].replace(",", ".") <= parcelaMaxima)
    ]  # Salvar os resultados no arquivo Results.csv
    filtro.to_csv("Results.csv", index=False)
