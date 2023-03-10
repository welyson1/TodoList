import tkinter as tk
import psycopg2

#Para criar a tabela uso o codigo abaixo
# CREATE TABLE todo_list (
#   id SERIAL PRIMARY KEY,
#   task_name VARCHAR(255) NOT NULL,
#   due_date DATE,
#   priority INT,
#   completed BOOLEAN DEFAULT false
# );

class TaskApp(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    self.pack()
    self.master.title("Lista de Tarefas")
    self.master.geometry("400x400")

    self.conn = psycopg2.connect(
      # Coloque as credenciais do banco de dados postgres aqui
      host="localhost",
      database="tasks",
      user="postgres",
      password="senha"
    )
    self.cursor = self.conn.cursor()       
    self.create_widgets()

  def create_widgets(self):      
    # Criar widgets
    self.task_label = tk.Label(self, text="Tarefa:")
    self.task_label.grid(row=0, column=0)
    self.task_entry = tk.Entry(self)
    self.task_entry.grid(row=0, column=1)

    self.date_label = tk.Label(self, text="Data de Vencimento (YYYY-MM-DD):")
    self.date_label.grid(row=1, column=0)
    self.date_entry = tk.Entry(self)
    self.date_entry.grid(row=1, column=1)

    self.priority_label = tk.Label(self, text="Prioridade (1-5):")
    self.priority_label.grid(row=2, column=0)
    self.priority_entry = tk.Entry(self)
    self.priority_entry.grid(row=2, column=1)

    self.add_button = tk.Button(self, text="Adicionar Tarefa", command=self.add_task)
    self.add_button.grid(row=3, column=1)

    self.task_list = tk.Listbox(self)
    self.task_list.grid(row=4, column=0, columnspan=2)

    self.refresh_button = tk.Button(self, text="Atualizar Lista", command=self.refresh_list)
    self.refresh_button.grid(row=5, column=1)

  # Definir cursor para o banco de dados
    self.cursor = self.conn.cursor()

  def refresh_list(self):    
    # Limpar lista atual
    self.task_list.delete(0, tk.END)

    # Obter lista de tarefas do banco de dados
    cursor = self.conn.cursor()
    cursor.execute("SELECT * FROM todo_list ORDER BY priority DESC")
    rows = cursor.fetchall()
    cursor.close()

    # Adicionar tarefas ?? lista
    for row in rows:
      task = row[1]
      due_date = row[2].strftime("%Y-%m-%d")
      priority = row[3]
      completed = row[4]
      if completed:
        task += " (Conclu??da)"
      self.task_list.insert(tk.END, f"({priority}) {due_date}: {task}")

  def add_task(self):
    # Adicionar tarefa ao banco de dados
    task = self.task_entry.get()
    date = self.date_entry.get()
    priority = int(self.priority_entry.get())
    cursor = self.conn.cursor()
    cursor.execute("INSERT INTO todo_list (task_name, due_date, priority) VALUES (%s, %s, %s)",(task, date, priority))
    self.conn.commit()
    cursor.close()

    # Limpar caixas de entrada
    self.task_entry.delete(0, tk.END)
    self.date_entry.delete(0, tk.END)
    self.priority_entry.delete(0, tk.END)

    # Atualizar lista
    self.refresh_list()

root = tk.Tk()
app = TaskApp(master=root)
app.mainloop()