import tkinter as tk
import numpy as np
from tkinter import messagebox
from fractions import Fraction

from attr.validators import max_len
from click import command
from pyasn1_modules.rfc5280 import common_name


# Função para gerar os campos de entrada para a matriz com base nas dimensões informadas pelo usuário
def gerar_matriz():
    try:
        # Obtém as dimensões inseridas pelo usuário
        linhas = int(entry_linhas.get())
        colunas = int(entry_colunas.get())

        # Valida se as dimensões são positivas
        if linhas <= 0 or colunas <= 0:
            raise ValueError

        # Remove quaisquer widgets antigos no frame da matriz
        for widget in frame_matriz.winfo_children():
            widget.destroy()

        # Limpa a lista de entradas para a matriz e cria novos campos
        matriz_inputs.clear()
        for i in range(linhas):
            linha_inputs = []
            for j in range(colunas):
                entrada = tk.Entry(frame_matriz, width=7, font=("Helvetica", 16), justify="center")
                entrada.grid(row=i, column=j, padx=5, pady=5)  # Posiciona cada entrada na grade
                linha_inputs.append(entrada)
            matriz_inputs.append(linha_inputs)

        # Adiciona o trace para monitorar os campos de valor
        for linha in matriz_inputs:
            for entry in linha:
                entry.bind("<KeyRelease>", verificar_campos)

        botao_salvar.place_forget()

    except ValueError:
        # Exibe uma mensagem de erro se as dimensões não forem válidas
        messagebox.showerror("Erro", "Insira valores válidos para linhas e colunas!")

# Verifica se todos os campos foram preenchidos
def verificar_campos(*args):
    for linha in matriz_inputs:
        for entry in linha:
            if entry.get() == "": # Se algum campo estiver vazio
                botao_salvar.place_forget() # Oculta o botão salvar
                return
    # Se todos os campos estiverem preenchidos, mostra o botão salvar
    botao_salvar.place(x=400, y=72)

# Função para monitorar os campos de entrada
def monitorar_campos():
    for linha in matriz_inputs:
        for entry in linha:
            entry.bind("<KeyRelease>", verificar_campos)

# Função para salvar a matriz criada pelo usuário
def salvar_matriz():
    global contador_matrizes

    # Permite apenas 2 matrizes serem adicionadas
    if contador_matrizes >= 2:
        messagebox.showerror("Erro", "Apenas duas matrizes permitidas")
        return
    try:
        # Lê os valores inseridos nos campos e converte para uma matriz
        matriz = []
        for linha_inputs in matriz_inputs:
            linha = []
            for entrada in linha_inputs:
                valor = int(entrada.get())  # Converte o valor digitado para inteiro
                linha.append(valor)
            matriz.append(linha)

        # Adiciona a matriz à lista de matrizes
        matrizes.append(matriz)
        contador_matrizes += 1

        # Exibe a matriz no frame de resultados
        exibir_matriz(matriz, contador_matrizes, frame_resultados)

        # Limpa os campos de entrada da matriz após o salvamento
        for linha in matriz_inputs:
            for entry in linha:
                entry.delete(0, tk.END) # Limpa o conteúdo de cada campo de entrada

        # Após limpar, ocultar o botão salvar novamente
        botao_salvar.place_forget()

        # Oculta o botão "Salvar" até que todos os campos sejam preenchidos novamente
        janela_principal.after(100, verificar_campos)  # Recalcula se os campos estão preenchidos para reexibir o botão salvar

    except ValueError:
        # Exibe uma mensagem de erro se os campos não forem preenchidos corretamente
        messagebox.showerror("Erro", "Certifique-se de preencher todos os campos com valores válidos!")


# Função para exibir uma matriz no frame de resultados
def exibir_matriz(matriz, numero, frame_destino):
    """
    Exibe uma matriz no frame de resultados com um título indicando o número da matriz.
    """
    # Obtém as dimensões da matriz
    dimensao = f"{len(matriz)}x{len(matriz[0])}"

    # Cria um novo frame para a matriz gerada
    matriz_frame = tk.Frame(frame_destino, borderwidth=1, padx=10, pady=10)
    matriz_frame.pack(pady=20)

    # Exibe a matriz no frame correto, centralizando
    matriz_frame.pack(side="left", padx=30, pady=10)

    # Adiciona um título indicando o número da matriz
    titulo = tk.Label(matriz_frame, text=f"Matriz {numero} ({dimensao}):", font=("Helvetica", 18, "bold"))
    titulo.pack(anchor="w")

    max_len = max(len(str(item)) for linha in matriz for item in linha)

    for linha in matriz:
        linha_formatada = "  ".join(f"{item:{max_len}}" for item in linha)  # Alinha os elementos
        linha_label = tk.Label(matriz_frame, text=linha_formatada, font=("Courier", 18))
        linha_label.pack(anchor="center")

