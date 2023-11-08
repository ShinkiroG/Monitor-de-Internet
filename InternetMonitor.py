import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import time
import socket
import os
import sys
import subprocess
import json
import pystray
from PIL import Image
import webbrowser


# Caminho para o arquivo de configuração
config_file = "config.json"

# Obtenha o diretório do executável em execução
diretorio_do_executavel = os.path.dirname(sys.executable)

# Construindo um caminho C://.../img
caminho_img1 = os.path.join(diretorio_do_executavel, "img", "img1.png")
caminho_img2 = os.path.join(diretorio_do_executavel, "img", "img2.png")
caminho_icone_tray = os.path.join(diretorio_do_executavel, "img", "icone.png")
caminho_ico = os.path.join(diretorio_do_executavel, "img", "icone.ico")

# Função para sair
def on_exit(icon, item):
    icon.stop()
    root.deiconify()
    root.destroy()

# Função TEMPORÁRIA pra fechar o app
def on_exit_2():
    root.deiconify()
    root.destroy()

# Função para minimizar a janela
def on_minimize(icon, item):
    root.iconify()

# Essa função ia ser usada ao usuário clicar no X pra fechar o app
# Pra fechar o app de verdade ele precisaria fechar na bandeja.
def minimize_to_system_tray():
    root.iconify()  # Minimize a janela ao ícone da bandeja do sistema
    root.withdraw()

# Função para restaurar a janela se estiver minimizada
def on_open(icon, item):
    root.deiconify()
    icon.stop()

def create_tray_icon():
    menu = (
        pystray.MenuItem('Abrir', on_open),
        pystray.MenuItem('Fechar', on_exit)
    )

    image = caminho_icone_tray
    icon = pystray.Icon("InternetMonitor", image, "Meu App", menu)
    return icon

# Função para carregar as configurações salvas
def carregar_configuracoes():
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            config = json.load(file)
            return config
    return {}

# Função para salvar as configurações
def salvar_configuracoes(config):
    with open(config_file, "w") as file:
        json.dump(config, file)

log_file = "registro_conexao.txt"
diretorio_logs = ""
janela_altura_padrao = 700
conexao_online = True

# Função para verificar a conexão com a Internet
def verificar_conexao_internet():
    try:
        socket.create_connection(("www.google.com", 80), timeout=2)
        return True
    except OSError:
        pass
    return False

# Função para criar o arquivo de log se ele não existir
def criar_arquivo_log():
    if not os.path.exists(os.path.join(diretorio_logs, log_file)):
        with open(os.path.join(diretorio_logs, log_file), "w") as file:
            file.write("Arquivo de registro de conexão\n")

# Função para atualizar o status da conexão
def atualizar_status():
    global conexao_online

    if verificar_conexao_internet():
        if not conexao_online:
            status_label.config(text="Status: Online", foreground="green")
            registrar_log("Conexão Restaurada")
        conexao_online = True
    else:
        if conexao_online:
            status_label.config(text="Status: Offline", foreground="red")
            registrar_log("Conexão Caiu")
        conexao_online = False

    root.after(100, atualizar_status)

# Função para registrar no log
def registrar_log(mensagem):
    criar_arquivo_log()
    with open(os.path.join(diretorio_logs, log_file), "a") as file:
        timestamp = time.strftime("%I:%M%p - %d/%m/%Y")
        file.write(f"{timestamp} - {mensagem}\n")

# Função para atualizar a janela de registro recente
def atualizar_registro_recente():
    exibir_ultimas_linhas_registro()
    root.after(100, atualizar_registro_recente)

# Função para exibir as 3 últimas linhas do arquivo de registro
def exibir_ultimas_linhas_registro():
    try:
        with open(os.path.join(diretorio_logs, log_file), "r") as file:
            linhas = file.read().splitlines()[-3:]
            log_text.config(state=tk.NORMAL)
            log_text.delete(1.0, tk.END)
            for linha in linhas:
                log_text.insert(tk.END, linha + "\n")
            log_text.config(state=tk.DISABLED)
    except FileNotFoundError:
        log_text.config(state=tk.NORMAL)
        log_text.delete(1.0, tk.END)
        log_text.config(state=tk.DISABLED)

# Função para selecionar um diretório para salvar os logs
def selecionar_diretorio_logs():
    global diretorio_logs
    novo_diretorio = filedialog.askdirectory()
    if novo_diretorio:
        diretorio_logs = novo_diretorio
        diretorio_valor_label.config(text=diretorio_logs)

        # Salve o novo diretório nas configurações
        config["ultimo_diretorio"] = diretorio_logs
        salvar_configuracoes(config)

# Função para abrir a pasta de logs no explorador de arquivos
def abrir_pasta_logs():
    os.startfile(diretorio_logs)

# Função para abrir o link no navegador padrão
def abrir_link():
    url = "https://ko-fi.com/shinkirodev"
    webbrowser.open(url)

