import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping
import shutil
import json

# ---------- VARIÁVEIS GLOBAIS ----------
modelo_em_criacao = {
    "nome": "",
    "personagem1": "",
    "personagem2": "",
    "imagens_personagem1": [],
    "imagens_personagem2": [],
    "atributos_personagem1": {},
    "atributos_personagem2": {}
}

estado = {
    "qtd_atributos": 0,
    "indice_atual": 0,
    "nomes_atributos": [],
    "qtd_atributos_p2": 0,
    "indice_atual_p2": 0,
    "nomes_atributos_p2": []
}

# ---------- FUNÇÕES DE INTERFACE E LÓGICA ----------

import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import csv
import os

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

modelo_em_criacao = {
    "nome": "",
    "personagem1": "",
    "personagem2": "",
    "imagens_personagem1": [],
    "imagens_personagem2": [],
    "atributos_personagem1": {},
    "atributos_personagem2": {}
}

estado = {
    "qtd_atributos": 0,
    "indice_atual": 0,
    "nomes_atributos": [],
    "qtd_atributos_p2": 0,
    "indice_atual_p2": 0,
    "nomes_atributos_p2": []
}

def limpar_tela(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def mostrar_tela_inicial(janela, frame_principal):
    limpar_tela(frame_principal)
    ctk.CTkLabel(frame_principal, text="Menu Principal", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=30)
    ctk.CTkButton(frame_principal, text="Criar modelo baseado em RGB", command=lambda: mostrar_tela_criar_modelo(janela, frame_principal)).pack(pady=10)
    ctk.CTkButton(frame_principal, text="Criar modelo CNN", command=lambda: iniciar_fluxo_cnn(janela, frame_principal)).pack(pady=10)
    ctk.CTkButton(frame_principal, text="Testar modelo", command=lambda: mostrar_tela_testar_modelo_unificado(janela, frame_principal)).pack(pady=10)

def mostrar_tela_criar_modelo(janela, frame):
    limpar_tela(frame)
    ctk.CTkLabel(frame, text="Etapa 1: Nome do Modelo", font=ctk.CTkFont(size=16)).pack(pady=10)
    nome_entry = ctk.CTkEntry(frame, width=300)
    nome_entry.pack(pady=5)
    def salvar_nome():
        modelo_em_criacao["nome"] = nome_entry.get().strip()
        mostrar_nomes_personagens(janela, frame)
    ctk.CTkButton(frame, text="Avançar", command=salvar_nome).pack(pady=10)

def mostrar_nomes_personagens(janela, frame):
    limpar_tela(frame)
    ctk.CTkLabel(frame, text="Nome dos Personagens", font=ctk.CTkFont(size=16)).pack(pady=10)
    ctk.CTkLabel(frame, text="Nome do Personagem 1").pack()
    p1_entry = ctk.CTkEntry(frame)
    p1_entry.pack(pady=5)
    ctk.CTkLabel(frame, text="Nome do Personagem 2").pack()
    p2_entry = ctk.CTkEntry(frame)
    p2_entry.pack(pady=5)
    def avancar():
        modelo_em_criacao["personagem1"] = p1_entry.get().strip()
        modelo_em_criacao["personagem2"] = p2_entry.get().strip()
        mostrar_upload_personagem1(janela, frame)
    ctk.CTkButton(frame, text="Avançar", command=avancar).pack(pady=10)

def mostrar_upload_personagem1(janela, frame):
    limpar_tela(frame)
    ctk.CTkLabel(frame, text="Etapa 2: Upload Imagens do Personagem 1", font=ctk.CTkFont(size=16)).pack(pady=10)
    def selecionar_arquivos():
        arquivos = filedialog.askopenfilenames(title="Imagens personagem 1")
        modelo_em_criacao["imagens_personagem1"] = list(arquivos)
        mostrar_upload_personagem2(janela, frame)
    ctk.CTkButton(frame, text="Selecionar imagens", command=selecionar_arquivos).pack(pady=20)

def mostrar_upload_personagem2(janela, frame):
    limpar_tela(frame)
    ctk.CTkLabel(frame, text="Etapa 3: Upload Imagens do Personagem 2", font=ctk.CTkFont(size=16)).pack(pady=10)
    def selecionar_arquivos():
        arquivos = filedialog.askopenfilenames(title="Imagens personagem 2")
        modelo_em_criacao["imagens_personagem2"] = list(arquivos)
        treinar_modelo_cnn(janela, frame)
    ctk.CTkButton(frame, text="Selecionar imagens", command=selecionar_arquivos).pack(pady=20)

def mostrar_etapa_qtd_atributos(janela, frame, personagem):
    limpar_tela(frame)
    ctk.CTkLabel(frame, text=f"Personagem {personagem}: Quantos atributos deseja definir?", font=ctk.CTkFont(size=16)).pack(pady=10)
    qtd_entry = ctk.CTkEntry(frame)
    qtd_entry.pack()
    def avancar():
        try:
            qtd = int(qtd_entry.get())
            if personagem == 1:
                estado["qtd_atributos"] = qtd
                estado["indice_atual"] = 0
                estado["nomes_atributos"] = []
            else:
                estado["qtd_atributos_p2"] = qtd
                estado["indice_atual_p2"] = 0
                estado["nomes_atributos_p2"] = []
            mostrar_etapa_nome_atributo(janela, frame, personagem)
        except ValueError:
            print("Digite um número válido")
    ctk.CTkButton(frame, text="Avançar", command=avancar).pack(pady=10)

def mostrar_etapa_nome_atributo(janela, frame, personagem):
    limpar_tela(frame)
    i = (estado["indice_atual"] if personagem == 1 else estado["indice_atual_p2"]) + 1
    ctk.CTkLabel(frame, text=f"Personagem {personagem} – Nome do Atributo {i}", font=ctk.CTkFont(size=16)).pack(pady=10)
    nome_entry = ctk.CTkEntry(frame)
    nome_entry.pack()
    def avancar():
        nome = nome_entry.get().strip()
        if nome:
            if personagem == 1:
                estado["nomes_atributos"].append(nome)
            else:
                estado["nomes_atributos_p2"].append(nome)
            mostrar_conta_gotas(janela, frame, nome, personagem)
    ctk.CTkButton(frame, text="Avançar", command=avancar).pack(pady=10)

def mostrar_conta_gotas(janela, frame, nome_atributo, personagem):
    limpar_tela(frame)
    ctk.CTkLabel(frame, text=f"Selecione uma cor para: {nome_atributo} (Personagem {personagem})", font=ctk.CTkFont(size=16)).pack(pady=10)
    caminho_imagem = modelo_em_criacao[f"imagens_personagem{personagem}"][0]
    imagem_pil = Image.open(caminho_imagem)
    imagem_pil.thumbnail((400, 400))
    imagem_tk = ImageTk.PhotoImage(imagem_pil)
    canvas = ctk.CTkCanvas(frame, width=imagem_pil.width, height=imagem_pil.height)
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=imagem_tk)
    canvas.image = imagem_tk
    pixels = imagem_pil.load()
    def clique(event):
        x, y = event.x, event.y
        r, g, b = pixels[x, y][:3]
        modelo_em_criacao[f"atributos_personagem{personagem}"][nome_atributo] = {"referencia": (r, g, b)}
        if personagem == 1:
            estado["indice_atual"] += 1
            if estado["indice_atual"] < estado["qtd_atributos"]:
                mostrar_etapa_nome_atributo(janela, frame, personagem)
        else:
            estado["indice_atual_p2"] += 1
            if estado["indice_atual_p2"] < estado["qtd_atributos_p2"]:
                mostrar_etapa_nome_atributo(janela, frame, personagem)
            else:
                gerar_csv_e_treinar(janela, frame)
    canvas.bind("<Button-1>", clique)