# Função para limpar todas as matrizes
def limpar_todas_matrizes():
    # Limpa a lista de matrizes salvas
    matrizes.clear()

    # Zera o contador de matrizes
    global contador_matrizes
    contador_matrizes = 0

    # Remove todas as matrizes exibidas na interface
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    # Remove os widgets da interface
    for widget in frame_matriz.winfo_children():
        widget.grid_forget()

    # Exibe uma mensagem e confirmação
    messagebox.showinfo("Limpar Matrizes", "Todas as matrizes foram removidas!")

#Função para limpar o resultado de uma operação
def limpar_resultado(frame_resultados):
    for widget in frame_resultados.winfo_children():
        widget.destroy()

def abrir_janela_calculadora():
    if len(matrizes) < 1:
        messagebox.showerror("Erro", "Adicione pelo menos uma matriz para abrir a calculadora!")
        return

    # Oculta a janela principal
    janela_principal.withdraw()

    #Cria a nova janela
    janela_calculadora = tk.Toplevel()
    janela_calculadora.title("Calculadora")
    janela_calculadora.geometry("800x700")

    # Configura o que acontece quando a janela da calculadora é fechada
    def fechar_janela_calculadora():
        janela_calculadora.destroy()  # Fecha a janela da calculadora
        janela_principal.deiconify()  # Exibe a janela principal novamente

    janela_calculadora.protocol("WM_DELETE_WINDOW", fechar_janela_calculadora)

    # Titulo na nova janela
    label_calculadora = tk.Label(janela_calculadora, text="CALCULADORA", font=("Georgia", 20))
    label_calculadora.pack(pady=20)

    # Frame para exibir as matrizes
    frame_matrizes = tk.Frame(janela_calculadora)
    frame_matrizes.pack(pady=10)

    # Loop para exibir as matrizes
    for i, matriz in enumerate(matrizes, start=1):
        matriz_frame = tk.Frame(frame_matrizes, borderwidth=2, padx=20, pady=20)
        matriz_frame.pack(side="left", padx=30, pady=15)

        # Título para cada matriz
        titulo_matriz = tk.Label(matriz_frame, text=f"Matriz {i}:", font=("Helvetica", 16, "bold"))
        titulo_matriz.pack()

        # Calcula a largura máxima dos números na matriz para alinhamento
        max_len = max(len(str(item)) for linha in matriz for item in linha)

        # Exibe cada linha da matriz
        for linha in matriz:
            linha_formatada = "  ".join(f"{item:<{max_len}}" for item in linha)  # Alinha os elementos
            linha_label = tk.Label(matriz_frame, text=linha_formatada, font=("Courier", 18), bg="#f5f5f5")
            linha_label.pack(anchor="center", pady=5)

    # Frame para exibir o resultado
    frame_resultados = tk.Frame(janela_calculadora)
    frame_resultados.pack(pady=20)

    # Botão para limpar o resultado
    botao_limpar = tk.Button(janela_calculadora, text="LIMPAR", command=lambda: limpar_resultado(frame_resultados), font=("Helvetica", 12), bg="black", fg="white", width=10)
    botao_limpar.pack(side="left", padx=10, pady=10)

    # Posiciona o botão no lado superior direito
    botao_limpar.place(relx=1.0, y=650, anchor="ne")

    # Botão para somar
    botao_somar = tk.Button(janela_calculadora, text="SOMAR", command=lambda: somar_subratir_matrizes(
        frame_resultados, lambda x, y: x + y,"Soma"), font=("Helvetica", 12), bg="#FF5722", fg="white", width=13)
    botao_somar.pack(side="left", padx=10, pady=10)

    # Posiciona o botão no lado superior direito
    botao_somar.place(relx=1.0, y=80, anchor="ne")

    # Botão para subtrair
    botao_subtrair = tk.Button(janela_calculadora, text="SUBTRAIR", command=lambda: somar_subratir_matrizes(
        frame_resultados, lambda x, y: x - y, "Subtração"), font=("Helvetica", 12), bg="#FF5722", fg="white", width=13)
    botao_subtrair.pack(side="left", padx=10, pady=10)

    # Posiciona o botão no lado superior direito abaixo do botão somar
    botao_subtrair.place(relx=1.0, y=130, anchor="ne")

    # Botão para multiplicar
    botao_multiplicar = tk.Button(janela_calculadora, text="MULTIPLICAR", command=lambda: multiplicar_matrizes(frame_resultados), font=("Helvetica", 12), bg="#FF5722", fg="white", width=13)
    botao_multiplicar.pack(side="left", padx=10, pady=10)

    # Posiciona o botão no lado superior direito abaixo do botão subtrair
    botao_multiplicar.place(relx=1.0, y=180, anchor="ne")

    # Botão para transpor a última matriz
    botao_transposta = tk.Button(janela_calculadora, text="TRANSPOR", command=lambda: transpor_matriz(frame_resultados), font=("Helvetica", 12), bg="#FF5722", fg="white", width=13)
    botao_transposta.pack(side="left", padx=10, pady=10)

    # Posiciona o botão no lado superior direito abaixo do botão multiplicar
    botao_transposta.place(relx=1.0, y=230, anchor="ne")

    # Botão para calcular o determinante
    botao_determinante = tk.Button(janela_calculadora, text="DETERMINANTE", command=lambda: determinante_matriz(frame_resultados, matrizes), font=("Helvetica", 12), bg="#FF5722", fg="white", width=13)
    botao_determinante.pack(side="left", padx=10, pady=10)

    # Posiciona o botão no lado superior direito abaixo do botão transposta
    botao_determinante.place(relx=1.0, y=280, anchor="ne")

    # Adiciona botão na janela da calculadora para calcular o cofator
    botao_cofator = tk.Button(janela_calculadora, text="COFATOR", command=lambda: matriz_cofator(frame_resultados, matrizes), font=("Helvetica", 12), bg="#FF5722", fg="white", width=13)
    botao_cofator.pack(side="left", padx=10, pady=10)

    # Posiciona o botão no lado superior direito abaixo do botão transposta
    botao_cofator.place(relx=1.0, y=330, anchor="ne")

    # Adiciona botão na janela da calculadora para calcular a matriz adjunta
    botao_adjunta = tk.Button(janela_calculadora, text="ADJUNTA", command=lambda: matriz_adjunta(frame_resultados, matrizes),font=("Helvetica", 12), bg="#FF5722", fg="white", width=13)
    botao_adjunta.pack(side="left", padx=10, pady=10)

    # Posiciona o botão no lado superior direito abaixo do botão cofator
    botao_adjunta.place(relx=1.0, y=380, anchor="ne")

    botao_inversa = tk.Button(janela_calculadora, text="INVERSA", command=lambda: matriz_inversa_fracoes(frame_resultados, matrizes), font=("Helvetica", 12), bg="#FF5722", fg="white", width=13)
    botao_inversa.pack(side="left", padx=10, pady=10)

    # Posiciona o botão no lado superior direito abaixo do botão adjunta
    botao_inversa.place(relx=1.0, y=430, anchor="ne")