def abrir_nd_link():
    # Substitua o URL abaixo pelo link que deseja abrir
    link = "https://www.youtube.com/@ShinkiroDev"
    subprocess.Popen(["start", link], shell=True)

# Inicializar a janela do Tkinter
root = tk.Tk()
root.title("Monitor de Internet - By ShinkiroDev")

root.iconbitmap(caminho_ico)

# Carregue as configurações
config = carregar_configuracoes()
diretorio_logs = config.get("ultimo_diretorio", "")  # Use o último diretório salvo, se existir

# Centralizar todo o conteúdo na janela
largura_janela = 500
janela_altura = janela_altura_padrao
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
x = (largura_tela - largura_janela) // 2
y = (altura_tela - janela_altura) // 2
root.geometry(f"{largura_janela}x{janela_altura}+{x}+{y}")

frame = ttk.Frame(root)
frame.pack(expand=True, fill="both")

status_label = ttk.Label(frame, text="Status: Online", foreground="green", font=("Helvetica", 16))
status_label.pack(pady=10)

monitorando_label = ttk.Label(frame, text="Monitorando Conexão.", font=("Helvetica", 12))
monitorando_label.pack()

proxima_verificacao_label = ttk.Label(frame, text="")
proxima_verificacao_label.pack(pady=10)

registro_recente_label = ttk.Label(frame, text="Registro recente:")
registro_recente_label.pack(pady=10)

log_text = scrolledtext.ScrolledText(frame, width=50, height=6, state=tk.DISABLED)
log_text.pack(pady=5)

diretorio_label = ttk.Label(frame, text="Diretório dos logs:")
diretorio_label.pack(pady=5)

diretorio_valor_label = ttk.Label(frame, text=diretorio_logs)
diretorio_valor_label.pack(pady=5)

mudar_diretorio_button = ttk.Button(frame, text="Mudar diretório dos logs", command=selecionar_diretorio_logs)
mudar_diretorio_button.pack(pady=5)

ver_logs_button = ttk.Button(frame, text="Ver logs", command=abrir_pasta_logs)
ver_logs_button.pack(pady=5)

rodape_frame = ttk.Frame(root)
rodape_frame.pack(expand=True, fill="both")

rodape_texto = ("Esse aplicativo apenas registra localmente em um arquivo de texto quando sua internet cai,"
                " pois ele tenta acessar o Google ou acessar a interface de rede. Em outras palavras,"
                " esse app não envia seus dados para ninguém.")
rodape_label = ttk.Label(rodape_frame, text=rodape_texto, wraplength=400, justify="center")
rodape_label.pack(pady=10)

frame = ttk.Frame(root)
frame.pack()

button_frame = ttk.Frame(frame)
button_frame.grid(row=0, column=0, padx=10)

img1 = tk.PhotoImage(file=caminho_img1)
img2 = tk.PhotoImage(file=caminho_img2)

img1_button = ttk.Button(button_frame, image=img1, command=abrir_link)
img1_button.grid(row=0, column=0, padx=0, pady=25)

img2_button = ttk.Button(button_frame, image=img2, command=abrir_nd_link)
img2_button.grid(row=0, column=1, padx=10, pady=25)



# Função para atualizar o texto "Monitorando Conexão" com animação
def atualizar_monitorando_texto():
    texto = monitorando_label.cget("text")
    if texto == "Monitorando Conexão.":
        monitorando_label.config(text="Monitorando Conexão..")
    elif texto == "Monitorando Conexão..":
        monitorando_label.config(text="Monitorando Conexão...")
    elif texto == "Monitorando Conexão...":
        monitorando_label.config(text="Monitorando Conexão.")
    root.after(1000, atualizar_monitorando_texto)


# Iniciar a primeira verificação
atualizar_status()
atualizar_monitorando_texto()
atualizar_registro_recente()


# Criar um ícone na bandeja do sistema
# Por enquanto sem uso, necessário fazer o app rodar em 2nd plano adequadamente e então voltar nesse item
def criar_icone_bandeja():
    minimize_to_system_tray()
    menu = (
        pystray.MenuItem('Abrir', on_open),
        pystray.MenuItem('Fechar', on_exit)
    )

    image = Image.open(caminho_icone_tray)  # Substitua "icone.png" pelo caminho da imagem do ícone.

    icon = pystray.Icon("InternetMonitor", image, "Internet Monitor By ShinkiroDev", menu)
    icon.run()


# Configurar o evento para minimizar a janela para a bandeja quando o botão de minimizar padrão for clicado
root.protocol("WM_DELETE_WINDOW", on_exit_2)

# Função para abrir o aplicativo
def abrir_aplicativo():
    root.deiconify()  # Restaurar a janela



# Iniciar a janela principal do aplicativo
root.mainloop()