def cor_esta_na_faixa(pixel_rgb, cor_referencia, tolerancia=25):
    r1, g1, b1 = pixel_rgb
    r2, g2, b2 = cor_referencia
    dist = ((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2) ** 0.5
    return dist <= tolerancia

def contar_pixels(imagem_path, atributos, tolerancia=25):
    imagem = Image.open(imagem_path).convert("RGB")
    pixels = imagem.load()
    largura, altura = imagem.size
    contagens = {nome: 0 for nome in atributos}
    total = 0
    for x in range(largura):
        for y in range(altura):
            r, g, b = pixels[x, y]
            for nome, dado in atributos.items():
                if cor_esta_na_faixa((r, g, b), dado["referencia"], tolerancia):
                    contagens[nome] += 1
                    total += 1
    return contagens, total

def gerar_csv_e_treinar(janela, frame):
    limpar_tela(frame)
    imagens = modelo_em_criacao["imagens_personagem1"] + modelo_em_criacao["imagens_personagem2"]
    atributos = {**modelo_em_criacao["atributos_personagem1"], **modelo_em_criacao["atributos_personagem2"]}
    colunas = ["imagem"] + list(atributos.keys()) + ["classe"]
    linhas = []
    for img in imagens:
        contagens, total = contar_pixels(img, atributos)
        linha = [os.path.basename(img)]
        for nome in atributos:
            proporcao = contagens[nome] / total if total else 0
            linha.append(round(proporcao * 10, 4))
        linha.append(modelo_em_criacao["personagem1"] if img in modelo_em_criacao["imagens_personagem1"] else modelo_em_criacao["personagem2"])
        linhas.append(linha)
    with open("dados_personagens.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(colunas)
        writer.writerows(linhas)
    treinar_modelo(janela, frame)

def treinar_modelo(janela, frame):
    df = pd.read_csv("dados_personagens.csv")
    X = df.iloc[:, 1:-1].values
    y = (df.iloc[:, -1].values == modelo_em_criacao["personagem1"])
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=(X.shape[1],)),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X, y, epochs=300, validation_split=0.2, verbose=0)
    nome_base = modelo_em_criacao["nome"]
    model.save(f"{nome_base}.keras")
    dados = {
        "personagem1": modelo_em_criacao["personagem1"],
        "personagem2": modelo_em_criacao["personagem2"],
        "atributos_personagem1": modelo_em_criacao["atributos_personagem1"],
        "atributos_personagem2": modelo_em_criacao["atributos_personagem2"]
    }
    with open(f"{nome_base}.json", "w") as f_json:
        json.dump(dados, f_json)
    mostrar_tela_inicial(janela, frame)
