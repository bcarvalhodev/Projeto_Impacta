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




# criar a janela principal
janela = tk.Tk()
janela.title("Robô de Cotação de Frete")
janela.geometry("800x600")
janela.resizable(False, False)

# centralizar a janela na tela
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
largura_janela = janela.winfo_reqwidth()
altura_janela = janela.winfo_reqheight()
pos_x = int((largura_tela / 2) - (largura_janela / 2))
pos_y = int((altura_tela / 2) - (altura_janela / 2))
janela.geometry(f"+{pos_x}+{pos_y}")

# adicionar estilo à janela
janela.configure(bg="#F7F7F7", padx=20, pady=20)

# adicionar campo de entrada para a origem
aviso = tk.Label(janela, text="Digite com todos acentos e nesse padrão: São Paulo-SP", font=("Arial", 14, "bold"), bg="#F7F7F7", fg="#333")
aviso.pack()

rotulo_origem = tk.Label(janela, text="Origem:", font=("Arial", 14, "bold"), bg="#F7F7F7", fg="#333")
rotulo_origem.pack(pady=(20, 5))

campo_origem = tk.Entry(janela, font=("Arial", 12), width=40, bd=1, relief=tk.SOLID)
campo_origem.pack(pady=(0, 20))

# adicionar campo de entrada para o destino
rotulo_destino = tk.Label(janela, text="Destino:", font=("Arial", 14, "bold"), bg="#F7F7F7", fg="#333")
rotulo_destino.pack()

campo_destino = tk.Entry(janela, font=("Arial", 12), width=40, bd=1, relief=tk.SOLID)
campo_destino.pack(pady=(0, 20))

# adicionar um botão para iniciar a execução do código
botao_executar = tk.Button(janela, text="Executar", font=("Arial", 14, "bold"), bg="#4CAF50", fg="#FFFFFF", bd=0,
                           activebackground="#60bb67", activeforeground="#FFFFFF", command=executar_robo)
botao_executar.pack(pady=20)

# adicionar espaço para exibir o resultado
rotulo_resultado = tk.Label(janela, text="Resultado:", font=("Arial", 14, "bold"), bg="#F7F7F7", fg="#333")
rotulo_resultado.pack(pady=(20, 5))

resultado_text = tk.Text(janela, font=("Arial", 12), width=60, height=10, bd=1, relief=tk.SOLID)
resultado_text.pack()

# iniciar a janela principal
janela.mainloop()

conexao.close()

