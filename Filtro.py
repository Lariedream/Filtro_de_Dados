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
        df = pd.read_excel(os.path.join("dados", nome_arquivo), engine="openpyxl")
    else:
        print("extensão de arquivo não encontrado.")
else:
    print("O arquivo especificado não está presente no diretório 'dados'.")

idadeMinima= int(input("Digite a idade minima: "))

idadeMaxima = int(input("Digite a idade maxima: "))

taxaMinima = float(input("Digite a taxa minima: "))

taxaMaxima = float(input("Digite a taxa maxima: "))


parcelaMinima= input("Digite o valor minimo da parcela: ")
parcelaMinima= parcelaMinima.replace(",",".")  #trocando virgula por ponto final
parcelaMinima= re.sub("[^0-9.]","", parcelaMinima)  #tirando qualquer caracteries especiais ou letras

parcelaMaxima= input("Digite o valor maximo da parcela: ")
parcelaMaxima= parcelaMaxima.replace(",",".")
parcelaMaxima= re.sub("[^0-9.]","", parcelaMaxima)

if extensao == "csv":
    filtro = []
    for linha in dados:
       if int(linha["Idade Minima"]) >= idadeMinima and int(linha["Idade Maxima"]) <= idadeMaxima and float(linha["Taxa Minima"]) >= taxaMinima and float(linha["Taxa Maxima"]) <= taxaMaxima and str(linha["Parcela Minima"]) >= parcelaMinima and str(linha["Parcela Maxima"]) <= parcelaMaxima:
        filtro.append(linha)
    with open("Results.csv", "w", newline="") as file: #abrindo o arquivo csv e inserindo uma linha nova no arquivo
        header= ["Idade Minima", "Idade Maxima", "Taxa Minima", "Taxa Maxima", "Parcela Minima", "Parcela Maxima"]
        writer= csv.DictWriter(file, fieldnames = header)
        writer.writeheader()
        writer.writerows(filtro)
elif extensao == "xlsx":
    df_resultado = pd.DataFrame(columns=["Idade Minima", "Idade Maxima", "Taxa Minima", "Taxa Maxima", "Parcela Minima", "Parcela Maxima"])
    for linha in df.itertuples(index=False):
        if (
            (idadeMinima >= linha[0]) and (idadeMaxima <= linha[1]) and
            (taxaMinima >= linha[2]) and (taxaMaxima <= linha[3]) and
            (parcelaMinima >= linha[4]) and (parcelaMaxima <= linha[5])
        ):
            df_resultado = df_resultado.append(pd.Series(linha, index=df_resultado.columns), ignore_index=True)
        df_resultado.to_excel("Results.xlsx", index=False, engine="openpyxl")