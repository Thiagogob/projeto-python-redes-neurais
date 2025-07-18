import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import os


modelo_em_criacao = {
    "nome": "",
    "personagem1": "",
    "personagem2": "",
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

    tk.Button(frame_principal, text="Criar modelo baseado em RGB", width=30, command=mostrar_tela_criar_modelo).pack(pady=10)
    tk.Button(frame_principal, text="Testar modelo RGB", width=30, command=mostrar_tela_testar_modelo).pack(pady=10)
    tk.Button(frame_principal, text="Criar modelo rede convolucional", width=30, command=iniciar_fluxo_cnn).pack(pady=10)
    tk.Button(frame_principal, text="Testar modelo convolucional", width=30, command=mostrar_tela_testar_modelo_cnn).pack(pady=10)



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
        mostrar_nomes_personagens()
    
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

        # Verifica se o fluxo é CNN
        if modelo_em_criacao.get("tipo_modelo") == "cnn":
            treinar_modelo_cnn()
        else:
            mostrar_etapa_qtd_atributos(personagem=1)


    tk.Button(frame_principal, text="Selecionar imagens", command=selecionar_arquivos).pack(pady=20)

def mostrar_nomes_personagens():
    limpar_tela()
    tk.Label(frame_principal, text="Nome dos Personagens", font=("Arial", 14)).pack(pady=10)

    tk.Label(frame_principal, text="Nome do Personagem 1").pack()
    p1_entry = tk.Entry(frame_principal)
    p1_entry.pack(pady=5)

    tk.Label(frame_principal, text="Nome do Personagem 2").pack()
    p2_entry = tk.Entry(frame_principal)
    p2_entry.pack(pady=5)

    def avancar():
        modelo_em_criacao["personagem1"] = p1_entry.get().strip()
        modelo_em_criacao["personagem2"] = p2_entry.get().strip()
        mostrar_upload_personagem1()

    tk.Button(frame_principal, text="Avançar", command=avancar).pack(pady=10)


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
            "referencia": rgb
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

def cor_esta_na_faixa(pixel_rgb, cor_referencia, tolerancia=25):
    r1, g1, b1 = pixel_rgb
    r2, g2, b2 = cor_referencia
    dist = ((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2) ** 0.5
    return dist <= tolerancia

def contar_por_distancia_com_area_util(imagem_path, atributos, tolerancia):
        imagem = Image.open(imagem_path).convert("RGB")
        pixels = imagem.load()
        largura, altura = imagem.size

        contagens = {nome: 0 for nome in atributos}
        total_relevante = 0

        for x in range(largura):
            for y in range(altura):
                r, g, b = pixels[x, y]
                bateu_em_algum = False
                for nome, dados in atributos.items():
                    ref = dados["referencia"]
                    if cor_esta_na_faixa((r, g, b), ref, tolerancia):
                        contagens[nome] += 1
                        bateu_em_algum = True
                if bateu_em_algum:
                    total_relevante += 1

        return contagens, total_relevante

def gerar_csv(modelo, tolerancia=25):
    from PIL import Image
    import csv
    import os

    atributos_p1 = modelo["atributos_personagem1"]
    atributos_p2 = modelo["atributos_personagem2"]

    imagens = modelo["imagens_personagem1"] + modelo["imagens_personagem2"]
    atributos = {**atributos_p1, **atributos_p2}

    colunas = ["imagem"] + list(atributos.keys()) + ["classe"]

    linhas = []


    for img in imagens:
        contagens, total_util = contar_por_distancia_com_area_util(img, atributos, tolerancia)
        linha = [os.path.basename(img)]
        for nome in atributos:
            proporcao = contagens[nome] / total_util if total_util else 0
            linha.append(round(proporcao * 10, 4))
    
        # Define a classe com base no nome do personagem correspondente
        if img in modelo["imagens_personagem1"]:
            classe = modelo["personagem1"]
        else:
            classe = modelo["personagem2"]
        linha.append(classe)

        linhas.append(linha)



    with open("dados_personagens.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(colunas)
        writer.writerows(linhas)

    print("CSV gerado com sucesso usando distância de cor com tolerância =", tolerancia)





# FINAL – Salvar tudo
def salvar_modelo_final():
    modelos_salvos.append(modelo_em_criacao.copy())
    gerar_csv(modelo_em_criacao)
    print("Modelo salvo com sucesso!\n", modelo_em_criacao)
    treinar_modelo()
    mostrar_tela_inicial()
    janela.after(100, mostrar_tela_inicial)
# Menu superior
menu = tk.Frame(janela)
menu.pack(side="top", fill="x")
tk.Button(menu, text="Criar modelo", command=mostrar_tela_criar_modelo).pack(side="left", padx=5, pady=5)

# ETAPA EXTRA – Treinar modelo com dados do CSV
def treinar_modelo():
    import pandas as pd
    import tensorflow as tf
    from sklearn.model_selection import train_test_split

    dataset = pd.read_csv("dados_personagens.csv")

    # X = atributos (depois da coluna 'imagem', antes da última 'classe')
    X = dataset.iloc[:, 1:-1].values
    y = dataset.iloc[:, -1].values

    y = (y == modelo_em_criacao["personagem1"])

    # separa dados para treino e teste
    #X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(X, y, test_size=0.2)

    # modelo de rede neural
    input_dim = X.shape[1]  # número de atributos

    rede_neural = tf.keras.models.Sequential()
    rede_neural.add(tf.keras.layers.Dense(units=16, activation='relu', input_shape=(input_dim,)))
    rede_neural.add(tf.keras.layers.Dense(units=8, activation='relu'))
    rede_neural.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

    rede_neural.compile(optimizer='Adam', loss='binary_crossentropy', metrics=['accuracy'])

    historico = rede_neural.fit(X, y, epochs=300, validation_split=0.15)

    print("Rede neural treinada com sucesso!")

    import json

    dados = {
        "personagem1": modelo_em_criacao["personagem1"],
        "personagem2": modelo_em_criacao["personagem2"],
        "atributos_personagem1": modelo_em_criacao["atributos_personagem1"],
        "atributos_personagem2": modelo_em_criacao["atributos_personagem2"]
    }

    nome_base = modelo_em_criacao["nome"]
    with open(f"{nome_base}.json", "w") as f:
        json.dump(dados, f)


    rede_neural.save(f"{nome_base}.keras")


def testar_modelo(nome_arquivo_modelo):
    import pandas as pd
    import tensorflow as tf
    from tkinter import filedialog
    import numpy as np
    from PIL import Image, ImageTk

    # Seleciona imagem
    caminho_imagem = filedialog.askopenfilename(title="Escolha uma imagem para testar")
    if not caminho_imagem:
        return

    # Carrega modelo
    modelo = tf.keras.models.load_model(nome_arquivo_modelo)

    import json
    import os

    json_path = os.path.splitext(nome_arquivo_modelo)[0] + ".json"
    with open(json_path, "r") as f:
        dados = json.load(f)

    modelo_em_criacao["personagem1"] = dados["personagem1"]
    modelo_em_criacao["personagem2"] = dados["personagem2"]
    modelo_em_criacao["atributos_personagem1"] = dados["atributos_personagem1"]
    modelo_em_criacao["atributos_personagem2"] = dados["atributos_personagem2"]


    # Lê CSV para pegar ordem dos atributos
    atributos_csv = pd.read_csv("dados_personagens.csv")
    nomes_atributos = atributos_csv.columns[1:-1]

    # Recalcula atributos
    atributos = {**modelo_em_criacao["atributos_personagem1"], **modelo_em_criacao["atributos_personagem2"]}
    contagens, total = contar_por_distancia_com_area_util(caminho_imagem, atributos, tolerancia=25)
    entrada = []
    for nome in nomes_atributos:
        proporcao = contagens[nome] / total if total else 0
        entrada.append(round(proporcao * 10, 4))
    entrada = np.array(entrada).reshape(1, -1)

    # Faz a predição
    resultado = modelo.predict(entrada)[0][0]
    classes = atributos_csv["classe"].unique()
    if len(classes) >= 2:
        personagem_predito = classes[0] if resultado >= 0.5 else classes[1]
    else:
        personagem_predito = "Desconhecido"

    #print("Predição: ", personagem_predito)


    # Volta à tela principal para mostrar os dados
    limpar_tela()

    tk.Label(frame_principal, text="Resultado da Predição", font=("Arial", 16)).pack(pady=10)

    # Exibe imagem carregada
    imagem_pil = Image.open(caminho_imagem)
    imagem_pil.thumbnail((300, 300))
    imagem_tk = ImageTk.PhotoImage(imagem_pil)

    canvas = tk.Canvas(frame_principal, width=imagem_pil.width, height=imagem_pil.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=imagem_tk)
    canvas.image = imagem_tk  # necessário para manter a imagem visível

    # Exibe o resultado
    tk.Label(frame_principal, text="Predição:", font=("Arial", 14)).pack(pady=10)
    tk.Label(frame_principal, text=f"{personagem_predito}", font=("Arial", 14, "bold")).pack(pady=5)
    tk.Label(frame_principal, text=f"Probabilidade: {resultado:.4f}", font=("Arial", 12)).pack(pady=5)


    botoes = tk.Frame(frame_principal)
    botoes.pack(pady=20)

    tk.Button(botoes, text="🏠 Voltar ao início", command=mostrar_tela_inicial).pack(side="left", padx=10)


def mostrar_tela_testar_modelo():
    limpar_tela()
    tk.Label(frame_principal, text="Testar Modelo", font=("Arial", 16)).pack(pady=10)

    from os import listdir
    from os.path import isfile, join

    # busca modelos .keras na pasta atual
    modelos_disponiveis = [f for f in listdir() if f.endswith(".keras")]

    if not modelos_disponiveis:
        tk.Label(frame_principal, text="Nenhum modelo .keras encontrado.").pack(pady=10)
        return

    tk.Label(frame_principal, text="Selecione um modelo:").pack()
    var_modelo = tk.StringVar()
    var_modelo.set(modelos_disponiveis[0])

    drop = tk.OptionMenu(frame_principal, var_modelo, *modelos_disponiveis)
    drop.pack(pady=10)

    def carregar_e_testar():
        nome_modelo = var_modelo.get()
        testar_modelo(nome_modelo)

    tk.Button(frame_principal, text="Selecionar imagem para testar", command=carregar_e_testar).pack(pady=20)
    tk.Button(frame_principal, text="Voltar", command=mostrar_tela_inicial).pack(pady=10)


def iniciar_fluxo_cnn():
    limpar_tela()
    tk.Label(frame_principal, text="CNN - Nome do Modelo", font=("Arial", 14)).pack(pady=10)
    nome_entry = tk.Entry(frame_principal, width=30)
    nome_entry.pack(pady=5)

    def salvar_nome():
        modelo_em_criacao["nome"] = nome_entry.get().strip()
        modelo_em_criacao["tipo_modelo"] = "cnn"
        mostrar_nomes_personagens()

    tk.Button(frame_principal, text="Avançar", command=salvar_nome).pack(pady=10)

def treinar_modelo_cnn():
    import tensorflow as tf
    import os
    import shutil
    from PIL import Image
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    nome_modelo = modelo_em_criacao["nome"]
    personagem1 = modelo_em_criacao["personagem1"]
    personagem2 = modelo_em_criacao["personagem2"]

    # Cria estrutura de diretórios temporários para treinamento
    pasta_base = f"dataset_{nome_modelo}"
    pasta_treino = os.path.join(pasta_base, "train")
    shutil.rmtree(pasta_base, ignore_errors=True)

    os.makedirs(os.path.join(pasta_treino, personagem1), exist_ok=True)
    os.makedirs(os.path.join(pasta_treino, personagem2), exist_ok=True)

    # Copia imagens para as pastas certas
    for img_path in modelo_em_criacao["imagens_personagem1"]:
        shutil.copy(img_path, os.path.join(pasta_treino, personagem1, os.path.basename(img_path)))
    for img_path in modelo_em_criacao["imagens_personagem2"]:
        shutil.copy(img_path, os.path.join(pasta_treino, personagem2, os.path.basename(img_path)))

    # Gera dados de imagem com data augmentation e validação
    datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.1,
        rotation_range=20,
        zoom_range=0.2,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2]
    )

    treino_gen = datagen.flow_from_directory(
        pasta_treino,
        target_size=(64, 64),
        batch_size=8,
        class_mode='binary',
        subset='training'
    )

    valid_gen = datagen.flow_from_directory(
        pasta_treino,
        target_size=(64, 64),
        batch_size=8,
        class_mode='binary',
        subset='validation'
    )


    # Salva o mapeamento real das classes
    indice_para_classe = {v: k for k, v in treino_gen.class_indices.items()}


    valid_gen = datagen.flow_from_directory(
        pasta_treino,
        target_size=(64, 64),
        batch_size=8,
        class_mode='binary',
        subset='validation'
    )

    # Modelo CNN
    from tensorflow.keras.callbacks import EarlyStopping

    # Early stopping para evitar overfitting
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )

