import tkinter as tk
import sqlite3

cor1 = '#252525'

# Função para abrir uma nova janela de tarefa
def abrir_nova_tarefa():
    nova_janela = tk.Toplevel(janela)
    nova_janela.title("Nova Tarefa")
    nova_janela.geometry("200x200")
    nova_janela.configure(bg=cor1)
    
    # Adicionar campos ou widgets necessários na nova janela
    nova_tarefa_label = tk.Label(nova_janela, text="Nova Tarefa", bg=cor1, fg="white")
    nova_tarefa_label.pack(pady=10)
    
    nova_tarefa_text = tk.Text(nova_janela, height=3, width=20)  # Ajuste a altura e largura conforme necessário
    nova_tarefa_text.pack(pady=10)
    
    salvar_button = tk.Button(nova_janela, text="Salvar", command=lambda: salvar_tarefa(nova_tarefa_text.get("1.0", tk.END), nova_janela))
    salvar_button.pack(pady=10)

# Função para abrir uma nova janela para remover tarefa
def abrir_remover_tarefa():
    remover_janela = tk.Toplevel(janela)
    remover_janela.title("Remover Tarefa")
    remover_janela.geometry("200x200")
    remover_janela.configure(bg=cor1)
    
    remove_tarefa_label = tk.Label(remover_janela, text="Remover Tarefa", bg=cor1, fg="white")
    remove_tarefa_label.pack(pady=10)
    
    remove_tarefa_text = tk.Text(remover_janela, height=3, width=20)  # Ajuste a altura e largura conforme necessário
    remove_tarefa_text.pack(pady=10)
    
    remover_button = tk.Button(remover_janela, text="Remover", command=lambda: remover_tarefa(remove_tarefa_text.get("1.0", tk.END), remover_janela))
    remover_button.pack(pady=10)

# Função para salvar a tarefa no banco de dados e atualizar o Canvas
def salvar_tarefa(tarefa, janela_para_fechar):
    tarefa = tarefa.strip()
    if tarefa:
        conn = sqlite3.connect('tarefas.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tarefas (descricao) VALUES (?)', (tarefa,))
        conn.commit()
        conn.close()
        janela_para_fechar.destroy()
        carregar_tarefas()

# Função para carregar as tarefas do banco de dados e exibi-las no Canvas
def carregar_tarefas(filtro=""):
    for widget in tasks_frame.winfo_children():
        widget.destroy()  # Limpar tasks_frame antes de recarregar as tarefas
    
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    if filtro:
        cursor.execute('SELECT id, descricao FROM tarefas WHERE descricao LIKE ?', ('%' + filtro + '%',))
    else:
        cursor.execute('SELECT id, descricao FROM tarefas')
    tarefas = cursor.fetchall()
    conn.close()
    
    for tarefa in tarefas:
        tarefa_id, descricao = tarefa
        var = tk.IntVar()
        check = tk.Checkbutton(tasks_frame, text=descricao, variable=var, bg="white")
        check.pack(anchor='w')

# Função para remover tarefa por descrição
def remover_tarefa(descricao, janela_para_fechar):
    descricao = descricao.strip()
    if descricao:
        conn = sqlite3.connect('tarefas.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tarefas WHERE descricao = ?', (descricao,))
        conn.commit()
        conn.close()
        carregar_tarefas()
        janela_para_fechar.destroy()

# Função para pesquisar tarefas
def pesquisar_tarefa(*args):
    filtro = pesquisa_entry.get().strip()
    carregar_tarefas(filtro)

# Configuração inicial do banco de dados
def inicializar_banco():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# GUI
janela = tk.Tk()
janela.title("Desafio 4")
janela.geometry("300x400")
janela.configure(bg=cor1)

# Ajuste do tamanho do quadro (Frame) e do Canvas
quadro_largura = 250  # Largura do quadro em pixels
quadro_altura = 300   # Altura do quadro em pixels

# Label de pesquisa de tarefas
pesquisa_label = tk.Label(janela, text="Pesquisar Tarefa", bg=cor1, fg="white")
pesquisa_label.place(x=25, y=0)

# Campo de pesquisa de tarefas
pesquisa_entry = tk.Entry(janela)
pesquisa_entry.place(x=25, y=20, width=quadro_largura)
pesquisa_entry.bind("<KeyRelease>", pesquisar_tarefa)

# Quadro da tarefa (Canvas) e Scrollbar
canvas_frame = tk.Frame(janela, width=quadro_largura, height=quadro_altura, bg="white")
canvas_frame.place(x=25, y=50, width=quadro_largura, height=quadro_altura)

canvas = tk.Canvas(canvas_frame, width=quadro_largura, height=quadro_altura, bg="white")
canvas.pack(side=tk.LEFT, fill='both', expand=True)

scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill='y')

canvas.configure(yscrollcommand=scrollbar.set)

tasks_frame = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=tasks_frame, anchor='nw')

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))

tasks_frame.bind("<Configure>", on_configure)

# Botões
buttons_frame = tk.Frame(janela, bg=cor1)
buttons_frame.place(relx=0.5, y=quadro_altura + 70, anchor='center') 

nova_tarefa_button = tk.Button(buttons_frame, text="Nova Tarefa", command=abrir_nova_tarefa)
nova_tarefa_button.pack(side='left', padx=(0, 5))  

remover_tarefa_button = tk.Button(buttons_frame, text="Remover Tarefa", command=abrir_remover_tarefa)
remover_tarefa_button.pack(side='left', padx=(5, 0)) 

# Inicializar banco de dados e carregar tarefas
inicializar_banco()
carregar_tarefas()

# Iniciando o loop da interface gráfica
janela.mainloop()
