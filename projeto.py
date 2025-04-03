import tkinter as tk

def abrir_tela(titulo):
    nova_janela = tk.Toplevel(root)
    nova_janela.title(titulo)
    nova_janela.geometry("300x200")

    label = tk.Label(nova_janela, text=f"Você está na tela: {titulo}", font=("Arial", 14))
    label.pack(expand=True)

# Janela principal
root = tk.Tk()
root.title("Menu Principal")
root.geometry("300x300")

btn1 = tk.Button(root, text="Criar modelo", command=lambda: abrir_tela("Criar modelo"), width=20, height=2)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Botão 2", command=lambda: abrir_tela("Botão 2"), width=20, height=2)
btn2.pack(pady=10)

btn3 = tk.Button(root, text="Botão 3", command=lambda: abrir_tela("Botão 3"), width=20, height=2)
btn3.pack(pady=10)

btn4 = tk.Button(root, text="Botão 4", command=lambda: abrir_tela("Botão 4"), width=20, height=2)
btn4.pack(pady=10)

root.mainloop()