# Novo modelo mais profundo e robusto
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.BatchNormalization(),

        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.BatchNormalization(),

        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.BatchNormalization(),

        tf.keras.layers.Flatten(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Treinamento com early stopping
    model.fit(
        treino_gen,
        validation_data=valid_gen,
        epochs=50
    )


    # Salva modelo e JSON
    nome_arquivo = f"{nome_modelo}_cnn"
    model.save(f"{nome_arquivo}.keras")

    import json
    with open(f"{nome_arquivo}.json", "w") as f:
        json.dump({
        "personagem1": personagem1,
        "personagem2": personagem2,
        "classe_0": indice_para_classe[0],
        "classe_1": indice_para_classe[1]
    }, f)


    print("Modelo CNN treinado e salvo com sucesso!")

    # Volta ao menu
    janela.after(100, mostrar_tela_inicial)

def mostrar_tela_testar_modelo_cnn():
    limpar_tela()
    tk.Label(frame_principal, text="Testar Modelo CNN", font=("Arial", 16)).pack(pady=10)

    from os import listdir
    from os.path import isfile, join

    modelos_disponiveis = [f for f in listdir() if f.endswith("_cnn.keras")]

    if not modelos_disponiveis:
        tk.Label(frame_principal, text="Nenhum modelo CNN encontrado.").pack(pady=10)
        return

    tk.Label(frame_principal, text="Selecione um modelo:").pack()
    var_modelo = tk.StringVar()
    var_modelo.set(modelos_disponiveis[0])

    drop = tk.OptionMenu(frame_principal, var_modelo, *modelos_disponiveis)
    drop.pack(pady=10)

    def carregar_e_testar():
        nome_modelo = var_modelo.get()
        testar_modelo_cnn(nome_modelo)

    tk.Button(frame_principal, text="Selecionar imagem para testar", command=carregar_e_testar).pack(pady=20)
    tk.Button(frame_principal, text="Voltar", command=mostrar_tela_inicial).pack(pady=10)

def testar_modelo_cnn(nome_arquivo_modelo):
    import tensorflow as tf
    from tkinter import filedialog
    from PIL import Image, ImageTk
    import numpy as np
    import json
    import os

    caminho_imagem = filedialog.askopenfilename(title="Escolha uma imagem para testar")
    if not caminho_imagem:
        return

    # Carrega o modelo
    modelo = tf.keras.models.load_model(nome_arquivo_modelo)

    # Lê o JSON com nomes dos personagens
    json_path = os.path.splitext(nome_arquivo_modelo)[0] + ".json"
    with open(json_path, "r") as f:
        dados = json.load(f)
    personagem1 = dados["personagem1"]
    personagem2 = dados["personagem2"]

    # Prepara a imagem
    imagem = Image.open(caminho_imagem).convert("RGB")
    imagem = imagem.resize((64, 64))
    imagem_array = np.array(imagem) / 255.0
    imagem_array = imagem_array.reshape((1, 64, 64, 3))

    resultado = modelo.predict(imagem_array)[0][0]
    classe_0 = dados["classe_0"]
    classe_1 = dados["classe_1"]
    predicao = classe_1 if resultado >= 0.5 else classe_0


    # Mostra na interface
    limpar_tela()
    tk.Label(frame_principal, text="Resultado da Predição", font=("Arial", 16)).pack(pady=10)

    imagem_tk = ImageTk.PhotoImage(imagem.resize((300, 300)))
    canvas = tk.Canvas(frame_principal, width=300, height=300)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=imagem_tk)
    canvas.image = imagem_tk

    tk.Label(frame_principal, text=f"Predição: {predicao}", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(frame_principal, text=f"Probabilidade: {resultado:.4f}", font=("Arial", 12)).pack(pady=5)

    botoes = tk.Frame(frame_principal)
    botoes.pack(pady=20)

    tk.Button(botoes, text="🏠 Voltar ao início", command=mostrar_tela_inicial).pack(side="left", padx=10)


# Inicializa a tela inicial
mostrar_tela_inicial()
janela.mainloop()