# Função para somar as duas últimas matrizes salvas, caso tenham o mesmo tamanho
def somar_subratir_matrizes(frame_resultados, operacao, operacao_nome):
    # Verifica se há pelo menos duas matrizes salvas
    if len(matrizes) < 2:
        messagebox.showerror("Erro", f"São necessárias pelo menos duas matrizes para {operacao_nome}!")
        return

    # Obtém as duas últimas matrizes
    matriz1 = matrizes[-2]
    matriz2 = matrizes[-1]

    # Verifica se as dimensões das matrizes são iguais
    if len(matriz1) != len(matriz2) or any(len(m1) != len(m2) for m1, m2 in zip(matriz1, matriz2)):
        messagebox.showerror("Erro", "As matrizes devem ter o mesmo tamanho para realizar a operação!")
        return

    # Aplica a operação nos elementos correspondentes
    matriz_resultado = [[operacao(m1, m2) for m1, m2 in zip(l1, l2)] for l1, l2 in zip(matriz1, matriz2)]

    for widget in frame_resultados.winfo_children():
        widget.destroy()

    # Exibe a matriz resultado
    exibir_matriz(matriz_resultado, f"Resultado ({operacao_nome})", frame_resultados)

# Função para multiplicar as duas últimas matrizes salvas
def multiplicar_matrizes(frame_resultados):
    # Verifica se há pelo menos duas matrizes salvas
    if len (matrizes) < 2:
        messagebox.showerror("Erro", "São necessárias pelo menos duas matrizes para multiplicar!")
        return

    # Obtém as duas últimas matrizes
    matriz1 = matrizes[-2]
    matriz2 = matrizes[-1]

    # Verifica se a multiplicação é possível (número de colunas de matriz1 igual ao número de linhas de matriz2)
    if len(matriz1[0]) != len(matriz2):
        messagebox.showerror("Erro", "O número de colunas da matriz 1 deve ser igual ao número de linhas da matriz 2!")
        return

    # Realiza a multiplicação
    matriz_resultado = []
    for i in range(len(matriz1)): # Para cada linha da matriz 1
        linha_resultado = []
        for j in range(len(matriz2[0])): # Para cada coluna da matriz 2
            # Calcula o valor do elemento (i, j) da matriz resultado
            valor = sum(matriz1[i][k] * matriz2[k][j] for k in range(len(matriz2)))
            linha_resultado.append(valor)
        matriz_resultado.append(linha_resultado)

    # Atualiza a exibição para remover as matrizes usadas
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    # Exibe a matriz resultado
    exibir_matriz(matriz_resultado, "Resultado (Multiplicação)", frame_resultados)

