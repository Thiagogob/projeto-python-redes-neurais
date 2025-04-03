import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

modelo_em_criacao = {
    "nome": "",
    "imagens_personagem1": [],
    "imagens_personagem2": [],
    "atributos_personagem1": {}
}

modelos_salvos = []
janela = tk.Tk()
janela.title("Criar Modelo")
janela.geometry("700x600")

frame_principal = tk.Frame(janela)
frame_principal.pack(fill="both", expand=True)

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
        mostrar_etapa_qtd_atributos()

    tk.Button(frame_principal, text="Selecionar imagens", command=selecionar_arquivos).pack(pady=20)

# ETAPA 4 – Quantidade de atributos
def mostrar_etapa_qtd_atributos():
    limpar_tela()
    tk.Label(frame_principal, text="Etapa 4: Quantos atributos deseja definir?", font=("Arial", 14)).pack(pady=10)
    qtd_entry = tk.Entry(frame_principal)
    qtd_entry.pack()

    def avancar():
        try:
            qtd = int(qtd_entry.get())
            janela.qtd_atributos = qtd
            janela.indice_atual = 0
            janela.nomes_atributos = []
            mostrar_etapa_nome_atributo()
        except ValueError:
            print("Digite um número válido")

    tk.Button(frame_principal, text="Avançar", command=avancar).pack(pady=10)

# ETAPA 5 – Nome do atributo
def mostrar_etapa_nome_atributo():
    limpar_tela()
    i = janela.indice_atual + 1
    tk.Label(frame_principal, text=f"Etapa 5.{i}: Nome do Atributo {i}", font=("Arial", 14)).pack(pady=10)
    nome_entry = tk.Entry(frame_principal)
    nome_entry.pack()

    def avancar():
        nome = nome_entry.get().strip()
        if nome:
            janela.nomes_atributos.append(nome)
            mostrar_conta_gotas(nome)
        else:
            print("Nome inválido")

    tk.Button(frame_principal, text="Avançar", command=avancar).pack(pady=10)

# ETAPA 6 – Conta-gotas com clique na imagem
def mostrar_conta_gotas(nome_atributo):
    limpar_tela()
    tk.Label(frame_principal, text=f"Selecione uma cor para: {nome_atributo}", font=("Arial", 14)).pack(pady=10)

    caminho_imagem = modelo_em_criacao["imagens_personagem1"][0]
    imagem_pil = Image.open(caminho_imagem)
    imagem_pil.thumbnail((500, 500))
    imagem_tk = ImageTk.PhotoImage(imagem_pil)

    canvas = tk.Canvas(frame_principal, width=imagem_pil.width, height=imagem_pil.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=imagem_tk)
    canvas.imagem_tk = imagem_tk
    canvas.imagem_pil = imagem_pil

    # Label para mostrar a cor selecionada
    cor_label = tk.Label(frame_principal, text="Clique em uma cor", width=30, height=2, relief="solid")
    cor_label.pack(pady=15)

    pixels = imagem_pil.load()

    def clique(event):
        x, y = event.x, event.y
        r, g, b = pixels[x, y][:3]
        margem = 30

        cor_min = (max(0, r - margem), max(0, g - margem), max(0, b - margem))
        cor_max = (min(255, r + margem), min(255, g + margem), min(255, b + margem))

        modelo_em_criacao["atributos_personagem1"][nome_atributo] = {
            "min": cor_min,
            "max": cor_max
        }

        cor_hex = f'#{r:02x}{g:02x}{b:02x}'
        cor_label.config(bg=cor_hex, text=f"RGB: ({r}, {g}, {b})", fg="white" if r+g+b < 382 else "black")

        janela.indice_atual += 1
        if janela.indice_atual < janela.qtd_atributos:
            janela.after(1000, mostrar_etapa_nome_atributo)  # espera 1s e vai pro próximo
        else:
            janela.after(1000, salvar_modelo_final)

    canvas.bind("<Button-1>", clique)

# FINAL – Salvar tudo
def salvar_modelo_final():
    modelos_salvos.append(modelo_em_criacao.copy())
    print("Modelo salvo com sucesso!\n", modelo_em_criacao)
    mostrar_tela_criar_modelo()

# Menu superior
menu = tk.Frame(janela)
menu.pack(side="top", fill="x")
tk.Button(menu, text="Criar modelo", command=mostrar_tela_criar_modelo).pack(side="left", padx=5, pady=5)

# Inicializa a primeira tela
mostrar_tela_criar_modelo()
janela.mainloop()
