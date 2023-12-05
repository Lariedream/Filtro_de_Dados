import os
import csv
import re
import pandas as pd
from tkinter import *
from tkinter import messagebox


def processar_dados():
    try:
        idade_minima = int(entry_idade_minima.get())
        idade_maxima = int(entry_idade_maxima.get())

        taxa_minima = float(re.sub("[^0-9.]", "", entry_taxa_minima.get()).replace(",", "."))
        taxa_maxima = float(re.sub("[^0-9.]", "", entry_taxa_maxima.get()).replace(",", "."))

        parcela_minima = float(re.sub("[^0-9.]", "", entry_parcela_minima.get()).replace(",", "."))
        parcela_maxima = float(re.sub("[^0-9.]", "", entry_parcela_maxima.get()).replace(",", "."))

        nome_arquivo = entry_nome_arquivo.get()

        arquivo_presente = nome_arquivo in os.listdir("dados")

        if arquivo_presente:
            nome, extensao = os.path.splitext(nome_arquivo)
            extensao = extensao[1:]  # Removendo o ponto da extensão

            if extensao == "csv":    
                with open(os.path.join("dados", nome_arquivo), newline="") as file:
                    reader = csv.DictReader(file)
                    dados = list(reader)
            elif extensao == "xlsx":
                df = pd.read_excel(os.path.join("dados", nome_arquivo), engine="openpyxl", dtype={})
            else:
                messagebox.showerror("Erro", "Extensão de arquivo não encontrada.")
                return
        else:
            messagebox.showerror("O arquivo especificado não está presente no diretório 'dados'.")
            return

        if extensao == "csv":
            filtro = []
            for linha in dados:
                if (
                    int(linha["Idade"]) >= idade_minima and int(linha["Idade"]) <= idade_maxima and
                    float(linha["Taxa"].replace(",", ".")) >= taxa_minima and float(linha["Taxa"].replace(",", ".")) <= taxa_maxima and
                    float(linha["Parcela"].replace(",", ".")) >= parcela_minima and float(linha["Parcela"].replace(",", ".")) <= parcela_maxima
                ):
                    filtro.append(linha)
            with open("Results.csv", "w", newline="") as file:
                header = ["Idade", "Taxa", "Parcela"]
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()
                writer.writerows(filtro)
        elif extensao == "xlsx":
            filtro = df[
                (df["Idade"] >= idade_minima) & (df["Idade"] <= idade_maxima) &
                (df["Taxa"] >= taxa_minima) & (df["Taxa"] <= taxa_maxima) &
                (df["Parcela"].replace(",", ".") >= parcela_minima) &
                (df["Parcela"].replace(",", ".") <= parcela_maxima)
            ]
            filtro.to_csv("Results.csv", index=False)

        messagebox.showinfo("Dados filtrados com sucesso. Resultados salvos em Results.csv.")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

# Criei a janela principal
janela = Tk()
janela.title("Filtro de Dados")

# Adicionei widgets à janela
Label(janela, text="Nome do Arquivo:").pack()
entry_nome_arquivo = Entry(janela)
entry_nome_arquivo.pack()

Label(janela, text="Idade Mínima:").pack()
entry_idade_minima = Entry(janela)
entry_idade_minima.pack()

Label(janela, text="Idade Máxima:").pack()
entry_idade_maxima = Entry(janela)
entry_idade_maxima.pack()

Label(janela, text="Taxa Mínima:").pack()
entry_taxa_minima = Entry(janela)
entry_taxa_minima.pack()

Label(janela, text="Taxa Máxima:").pack()
entry_taxa_maxima = Entry(janela)
entry_taxa_maxima.pack()

Label(janela, text="Parcela Mínima:").pack()
entry_parcela_minima = Entry(janela)
entry_parcela_minima.pack()

Label(janela, text="Parcela Máxima:").pack()
entry_parcela_maxima = Entry(janela)
entry_parcela_maxima.pack()

botao_processar = Button(janela, text="Processar Dados", command=processar_dados)
botao_processar.pack()

janela.mainloop()