def transpor_matriz(frame_resultados):
    # Verifica se há pelo menos uma matriz salva
    if len(matrizes) < 1:
        messagebox.showerror("Erro", "Adicione uma matriz para gerar a transposta!")
        return

    # Cria uma lista com os nomes das matrizes (como A3x3, B5x2, etc.)
    nomes_matrizes = [f"Matriz {i + 1} ({len(matriz)}x{len(matriz[0])})" for i, matriz in enumerate(matrizes)]

    # Cria uma nova janela para escolher a matriz
    janela_selecao = tk.Toplevel()
    janela_selecao.title("Escolher Matriz para Transpor")

    # Cria o menu suspenso para selecionar a matriz
    var_matriz_selecionada = tk.StringVar(janela_selecao)
    var_matriz_selecionada.set(nomes_matrizes[0])  # Define a primeira matriz como padrão

    option_menu = tk.OptionMenu(janela_selecao, var_matriz_selecionada, *nomes_matrizes)
    option_menu.pack(pady=10)

    # Função para transpor a matriz selecionada
    def transpor_selecionada():
        # Obtém o índice da matriz selecionada
        indice_matriz = nomes_matrizes.index(var_matriz_selecionada.get())

        # Obtém a matriz selecionada
        matriz = matrizes[indice_matriz]

        # Gera a matriz transposta
        matriz_transposta = list(zip(*matriz))

        # Atualiza a exibição para remover a matriz usada
        for widget in frame_resultados.winfo_children():
            widget.destroy()

        # Exibe a matriz transposta
        exibir_matriz(matriz_transposta, f"{indice_matriz + 1} Transposta ", frame_resultados)

        # Fecha a janela de seleção
        janela_selecao.destroy()

    # Botão para confirmar a transposição
    botao_confirmar = tk.Button(janela_selecao, text="Transpor", command=transpor_selecionada, font=("Helvetica", 12), bg="#4CAF50", fg="white")
    botao_confirmar.pack(pady=20)

