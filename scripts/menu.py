import tkinter as tk
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tkinter import ttk
import sqlite3
from PIL import ImageTk, Image



conexao = sqlite3.connect('resultado.db')

conexao.execute('''CREATE TABLE IF NOT EXISTS resultados
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             origem TEXT NOT NULL,
             destino TEXT NOT NULL,
             resultado TEXT NOT NULL);''')




def executar_robo():
    # obter origem e destino dos campos de entrada
    origem = campo_origem.get()
    destino = campo_destino.get()

    # iniciar o navegador
    navegador = webdriver.Chrome()
    navegador.get("https://www.transvias.com.br")

    # preencher campo de origem
    origem_input = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.ID, "OrigemDescricao"))
    )
    origem_input.send_keys(origem)
    time.sleep(2)

    # preencher campo de destino
    destino_input = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.ID, "DestinoDescricao"))
    )
    destino_input.send_keys(destino)
    destino_input.send_keys(Keys.TAB)
    time.sleep(2)

    # pressionar enter para buscar
    ActionChains(navegador).send_keys(Keys.ENTER).perform()

    # esperar carregar a página de resultados
    SCROLL_PAUSE_TIME = 0.5
    # Get scroll height
    last_height = navegador.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = navegador.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(1)

    # obter e exibir resultados separados por vírgula
    email = []
    elements = navegador.find_elements("xpath","//span[@title='E-mail']/a")
    for element in elements:
        email.append(element.text)
    resultado = ', '.join(email)
    resultado_text.delete("1.0", tk.END)
    resultado_text.insert(tk.END, resultado)

    # salvar resultado no banco de dados
    with conexao:
        conexao.execute("INSERT INTO resultados (origem, destino, resultado) VALUES (?, ?, ?)", (origem, destino, resultado))

    conexao.commit()

    navegador.quit()


# função que abre a janela principal
def abrir_janela_principal(janela_menu):
        # criar o frame dentro da janela do menu
        frame_principal = tk.Toplevel(janela_menu)
        

        # adicionar estilo ao frame
        frame_principal.configure(bg="#F7F7F7", padx=20, pady=20)
        

        # adicionar campo de entrada para a origem
        aviso = tk.Label(frame_principal, text="Explorar \n Digite com todos acentos e nesse padrão: São Paulo-SP", font=("Arial", 14, "bold"), bg="#F7F7F7", fg="#333")
        aviso.pack()

        rotulo_origem = tk.Label(frame_principal, text="Origem:", font=("Arial", 14, "bold"), bg="#F7F7F7", fg="#333")
        rotulo_origem.pack(pady=(20, 5))

        campo_origem = tk.Entry(frame_principal, font=("Arial", 12), width=40, bd=1, relief=tk.SOLID)
        campo_origem.pack(pady=(0, 20))

        # adicionar campo de entrada para o destino
        rotulo_destino = tk.Label(frame_principal, text="Destino:", font=("Arial", 14, "bold"), bg="#F7F7F7", fg="#333")
        rotulo_destino.pack()

        campo_destino = tk.Entry(frame_principal, font=("Arial", 12), width=40, bd=1, relief=tk.SOLID)
        campo_destino.pack(pady=(0, 20))

        # adicionar um botão para iniciar a execução do código
        botao_executar = tk.Button(frame_principal, text="Executar", font=("Arial", 14, "bold"), bg="#4CAF50", fg="#FFFFFF", bd=0,
                                activebackground="#60bb67", activeforeground="#FFFFFF", command=executar_robo)
        botao_executar.pack(pady=20)

        # adicionar espaço para exibir o resultado
        rotulo_resultado = tk.Label(frame_principal, text="Resultado:", font=("Arial", 14, "bold"), bg="#F7F7F7", fg="#333")
        rotulo_resultado.pack(pady=(20, 5))

        resultado_text = tk.Text(frame_principal, font=("Arial", 12), width=60, height=10, bd=1, relief=tk.SOLID)
        resultado_text.pack()
        janela_principal = frame_principal



