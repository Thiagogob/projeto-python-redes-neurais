import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import os


modelo_em_criacao = {
    "nome": "",
    "imagens_personagem1": [],
    "imagens_personagem2": [],
    "atributos_personagem1": {},
    "atributos_personagem2": {}

}

modelos_salvos = []
janela = tk.Tk()
janela.title("Criar Modelo")
janela.geometry("700x600")

frame_principal = tk.Frame(janela)
frame_principal.pack(fill="both", expand=True)

def mostrar_tela_inicial():
    limpar_tela()
    tk.Label(frame_principal, text="Menu Principal", font=("Arial", 18)).pack(pady=30)

    tk.Button(frame_principal, text="Criar modelo", width=20, command=mostrar_tela_criar_modelo).pack(pady=10)
    tk.Button(frame_principal, text="Botão 2 (futuro)", width=20, command=lambda: print("Botão 2 clicado")).pack(pady=10)
    tk.Button(frame_principal, text="Botão 3 (futuro)", width=20, command=lambda: print("Botão 3 clicado")).pack(pady=10)
    tk.Button(frame_principal, text="Botão 4 (futuro)", width=20, command=lambda: print("Botão 4 clicado")).pack(pady=10)


def limpar_tela():
    for widget in frame_principal.winfo_children():
        widget.destroy()

# ETAPA 1 – Nome
def mostrar_tela_criar_modelo():
    limpar_tela()
    tk.Label(frame_principal, text="Etapa 1: Nome do Modelo", font=("Arial", 14)).pack(pady=10)
    nome_entry = tk.Entry(frame_principal, width=30)
    nome_entry.pack(pady=5)

    def salvar_nome():
        modelo_em_criacao["nome"] = nome_entry.get().strip()
        mostrar_upload_personagem1()
    
    tk.Button(frame_principal, text="Avançar", command=salvar_nome).pack(pady=10)

# ETAPA 2 – Upload imagens personagem 1
def mostrar_upload_personagem1():
    limpar_tela()
    tk.Label(frame_principal, text="Etapa 2: Upload de Imagens do Personagem 1", font=("Arial", 14)).pack(pady=10)

    def selecionar_arquivos():
        arquivos = filedialog.askopenfilenames(title="Selecione as imagens do personagem 1")
        modelo_em_criacao["imagens_personagem1"] = list(arquivos)
        mostrar_upload_personagem2()

    tk.Button(frame_principal, text="Selecionar imagens", command=selecionar_arquivos).pack(pady=20)

# ETAPA 3 – Upload imagens personagem 2
def mostrar_upload_personagem2():
    limpar_tela()
    tk.Label(frame_principal, text="Etapa 3: Upload de Imagens do Personagem 2", font=("Arial", 14)).pack(pady=10)

    def selecionar_arquivos():
        arquivos = filedialog.askopenfilenames(title="Selecione as imagens do personagem 2")
        modelo_em_criacao["imagens_personagem2"] = list(arquivos)
        mostrar_etapa_qtd_atributos(personagem=1)

    tk.Button(frame_principal, text="Selecionar imagens", command=selecionar_arquivos).pack(pady=20)

# ETAPA 4 – Quantidade de atributos
def mostrar_etapa_qtd_atributos(personagem):
    limpar_tela()
    tk.Label(frame_principal, text=f"Personagem {personagem}: Quantos atributos deseja definir?", font=("Arial", 14)).pack(pady=10)
    qtd_entry = tk.Entry(frame_principal)
    qtd_entry.pack()

    def avancar():
        try:
            qtd = int(qtd_entry.get())
            if personagem == 1:
                janela.qtd_atributos = qtd
                janela.indice_atual = 0
                janela.nomes_atributos = []
            else:
                janela.qtd_atributos_p2 = qtd
                janela.indice_atual_p2 = 0
                janela.nomes_atributos_p2 = []
            mostrar_etapa_nome_atributo(personagem)
        except ValueError:
            print("Digite um número válido")

    tk.Button(frame_principal, text="Avançar", command=avancar).pack(pady=10)

# ETAPA 5 – Nome do atributo
def mostrar_etapa_nome_atributo(personagem):
    limpar_tela()
    i = (janela.indice_atual if personagem == 1 else janela.indice_atual_p2) + 1
    tk.Label(frame_principal, text=f"Personagem {personagem} – Nome do Atributo {i}", font=("Arial", 14)).pack(pady=10)
    nome_entry = tk.Entry(frame_principal)
    nome_entry.pack()

    def avancar():
        nome = nome_entry.get().strip()
        if nome:
            if personagem == 1:
                janela.nomes_atributos.append(nome)
            else:
                janela.nomes_atributos_p2.append(nome)
            mostrar_conta_gotas(nome, personagem)
        else:
            print("Nome inválido")

    tk.Button(frame_principal, text="Avançar", command=avancar).pack(pady=10)