# Função para calcular o determinante de uma matriz
def determinante_matriz(frame_resultados, matrizes):
    # Verifica se há pelo menos uma matriz salva
    if len(matrizes) < 1:
        messagebox.showerror("Erro", "Adicione uma matriz para calcular o determinante!")
        return

        # Cria uma nova janela para o menu suspenso
    janela_selecao = tk.Toplevel()
    janela_selecao.title("Selecionar Matriz")

    # Cria os nomes das matrizes para o menu suspenso
    nomes_matrizes = [f"Matriz {i + 1} ({len(matriz)}x{len(matriz[0])})" for i, matriz in enumerate(matrizes)]

    # Variável para armazenar a matriz selecionada
    matriz_selecionada = None

    # Função para definir a matriz selecionada e fechar a janela
    def selecionar():
        nonlocal matriz_selecionada  # Permite modificar a variável externa
        indice = nomes_matrizes.index(var_matriz.get())
        matriz_selecionada = matrizes[indice]
        janela_selecao.destroy()

    # Cria o menu suspenso
    var_matriz = tk.StringVar(janela_selecao)
    var_matriz.set(nomes_matrizes[0])  # Define o primeiro item como padrão
    menu = tk.OptionMenu(janela_selecao, var_matriz, *nomes_matrizes)
    menu.pack(pady=10)

    # Botão para confirmar a seleção
    botao_selecionar = tk.Button(janela_selecao, text="Selecionar", command=selecionar)
    botao_selecionar.pack()

    janela_selecao.wait_window(janela_selecao)  # Espera a janela ser fechada

    if matriz_selecionada is None:  # Se o usuário não selecionou nada
        return

    # Função recursiva para calcular o determinante
    def calcular_determinante(matriz):
        # Caso base: determinante de uma matriz 2x2
        if len(matriz) == 2:
            return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
        else:
            determinante = 0
            for i in range(len(matriz)):
                submatriz = [linha[:i] + linha[i + 1:] for linha in matriz[1:]]
                determinante += ((-1) ** i) * matriz[0][i] * calcular_determinante(submatriz)
            return determinante

    # Verifica se a matriz é quadrada
    if len(matriz_selecionada) != len(matriz_selecionada[0]):
        messagebox.showerror("Erro", "O determinante só pode ser calculado para matrizes quadradas!")
        return

    # Calcula o determinante
    det = calcular_determinante(matriz_selecionada)

    # Exibe o resultado do determinante
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    label_resultado = tk.Label(frame_resultados, text=f"Determinante: {det}", font=("Helvetica", 18, "bold"))
    label_resultado.pack(pady=10)

def matriz_cofator(frame_resultados, matrizes):
    # Verifica se há pelo menos uma matriz salva
    if len(matrizes) < 1:
        messagebox.showerror("Erro", "Adicione uma matriz para calcular a matriz cofator!")
        return

    janela_selecao = tk.Toplevel()
    janela_selecao.title("Selecionar Matriz")

    nomes_matrizes = [f"Matriz {i+1} ({len(matriz)}x{len(matriz[0])})" for i, matriz in enumerate(matrizes)]

    matriz_selecionada = None

    def selecionar():
        nonlocal matriz_selecionada
        indice = nomes_matrizes.index(var_matriz.get())
        matriz_selecionada = matrizes[indice]
        janela_selecao.destroy()

    var_matriz = tk.StringVar(janela_selecao)
    var_matriz.set(nomes_matrizes[0])
    menu = tk.OptionMenu(janela_selecao, var_matriz, *nomes_matrizes)
    menu.pack(pady=10)

    botao_selecionar = tk.Button(janela_selecao, text="Selecionar", command=selecionar)
    botao_selecionar.pack()

    janela_selecao.wait_window(janela_selecao)

    if matriz_selecionada is None:
        return

    # Verifica se a matriz é quadrada
    if len(matriz_selecionada) != len(matriz_selecionada[0]):
        messagebox.showerror("Erro", "A matriz cofator só pode ser calculada para matrizes quadradas!")
        return

    # Função para calcular o determinante de uma matriz
    def calcular_determinante(matriz):
        return round(np.linalg.det(matriz))

    # Calcula a matriz cofator
    matriz_cofator = []
    for i in range(len(matriz_selecionada)):
        linha_cofator = []
        for j in range(len(matriz_selecionada)):
            submatriz = [linha[:j] + linha[j + 1:] for k, linha in enumerate(matriz_selecionada) if k != i]
            cofator = ((-1) ** (i + j)) * calcular_determinante(submatriz)
            linha_cofator.append(cofator)
        matriz_cofator.append(linha_cofator)

    # Exibe a matriz cofator formatada
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    numero_matriz = matrizes.index(matriz_selecionada) + 1
    titulo = tk.Label(frame_resultados, text=f"Matriz Cofator da Matriz {numero_matriz}:", font=("Helvetica", 18, "bold"))
    titulo.pack(anchor="center")

    for linha in matriz_cofator:  # Itera sobre a matriz completa
        linha_formatada = "  ".join(f"{item:3}" for item in linha)
        linha_label = tk.Label(frame_resultados, text=linha_formatada, font=("Courier", 18))
        linha_label.pack(anchor="center")

    return matriz_cofator

