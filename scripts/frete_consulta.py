import sqlite3
import tkinter as tk


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
botao_executar = tk.Button(janela, text="Executar", font=("Arial", 14, "bold"), bg="#4CAF50", fg="#FFFFFF", bd=0,
                           activebackground="#60bb67", activeforeground="#FFFFFF", command=buscar_resultados)
botao_executar.pack(pady=20)

# adicionar espaço para exibir o resultado
rotulo_resultado = tk.Label(janela, text="Resultado:", font=("Arial", 14, "bold"), bg="#F7F7F7", fg="#333")
rotulo_resultado.pack(pady=(20, 5))

resultado_text = tk.Text(janela, font=("Arial", 12), width=60, height=10, bd=1, relief=tk.SOLID)
resultado_text.pack()

# exibir a janela
janela.mainloop()