def abrir_janela_consulta(janela_menu):

        frame_consulta = tk.Toplevel(janela_menu)
        
        frame_consulta.configure(bg="#F7F7F7", padx=20, pady=20)

        # adicionar estilo ao frame
        frame_consulta.configure(bg="#F7F7F7", padx=20, pady=20)

        # adicionar campo de entrada para a origem
        aviso = tk.Label(frame_consulta, text="Consultar \nDigite com todos acentos e nesse padrão: São Paulo-SP", font=("Arial", 14, "bold"), bg="#F7F7F7", fg="#333")
        aviso.pack()

        rotulo_origem = tk.Label(frame_consulta, text="Origem:", font=("Arial", 14, "bold"), bg="#F7F7F7", fg="#333")
        rotulo_origem.pack(pady=(20, 5))

        campo_origem = tk.Entry(frame_consulta, font=("Arial", 12), width=40, bd=1, relief=tk.SOLID)
        campo_origem.pack(pady=(0, 20))

        # adicionar campo de entrada para o destino
        rotulo_destino = tk.Label(frame_consulta, text="Destino:", font=("Arial", 14, "bold"), bg="#F7F7F7", fg="#333")
        rotulo_destino.pack()

        campo_destino = tk.Entry(frame_consulta, font=("Arial", 12), width=40, bd=1, relief=tk.SOLID)
        campo_destino.pack(pady=(0, 20))


        # criar o botão de busca
        def buscar_resultados():
            # obter a origem e destino
            origem = campo_origem.get()
            destino = campo_destino.get()

            # buscar os resultados no banco de dados
            conexao = sqlite3.connect('resultado.db')
            cursor = conexao.cursor()
            cursor.execute("SELECT resultado FROM resultados WHERE origem = ? AND destino = ?", (origem, destino))
            resultados = cursor.fetchall()

            # mostrar os resultados na tela
            resultado_text.delete("1.0", tk.END)
            for resultado in resultados:
                resultado_text.insert(tk.END, resultado[0] + "\n")

        # adicionar um botão para iniciar a execução do código
        botao_executar = tk.Button(frame_consulta, text="Executar", font=("Arial", 14, "bold"), bg="#4CAF50", fg="#FFFFFF", bd=0,
                                activebackground="#60bb67", activeforeground="#FFFFFF", command=buscar_resultados)
        botao_executar.pack(pady=20)

        # adicionar espaço para exibir o resultado
        rotulo_resultado = tk.Label(frame_consulta, text="Resultado:", font=("Arial", 14, "bold"), bg="#F7F7F7", fg="#333")
        rotulo_resultado.pack(pady=(20, 5))

        resultado_text = tk.Text(frame_consulta, font=("Arial", 12), width=60, height=10, bd=1, relief=tk.SOLID)
        resultado_text.pack()

        janela_consulta = frame_consulta


def abrir_menu():

        janela_inicial = tk.Tk()
        janela_inicial.title("Tela Inicial")

        largura_tela = janela_inicial.winfo_screenwidth()
        altura_tela = janela_inicial.winfo_screenheight()
        
        largura_janela = int(largura_tela * 0.8)
        altura_janela = int(altura_tela * 0.7)
        tamanho_janela = f"{largura_janela}x{altura_janela}"
        janela_inicial.geometry(tamanho_janela)
        
        posicao_janela_x = int(largura_tela * 0.1)
        posicao_janela_y = int(altura_tela * 0.15)
        posicao_janela = f"+{posicao_janela_x}+{posicao_janela_y}"
        janela_inicial.geometry(posicao_janela)
        
        janela_inicial.resizable(False, False)

        frame_titulo = tk.Frame(janela_inicial)
        titulo_label = tk.Label(frame_titulo, text="Menu Principal", font=("Arial", 18, "bold"), fg="#333333")
        titulo_label.pack(pady=20)
        frame_titulo.pack()

        frame_botoes = tk.Frame(janela_inicial)

        botao_abrir_janela_principal = tk.Button(frame_botoes, text="Explorar", font=("Arial", 14, "bold"), bg="#4CAF50", fg="#FFFFFF", bd=0,
                                activebackground="#60bb67", activeforeground="#FFFFFF", padx=10, pady=5,
                                command=lambda: abrir_janela_principal(janela_inicial))
        botao_abrir_janela_principal.pack(side='left', padx=10, pady=5)

        botao_abrir_janela_consulta = tk.Button(frame_botoes, text="Consultar", font=("Arial", 14, "bold"), bg="#4CAF50", fg="#FFFFFF", bd=0,
                                activebackground="#60bb67", activeforeground="#FFFFFF", padx=10, pady=5,
                                command=lambda: abrir_janela_consulta(janela_inicial))
        botao_abrir_janela_consulta.pack(side='left', padx=10, pady=5)

        frame_botoes.pack(pady=20)
        
        # Adicione o caminho da imagem que você deseja utilizar
        caminho_imagem = "C:\\Users\\bruno\\projeto-impacta\\Projeto_Impacta\\frete.png"

        imagem = ImageTk.PhotoImage(Image.open(caminho_imagem))
        label_imagem = tk.Label(janela_inicial, image=imagem)
        label_imagem.pack(pady=20)

        janela_principal_aberta = True

        janela_inicial.mainloop()

abrir_menu()
