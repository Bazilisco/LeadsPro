import csv
import json
import pandas as pd
from tkinter import filedialog, messagebox
import os

def obter_dados_da_tabela(treeview):
    """
    Coleta os dados diretamente da Treeview.
    """
    dados = []
    for item in treeview.get_children():
        valores = treeview.item(item)['values']
        if valores:
            dados.append({
                "Nome": valores[0],
                "Endereço": valores[1],
                "Telefone": valores[2],
                "Site": valores[3],
                "Email": valores[4]
            })
    return dados

def exportar_csv(treeview):
    dados = obter_dados_da_tabela(treeview)
    if not dados:
        messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
        return

    caminho = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )
    if not caminho:
        return

    with open(caminho, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=dados[0].keys())
        writer.writeheader()
        writer.writerows(dados)

    messagebox.showinfo("Sucesso", f"Arquivo CSV salvo em:\n{caminho}")

def exportar_excel(treeview):
    dados = obter_dados_da_tabela(treeview)
    if not dados:
        messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
        return

    caminho = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx")]
    )
    if not caminho:
        return

    df = pd.DataFrame(dados)
    df.to_excel(caminho, index=False)

    messagebox.showinfo("Sucesso", f"Arquivo Excel salvo em:\n{caminho}")

def exportar_json(treeview):
    dados = obter_dados_da_tabela(treeview)
    if not dados:
        messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
        return

    caminho = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json")]
    )
    if not caminho:
        return

    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    messagebox.showinfo("Sucesso", f"Arquivo JSON salvo em:\n{caminho}")
