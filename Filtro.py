import os
import csv
import re
import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox

def processar_dados():
    try:
        idade_minima = int(entry_idade_minima.get())
        idade_maxima = int(entry_idade_maxima.get())

        taxa_minima = float(re.sub("[^0-9.]", "", entry_taxa_minima.get()).replace(",", "."))
        taxa_maxima = float(re.sub("[^0-9.]", "", entry_taxa_maxima.get()).replace(",", "."))

        parcela_minima = float(re.sub("[^0-9.]", "", entry_parcela_minima.get()).replace(",", "."))
        parcela_maxima = float(re.sub("[^0-9.]", "", entry_parcela_maxima.get()).replace(",", "."))
        
        

        diretorio_selecionado = filedialog.askdirectory()

        if not diretorio_selecionado:
            messagebox.showinfo("Aviso", "Nenhum diretório selecionado.")
            return
        
        contador_cpf = {}
        
        resultados = []
        
        total_linhas_processadas = 0

        for nome_arquivo in os.listdir(diretorio_selecionado):
            arquivo_path = os.path.join(diretorio_selecionado, nome_arquivo)

            if nome_arquivo.lower().endswith(('.csv', '.xlsx')):
                extensao = nome_arquivo.lower().split('.')[-1]

                if extensao == "csv":
                    with open(arquivo_path, newline="", encoding="utf-8") as file:
                        reader = csv.DictReader(file)
                        for linha in reader:
                            cpf = linha["CPF"]
                            total_linhas_processadas += 1
                            contador_cpf[cpf] = contador_cpf.get(cpf, 0) + 1
                            idade = int(linha["Idade"])
                            taxa = float(linha["Taxa"].replace(",", "."))
                            parcela = float(linha["Parcela"].replace(",", "."))
                            
                            # Formatação para ter dois 0
                            linha_formatada = {
                                "Idade": idade,
                                "Taxa": f"{taxa:.2f}",
                                "Parcela": f"{parcela:.2f}",
                                "CPF": cpf
                            }
                            if (
                                idade >= idade_minima and idade <= idade_maxima and
                                taxa >= taxa_minima and taxa <= taxa_maxima and
                                parcela >= parcela_minima and parcela <= parcela_maxima
                            ):
                                resultados.append(linha_formatada)
                                
                elif extensao == "xlsx":
                    df = pd.read_excel(arquivo_path, engine="openpyxl", dtype={"CPF": str})
                    for _, linha in df.iterrows():
                        cpf = str(linha["CPF"])
                        total_linhas_processadas += 1
                        contador_cpf[cpf] = contador_cpf.get(cpf, 0) + 1
                        idade = int(linha["Idade"])
                        taxa = float(str(linha["Taxa"]).replace(",", "."))
                        parcela = float(str(linha["Parcela"]).replace(",", "."))
                        
                        # Formatação para ter dois 0
                        linha_formatada = {
                            "Idade": idade,
                            "Taxa": f"{taxa:.2f}",
                            "Parcela": f"{parcela:.2f}",
                            "CPF": cpf
                        }
                        if (
                            idade >= idade_minima and idade <= idade_maxima and
                            taxa >= taxa_minima and taxa <= taxa_maxima and
                            parcela >= parcela_minima and parcela <= parcela_maxima
                        ):
                            resultados.append(linha_formatada)
        if not resultados:
            messagebox.showinfo("Aviso", "Nenhum dado encontrado nos arquivos selecionados.")
        else:
            with open("Results.csv", "w", newline="") as file:
                header = ["CPF","Idade", "Taxa", "Parcela","Linhas"]
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writeheader()
                for linha in resultados:
                    linha["Linhas"] = contador_cpf.get(linha["CPF"], 0)
                    writer.writerow(linha)
                messagebox.showinfo("Dados filtrados com sucesso. Resultados salvos em Results.csv.")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

janela = Tk()
janela.title("Filtro de Dados")

# Adicionei widgets à 

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