# ETAPA 6 – Conta-gotas com clique na imagem
def mostrar_conta_gotas(nome_atributo, personagem):
    limpar_tela()
    tk.Label(frame_principal, text=f"Selecione uma cor para: {nome_atributo} (Personagem {personagem})", font=("Arial", 14)).pack(pady=10)

    caminho_imagem = modelo_em_criacao[f"imagens_personagem{personagem}"][0]
    imagem_pil = Image.open(caminho_imagem)
    imagem_pil.thumbnail((500, 500))
    imagem_tk = ImageTk.PhotoImage(imagem_pil)

    canvas = tk.Canvas(frame_principal, width=imagem_pil.width, height=imagem_pil.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=imagem_tk)
    canvas.imagem_tk = imagem_tk
    canvas.imagem_pil = imagem_pil

    pixels = imagem_pil.load()

    def clique(event):
        x, y = event.x, event.y
        r, g, b = pixels[x, y][:3]
        margem = 30

        cor_min = (max(0, r - margem), max(0, g - margem), max(0, b - margem))
        cor_max = (min(255, r + margem), min(255, g + margem), min(255, b + margem))
        cor_hex = f'#{r:02x}{g:02x}{b:02x}'

        mostrar_confirmacao_cor(nome_atributo, (r, g, b), cor_min, cor_max, cor_hex, personagem)

    canvas.bind("<Button-1>", clique)

def mostrar_confirmacao_cor(nome_atributo, rgb, cor_min, cor_max, cor_hex, personagem):
    limpar_tela()
    tk.Label(frame_principal, text=f"Confirmação da Cor (Personagem {personagem})", font=("Arial", 16)).pack(pady=10)

    label_cor = tk.Label(frame_principal, text=f"RGB: {rgb}", width=30, height=2, bg=cor_hex,
                         fg="white" if sum(rgb) < 382 else "black", relief="solid")
    label_cor.pack(pady=15)

    texto = f"Manter essa cor como referência para o atributo '{nome_atributo}'?"
    tk.Label(frame_principal, text=texto, font=("Arial", 12)).pack(pady=10)

    def confirmar():
        modelo_em_criacao[f"atributos_personagem{personagem}"][nome_atributo] = {
            "min": cor_min,
            "max": cor_max
        }

        if personagem == 1:
            janela.indice_atual += 1
            if janela.indice_atual < janela.qtd_atributos:
                mostrar_etapa_nome_atributo(personagem)
            else:
                mostrar_etapa_qtd_atributos(personagem=2)
        else:
            janela.indice_atual_p2 += 1
            if janela.indice_atual_p2 < janela.qtd_atributos_p2:
                mostrar_etapa_nome_atributo(personagem)
            else:
                salvar_modelo_final()

    def tentar_novamente():
        mostrar_conta_gotas(nome_atributo, personagem)

    botoes = tk.Frame(frame_principal)
    botoes.pack(pady=20)

    tk.Button(botoes, text="✅ Confirmar", command=confirmar, width=15).pack(side="left", padx=10)
    tk.Button(botoes, text="❌ Selecionar outra cor", command=tentar_novamente, width=20).pack(side="left", padx=10)

def gerar_csv(modelo):
    atributos_p1 = modelo["atributos_personagem1"]
    atributos_p2 = modelo["atributos_personagem2"]

    imagens = modelo["imagens_personagem1"] + modelo["imagens_personagem2"]
    atributos = {**atributos_p1, **atributos_p2}

    colunas = ["imagem"] + list(atributos.keys())
    linhas = []

    def contar_pixels(imagem_path, atributos):
        imagem = Image.open(imagem_path).convert("RGB")
        pixels = imagem.load()
        largura, altura = imagem.size

        contagens = {nome: 0 for nome in atributos}

        for x in range(largura):
            for y in range(altura):
                r, g, b = pixels[x, y]
                for nome, faixa in atributos.items():
                    rmin, gmin, bmin = faixa["min"]
                    rmax, gmax, bmax = faixa["max"]
                    if rmin <= r <= rmax and gmin <= g <= gmax and bmin <= b <= bmax:
                        contagens[nome] += 1

        return contagens, largura * altura

    def normalizar(valor, total_pixels):
        if total_pixels == 0:
            return 0
        porcentagem = valor / total_pixels
        if porcentagem == 0:
            return 0
        elif porcentagem > 0.02:
            return 10
        else:
            return round(porcentagem / 0.02 * 10)

    for img in imagens:
        contagens, total = contar_pixels(img, atributos)
        linha = [os.path.basename(img)]
        for nome in atributos:
            linha.append(normalizar(contagens[nome], total))
        linhas.append(linha)

    with open("dados_personagens.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(colunas)
        writer.writerows(linhas)

    print("Arquivo CSV 'dados_personagens.csv' gerado com sucesso!")

# FINAL – Salvar tudo
def salvar_modelo_final():
    modelos_salvos.append(modelo_em_criacao.copy())
    gerar_csv(modelo_em_criacao)
    print("Modelo salvo com sucesso!\n", modelo_em_criacao)
    mostrar_tela_inicial()

# Menu superior
menu = tk.Frame(janela)
menu.pack(side="top", fill="x")
tk.Button(menu, text="Criar modelo", command=mostrar_tela_criar_modelo).pack(side="left", padx=5, pady=5)

# Inicializa a tela inicial
mostrar_tela_inicial()
janela.mainloop()

