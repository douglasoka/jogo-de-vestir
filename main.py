import tkinter as tk
from tkinter import Canvas, filedialog, messagebox
from PIL import Image, ImageTk

# Configura a janela principal
root = tk.Tk()
root.title("Jogo de Vestir")
root.geometry("1000x800")  # Diminuindo o tamanho da janela

# Variáveis globais
print_slots = []
boneco_img = None
selected_item = None
drag_data = {"x": 0, "y": 0, "item": None}
roupas = {}  # Dicionário para armazenar as roupas carregadas
roupas_posicoes_iniciais = {}  # Dicionário para armazenar as posições iniciais das roupas

# Função para iniciar o drag
def start_drag(event):
    global selected_item
    item = canvas.find_closest(event.x, event.y)[0]
    if item in roupas.values():
        selected_item = item
        drag_data["item"] = item
        drag_data["x"] = event.x
        drag_data["y"] = event.y

# Função para mover o item arrastado
def do_drag(event):
    if selected_item:
        dx = event.x - drag_data["x"]
        dy = event.y - drag_data["y"]
        canvas.move(drag_data["item"], dx, dy)
        drag_data["x"] = event.x
        drag_data["y"] = event.y

# Função para soltar o item
def stop_drag(event):
    global selected_item
    selected_item = None

# Função para carregar as imagens de roupas
def carregar_roupas():
    global roupas, roupas_posicoes_iniciais
    # Carregar camisetas
    roupa1_img = ImageTk.PhotoImage(Image.open("camiseta1.png").resize((250, 250)))  # Diminuindo o tamanho das roupas
    roupa2_img = ImageTk.PhotoImage(Image.open("camiseta2.png").resize((250, 250)))
    # Carregar shorts
    short1_img = ImageTk.PhotoImage(Image.open("short1.png").resize((250, 250)))
    short2_img = ImageTk.PhotoImage(Image.open("short2.png").resize((250, 250)))
    
    # Adicionar ao canvas (à esquerda do boneco)
    roupas["camiseta1"] = canvas.create_image(-50, -50, image=roupa1_img, anchor=tk.NW)
    roupas["camiseta2"] = canvas.create_image(80, -50, image=roupa2_img, anchor=tk.NW)
    roupas["short1"] = canvas.create_image(210, -80, image=short1_img, anchor=tk.NW)
    roupas["short2"] = canvas.create_image(340, -80, image=short2_img, anchor=tk.NW)

    # Salvar a referência das imagens
    canvas.roupa1_img = roupa1_img
    canvas.roupa2_img = roupa2_img
    canvas.short1_img = short1_img
    canvas.short2_img = short2_img

    # Salvar as posições iniciais das roupas
    roupas_posicoes_iniciais = {
        "camiseta1": (-50, -50),
        "camiseta2": (80, -50),
        "short1": (210, -80),
        "short2": (340, -80)
    }

# Função para carregar o boneco
def carregar_boneco():
    global boneco_img
    boneco_img = ImageTk.PhotoImage(Image.open("boneco.png").resize((250, 250)))  # Diminuindo o tamanho do boneco
    canvas.create_image(150, 150, image=boneco_img, anchor=tk.NW)
    canvas.boneco_img = boneco_img  # Manter referência para não ser coletado

# Função para tirar um print do boneco com as roupas aplicadas
def tirar_print():
    global print_slots
    if len(print_slots) < 6:
        # Salvar uma captura do canvas apenas da área central
        x0, y0, x1, y1 = 180, 130, 375, 450  # Coordenadas ajustadas da área central
        canvas.postscript(file="boneco_com_roupa.eps", colormode='color', x=x0, y=y0, width=x1-x0, height=y1-y0)
        img = Image.open("boneco_com_roupa.eps")
        img.save(f"print_{len(print_slots)+1}.png")

        # Exibir o print no slot abaixo
        img_resized = img.resize((200, 200), Image.Resampling.LANCZOS)  # Ajustando o tamanho do print
        img_tk = ImageTk.PhotoImage(img_resized)
        label = tk.Label(print_frame, image=img_tk)
        label.image = img_tk  # Necessário para manter a referência
        label.pack(side="left", padx=5)
        print_slots.append(label)
    else:
        messagebox.showinfo("Limite de prints", "Você atingiu o limite de 6 prints.")

# Função para limpar as roupas e retornar ao local inicial
def limpar_roupas():
    for roupa, posicao in roupas_posicoes_iniciais.items():
        canvas.coords(roupas[roupa], posicao)

# Função para resetar o jogo, limpando os prints existentes
def resetar_jogo():
    global print_slots
    for label in print_slots:
        label.destroy()
    print_slots = []
    limpar_roupas()

# Criação da área de desenho (Canvas)
canvas = Canvas(root, width=500, height=500, bg="white")  # Diminuindo o tamanho do canvas
canvas.pack(side=tk.TOP, pady=0)

# Carregar boneco e roupas
carregar_boneco()
carregar_roupas()

# Vincular eventos de arrastar e soltar
canvas.bind("<Button-1>", start_drag)
canvas.bind("<B1-Motion>", do_drag)
canvas.bind("<ButtonRelease-1>", stop_drag)

# Botão de salvar o boneco com as roupas
btn_save = tk.Button(root, text="Salvar", command=tirar_print)
btn_save.pack(side=tk.LEFT, pady=10, padx=10)

# Botão de limpar as roupas
btn_clear = tk.Button(root, text="Limpar", command=limpar_roupas)
btn_clear.pack(side=tk.LEFT, pady=10, padx=10)


# Botão de resetar o jogo
btn_reset = tk.Button(root, text="Resetar", command=resetar_jogo)
btn_reset.pack(side=tk.RIGHT, pady=10, padx=10)

# Frame para armazenar os prints
print_frame = tk.Frame(root)
print_frame.pack(pady=10)

# Inicia o loop da interface gráfica
root.mainloop()