def matriz_adjunta(frame_resultados, matrizes):
    # Verifica se há pelo menos uma matriz salva
    if len(matrizes) < 1:
        messagebox.showerror("Erro", "Adicione uma matriz para calcular a matriz adjunta!")
        return

    janela_selecao = tk.Toplevel()
    janela_selecao.title("Selecionar Matriz")

    nomes_matrizes = [f"Matriz {i+1} ({len(matriz)}x{len(matriz[0])})" for i, matriz in enumerate(matrizes)]

    matriz_selecionada = None

    def selecionar():
        nonlocal matriz_selecionada
        indice = nomes_matrizes.index(var_matriz.get())
        matriz_selecionada = matrizes[indice]
        janela_selecao.destroy()

    var_matriz = tk.StringVar(janela_selecao)
    var_matriz.set(nomes_matrizes[0])
    menu = tk.OptionMenu(janela_selecao, var_matriz, *nomes_matrizes)
    menu.pack(pady=10)

    botao_selecionar = tk.Button(janela_selecao, text="Selecionar", command=selecionar)
    botao_selecionar.pack()

    janela_selecao.wait_window(janela_selecao)

    if matriz_selecionada is None:
        return

    # Verifica se a matriz é quadrada
    if len(matriz_selecionada) != len(matriz_selecionada[0]):
        messagebox.showerror("Erro", "A matriz adjunta só pode ser calculada para matrizes quadradas!")
        return

    # Função para calcular o determinante de uma matriz
    def calcular_determinante(matriz):
        return round(np.linalg.det(matriz))

    # Calcula a matriz de cofatores
    matriz_cofator = []
    for i in range(len(matriz_selecionada)):
        linha_cofator = []
        for j in range(len(matriz_selecionada)):
            submatriz = [linha[:j] + linha[j + 1:] for k, linha in enumerate(matriz_selecionada) if k != i]
            cofator = ((-1) ** (i + j)) * calcular_determinante(submatriz)
            linha_cofator.append(cofator)
        matriz_cofator.append(linha_cofator)

    # Calcula a matriz adjunta (transposta da matriz de cofatores)
    matriz_adjunta = list(map(list, zip(*matriz_cofator)))

    # Exibe a matriz adjunta formatada
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    numero_matriz = matrizes.index(matriz_selecionada) + 1
    titulo = tk.Label(frame_resultados, text=f"Matriz Adjunta da Matriz {numero_matriz}:", font=("Helvetica", 18, "bold"))
    titulo.pack(anchor="center")

    for linha in matriz_adjunta:  # Itera sobre a matriz completa
        linha_formatada = "  ".join(f"{item:3}" for item in linha)
        linha_label = tk.Label(frame_resultados, text=linha_formatada, font=("Courier", 18))
        linha_label.pack(anchor="center")

    return matriz_adjunta