def mostrar_tela_testar_modelo(janela, frame):
    from tkinter import filedialog
    import json

    limpar_tela(frame)
    ctk.CTkLabel(frame, text="Testar Modelo", font=ctk.CTkFont(size=18)).pack(pady=10)

    modelo_path = filedialog.askopenfilename(title="Selecione o modelo .keras")
    if not modelo_path:
        return

    try:
        model = tf.keras.models.load_model(modelo_path)
        json_path = os.path.splitext(modelo_path)[0] + ".json"
        with open(json_path, "r") as f:
            dados = json.load(f)

        modelo_em_criacao["personagem1"] = dados["personagem1"]
        modelo_em_criacao["personagem2"] = dados["personagem2"]
        modelo_em_criacao["atributos_personagem1"] = dados["atributos_personagem1"]
        modelo_em_criacao["atributos_personagem2"] = dados["atributos_personagem2"]

    except Exception as e:
        ctk.CTkLabel(frame, text=f"Erro ao carregar modelo: {e}", text_color="red").pack(pady=10)
        return

    ctk.CTkLabel(frame, text="Modelo carregado com sucesso. Agora selecione a imagem.").pack(pady=10)

    def selecionar_imagem_e_testar():
        imagem_path = filedialog.askopenfilename(title="Selecione uma imagem para testar")
        if not imagem_path:
            return

        atributos_csv = pd.read_csv("dados_personagens.csv")
        nomes_atributos = atributos_csv.columns[1:-1]
        atributos = {**modelo_em_criacao["atributos_personagem1"], **modelo_em_criacao["atributos_personagem2"]}
        contagens, total = contar_pixels(imagem_path, atributos)

        entrada = []
        for nome in nomes_atributos:
            proporcao = contagens[nome] / total if total else 0
            entrada.append(round(proporcao * 10, 4))
        entrada = np.array(entrada).reshape(1, -1)

        resultado = model.predict(entrada)[0][0]
        personagem_predito = modelo_em_criacao["personagem1"] if resultado >= 0.5 else modelo_em_criacao["personagem2"]
        probabilidade = round(resultado * 100, 2)

        limpar_tela(frame)

        imagem_pil = Image.open(imagem_path)
        imagem_pil.thumbnail((300, 300))
        imagem_tk = ImageTk.PhotoImage(imagem_pil)
        canvas = ctk.CTkCanvas(frame, width=imagem_pil.width, height=imagem_pil.height)
        canvas.pack(pady=10)
        canvas.create_image(0, 0, anchor="nw", image=imagem_tk)
        canvas.image = imagem_tk

        ctk.CTkLabel(frame, text="Resultado da Predição", font=ctk.CTkFont(size=16)).pack(pady=10)
        ctk.CTkLabel(frame, text=f"Predição: {personagem_predito}", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        ctk.CTkLabel(frame, text=f"Probabilidade: {probabilidade:.2f}%", font=ctk.CTkFont(size=12)).pack(pady=5)

        ctk.CTkButton(frame, text="Voltar ao início", command=lambda: mostrar_tela_inicial(janela, frame)).pack(pady=20)

    ctk.CTkButton(frame, text="Selecionar imagem para testar", command=selecionar_imagem_e_testar).pack(pady=20)




def iniciar_fluxo_cnn(janela, frame):
    limpar_tela(frame)
    ctk.CTkLabel(frame, text="CNN - Nome do Modelo", font=ctk.CTkFont(size=16)).pack(pady=10)
    nome_entry = ctk.CTkEntry(frame, width=300)
    nome_entry.pack(pady=5)

    def salvar_nome():
        modelo_em_criacao["nome"] = nome_entry.get().strip()
        modelo_em_criacao["tipo_modelo"] = "cnn"
        mostrar_nomes_personagens(janela, frame)

    ctk.CTkButton(frame, text="Avançar", command=salvar_nome).pack(pady=10)


def treinar_modelo_cnn(janela, frame):
    nome_modelo = modelo_em_criacao["nome"]
    personagem1 = modelo_em_criacao["personagem1"]
    personagem2 = modelo_em_criacao["personagem2"]

    pasta_base = f"dataset_{nome_modelo}"
    pasta_treino = os.path.join(pasta_base, "train")
    shutil.rmtree(pasta_base, ignore_errors=True)

    os.makedirs(os.path.join(pasta_treino, personagem1), exist_ok=True)
    os.makedirs(os.path.join(pasta_treino, personagem2), exist_ok=True)

    for img_path in modelo_em_criacao["imagens_personagem1"]:
        shutil.copy(img_path, os.path.join(pasta_treino, personagem1, os.path.basename(img_path)))
    for img_path in modelo_em_criacao["imagens_personagem2"]:
        shutil.copy(img_path, os.path.join(pasta_treino, personagem2, os.path.basename(img_path)))

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

    indice_para_classe = {v: k for k, v in treino_gen.class_indices.items()}

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        MaxPooling2D(2, 2),
        BatchNormalization(),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        BatchNormalization(),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        BatchNormalization(),
        Flatten(),
        Dropout(0.5),
        Dense(128, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(treino_gen, validation_data=valid_gen, epochs=50)

    nome_arquivo = f"{nome_modelo}_cnn"
    model.save(f"{nome_arquivo}.keras")

    with open(f"{nome_arquivo}.json", "w") as f:
        json.dump({
            "personagem1": personagem1,
            "personagem2": personagem2,
            "classe_0": indice_para_classe[0],
            "classe_1": indice_para_classe[1]
        }, f)

    mostrar_tela_inicial(janela, frame)



def mostrar_nomes_personagens_cnn(janela, frame):
    limpar_tela(frame)
    ctk.CTkLabel(frame, text="CNN - Nome dos Personagens", font=ctk.CTkFont(size=16)).pack(pady=10)

    ctk.CTkLabel(frame, text="Personagem 1").pack()
    p1_entry = ctk.CTkEntry(frame)
    p1_entry.pack(pady=5)

    ctk.CTkLabel(frame, text="Personagem 2").pack()
    p2_entry = ctk.CTkEntry(frame)
    p2_entry.pack(pady=5)

    def avancar():
        modelo_em_criacao["personagem1"] = p1_entry.get().strip()
        modelo_em_criacao["personagem2"] = p2_entry.get().strip()
        mostrar_upload_imagens_cnn(janela, frame)

    ctk.CTkButton(frame, text="Avançar", command=avancar).pack(pady=10)

def mostrar_upload_imagens_cnn(janela, frame):
    limpar_tela(frame)
    ctk.CTkLabel(frame, text="CNN - Upload de Imagens", font=ctk.CTkFont(size=16)).pack(pady=10)

    def upload_p1():
        arquivos = filedialog.askopenfilenames(title="Imagens do Personagem 1")
        modelo_em_criacao["imagens_personagem1"] = list(arquivos)
        btn_p1.configure(text=f"{len(arquivos)} imagens selecionadas")

    def upload_p2():
        arquivos = filedialog.askopenfilenames(title="Imagens do Personagem 2")
        modelo_em_criacao["imagens_personagem2"] = list(arquivos)
        btn_p2.configure(text=f"{len(arquivos)} imagens selecionadas")

    btn_p1 = ctk.CTkButton(frame, text="Upload Personagem 1", command=upload_p1)
    btn_p1.pack(pady=10)

    btn_p2 = ctk.CTkButton(frame, text="Upload Personagem 2", command=upload_p2)
    btn_p2.pack(pady=10)

    ctk.CTkButton(frame, text="Treinar modelo CNN", command=lambda: treinar_modelo_cnn(janela, frame)).pack(pady=20)



def mostrar_tela_testar_modelo_unificado(janela, frame):
    limpar_tela(frame)
    ctk.CTkLabel(frame, text="Testar Modelo", font=ctk.CTkFont(size=18)).pack(pady=10)

    modelo_path = filedialog.askopenfilename(title="Selecione o modelo .keras")
    if not modelo_path:
        return

    json_path = os.path.splitext(modelo_path)[0] + ".json"
    if not os.path.exists(json_path):
        ctk.CTkLabel(frame, text="Arquivo .json não encontrado", text_color="red").pack(pady=10)
        return

    with open(json_path, "r") as f:
        dados = json.load(f)

    model = tf.keras.models.load_model(modelo_path)

    imagem_path = filedialog.askopenfilename(title="Selecione uma imagem para testar")
    if not imagem_path:
        return

    limpar_tela(frame)
    imagem_pil = Image.open(imagem_path)
    imagem_pil.thumbnail((300, 300))
    imagem_tk = ImageTk.PhotoImage(imagem_pil)
    canvas = ctk.CTkCanvas(frame, width=imagem_pil.width, height=imagem_pil.height)
    canvas.pack(pady=10)
    canvas.create_image(0, 0, anchor="nw", image=imagem_tk)
    canvas.image = imagem_tk

    if "classe_0" in dados and "classe_1" in dados:
        imagem = imagem_pil.resize((64, 64))
        imagem = np.array(imagem) / 255.0
        imagem = imagem.reshape((1, 64, 64, 3))
        resultado = model.predict(imagem)[0][0]
        personagem_predito = dados["classe_1"] if resultado >= 0.5 else dados["classe_0"]
    else:
        modelo_em_criacao["atributos_personagem1"] = dados["atributos_personagem1"]
        modelo_em_criacao["atributos_personagem2"] = dados["atributos_personagem2"]
        modelo_em_criacao["personagem1"] = dados["personagem1"]
        modelo_em_criacao["personagem2"] = dados["personagem2"]
        atributos = {**dados["atributos_personagem1"], **dados["atributos_personagem2"]}
        atributos_csv = pd.read_csv("dados_personagens.csv")
        nomes_atributos = atributos_csv.columns[1:-1]
        contagens, total = contar_pixels(imagem_path, atributos)
        entrada = [round(contagens[nome] / total * 10, 4) if total else 0 for nome in nomes_atributos]
        entrada = np.array(entrada).reshape(1, -1)
        resultado = model.predict(entrada)[0][0]
        personagem_predito = modelo_em_criacao["personagem1"] if resultado >= 0.5 else modelo_em_criacao["personagem2"]

    probabilidade = round(resultado * 100, 2)

    ctk.CTkLabel(frame, text="Resultado da Predição", font=ctk.CTkFont(size=16)).pack(pady=10)
    ctk.CTkLabel(frame, text=f"Predição: {personagem_predito}", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
    ctk.CTkLabel(frame, text=f"Probabilidade: {probabilidade:.2f}%", font=ctk.CTkFont(size=12)).pack(pady=5)
    ctk.CTkButton(frame, text="Voltar ao início", command=lambda: mostrar_tela_inicial(janela, frame)).pack(pady=20)


# ---------- EXECUÇÃO PRINCIPAL ----------
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    janela = ctk.CTk()
    janela.title("Criar Modelo")
    janela.geometry("800x600")

    frame_principal = ctk.CTkFrame(janela)
    frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

    mostrar_tela_inicial(janela, frame_principal)

    janela.mainloop()