def matriz_inversa_fracoes(frame_resultados, matrizes):
    # Verifica se há pelo menos uma matriz salva
    if len(matrizes) < 1:
        messagebox.showerror("Erro", "Adicione uma matriz para calcular a matriz inversa!")
        return

    janela_selecao = tk.Toplevel()
    janela_selecao.title("Selecionar Matriz")

    nomes_matrizes = [f"Matriz {i+1} ({len(matriz)}x{len(matriz[0])})" for i, matriz in enumerate(matrizes)]

    matriz_selecionada = None

    def selecionar():
        nonlocal matriz_selecionada
        indice = nomes_matrizes.index(var_matriz.get())
        matriz_selecionada = matrizes[indice]
        janela_selecao.destroy()

    var_matriz = tk.StringVar(janela_selecao)
    var_matriz.set(nomes_matrizes[0])
    menu = tk.OptionMenu(janela_selecao, var_matriz, *nomes_matrizes)
    menu.pack(pady=10)

    botao_selecionar = tk.Button(janela_selecao, text="Selecionar", command=selecionar)
    botao_selecionar.pack()

    janela_selecao.wait_window(janela_selecao)

    if matriz_selecionada is None:
        return

    # Verifica se a matriz é quadrada
    if len(matriz_selecionada) != len(matriz_selecionada[0]):
        messagebox.showerror("Erro", "A matriz inversa só pode ser calculada para matrizes quadradas!")
        return

    # Verifica se a matriz é inversível (determinante diferente de zero)
    determinante = np.linalg.det(matriz_selecionada)
    if determinante == 0:
        messagebox.showerror("Erro", "A matriz não é inversível (determinante igual a zero)!")
        return

    # Calcula a matriz inversa usando numpy
    inversa_np = np.linalg.inv(matriz_selecionada)

    # Converte os elementos da matriz inversa para frações
    matriz_inversa_frac = []
    for linha in inversa_np:
        linha_frac = [Fraction(elemento).limit_denominator() for elemento in linha]
        matriz_inversa_frac.append(linha_frac)

    # Exibe a matriz inversa formatada em frações
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    numero_matriz = matrizes.index(matriz_selecionada) + 1
    titulo = tk.Label(frame_resultados, text=f"Matriz Inversa da Matriz {numero_matriz}:", font=("Helvetica", 18, "bold"))
    titulo.pack(anchor="center")

    for linha in matriz_inversa_frac:  # Itera sobre a matriz completa
        linha_formatada = "  ".join(f"{str(item):>3}" for item in linha)  # Formata cada fração
        linha_label = tk.Label(frame_resultados, text=linha_formatada, font=("Courier", 18))
        linha_label.pack(anchor="center")

    return matriz_inversa_frac

# Configuração da janela principal
janela_principal = tk.Tk()
janela_principal.title("Gerador de Matriz")
janela_principal.geometry("800x750")
janela_principal.resizable(False, False)

# Centraliza a janela na tela
janela_principal.eval('tk::PlaceWindow . center')

# Lista para armazenar os campos de entrada e as matrizes criadas
matriz_inputs = []
matrizes = []

# Contador para identificar cada matriz criada
contador_matrizes = 0

# Cabeçalho da aplicação
titulo_label = tk.Label(janela_principal, text="GERADORA DE MATRIZES", font=("Georgia", 20, "bold"))
titulo_label.pack(pady=10)

# Campos para inserir o número de linhas e colunas
label_linhas = tk.Label(janela_principal, text="Quantidade de Linhas:", font=("Helvetica", 16))
label_linhas.place(x=10, y=80) # Posição no canto superior esquerdo
entry_linhas = tk.Entry(janela_principal, font=("Helvetica", 16), width=4)
entry_linhas.place(x=240, y=80)

label_colunas = tk.Label(janela_principal, text="Quantidade de Colunas:", font=("Helvetica", 16))
label_colunas.place(x=10, y=120)
entry_colunas = tk.Entry(janela_principal, font=("Helvetica", 16), width=4)
entry_colunas.place(x=240, y=120)

# Botão para gerar os campos de entrada para a matriz
botao_gerar = tk.Button(janela_principal, text="Gerar Matriz", command=gerar_matriz, font=("Helvetica", 16), bg="#4CAF50", fg="white", width=15)
botao_gerar.place(x=10, y=160)

# Frame para exibir os campos de entrada da matriz
frame_matriz = tk.Frame(janela_principal)
frame_matriz.place(x=350, y=120)

# Botão para salvar a matriz gerada
botao_salvar = tk.Button(janela_principal, text="Salvar Matriz", command=salvar_matriz, font=("Helvetica", 16), bg="#4CAF50", fg="white", width=15)
botao_salvar.place_forget()

# Verifica os campos sempre que o usuário interagir com os campos da matriz
janela_principal.after(100, monitorar_campos)  # Atualiza a verificação a cada 100ms

# Frame para exibir as matrizes geradas
frame_resultados = tk.Frame(janela_principal)
frame_resultados.place(x=160, y=300)

# Botão para limpar todas as matrizes
botao_limpar = tk.Button(janela_principal, text="Limpar Todas Matrizes", command=limpar_todas_matrizes, font=("Helvetica", 12), bg="black", fg="white", width=20)
botao_limpar.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

# Botão para abrir a janela calculadora
botao_abrir_calculadora = tk.Button(janela_principal, text="Abrir Calculadora", command=abrir_janela_calculadora, font=("Helvetica", 12), bg="#FF5722", fg="white", width=20)
botao_abrir_calculadora.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

# Inicia o loop principal da interface
janela_principal.mainloop()