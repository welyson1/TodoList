import tkinter as tk
import psycopg2
from tkinter import messagebox
import win32gui
import win32con

# Para criar a tabela uso o codigo abaixo
# CREATE TABLE todo_list (
#   id SERIAL PRIMARY KEY,
#   task_name VARCHAR(255) NOT NULL,
#   due_date DATE,
#   priority INT,
#   completed BOOLEAN DEFAULT false
# );

# Obter o identificador da janela do console
console_window = win32gui.GetForegroundWindow()

# Ocultar a janela do console
win32gui.ShowWindow(console_window, win32con.SW_HIDE)

class TaskApp(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    self.pack()
    self.master.title("Lista de Tarefas")
    self.master.geometry("661x600")

    self.conn = psycopg2.connect(
      # Coloque as credenciais do banco de dados postgres aqui
      host="db.dfmqkzxfikspeqlukshk.supabase.co",
      database="postgres",
      user="postgres",
      password="SYt5A0lRZ7d9LgCV"
    )
    self.cursor = self.conn.cursor()       
    self.create_widgets()
    #Atualizar lista
    self.refresh_list()

  def create_widgets(self):     
    # Criar widgets
    self.task_label = tk.Label(self, text="Tarefa:", fg="black", font=("Arial", 14))
    self.task_label.grid(row=0, column=0, padx=10, pady=10, sticky="E")

    self.task_entry = tk.Entry(self, bg="lightgray", fg="black", font=("Arial", 14), bd=3, relief="groove")
    self.task_entry.grid(row=0, column=1, padx=10, pady=10)

    self.date_label = tk.Label(self, text="Data de Vencimento \n(YYYY-MM-DD):", fg="black", font=("Arial", 14))
    self.date_label.grid(row=1, column=0, padx=10, pady=10, sticky="E")

    self.date_entry = tk.Entry(self, bg="lightgray", fg="black", font=("Arial", 14), bd=3, relief="groove")
    self.date_entry.grid(row=1, column=1, padx=10, pady=10)

    self.priority_label = tk.Label(self, text="Prioridade (1-5):", fg="black", font=("Arial", 14))
    self.priority_label.grid(row=2, column=0, padx=10, pady=10, sticky="E")

    self.priority_entry = tk.Entry(self, bg="lightgray", fg="black", font=("Arial", 14), bd=3, relief="groove")
    self.priority_entry.grid(row=2, column=1, padx=10, pady=10)

    self.id_entry = tk.Entry(self, show="*", width=15)

    self.add_button = tk.Button(self, text="Adicionar Tarefa ➕", bg="#3CB371", fg="white", font=("Arial", 14), command=self.add_task, bd=3, relief="groove")
    self.add_button.grid(row=3, column=1, padx=10, pady=10, sticky="EW")

    self.edit_button = tk.Button(self, text="Editar Tarefa 🖊️", bg="orange", fg="white", font=("Arial", 14), command=self.edit_task, bd=3, relief="groove")
    self.edit_button.grid(row=5, column=0, padx=10, pady=10, sticky="EW") 

    self.task_list = tk.Listbox(self, bg="lightgray", font=("Arial", 14), bd=3, relief="groove")
    self.task_list.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="EW")
    self.task_list.bind("<Double-Button-1>", self.show_task_info)

    # self.refresh_button = tk.Button(self, text="Atualizar Lista 🔄️", bg="blue", fg="white", font=("Arial", 14), command=self.refresh_list, bd=3, relief="groove")
    # self.refresh_button.grid(row=3, column=0, padx=10, pady=10, sticky="EW")

    self.delete_button = tk.Button(self, text="Apagar Tarefa ❌", bg="#B22222", fg="white", font=("Arial", 14), command=self.delete_task, bd=3, relief="groove")
    self.delete_button.grid(row=3, column=0, padx=10, pady=10, sticky="EW")

    self.save_button = tk.Button(self, text="Salvar alteração 💾", bg="#1E90FF", fg="white", font=("Arial", 14), command=self.add_task, bd=3, relief="groove")
    self.save_button.grid(row=5, column=1, padx=10, pady=10, sticky="EW")

  # Definir cursor para o banco de dados
    self.cursor = self.conn.cursor()
    
  def show_task_info(self, event):
    selected_task = self.task_list.get(tk.ACTIVE)
    task_info = selected_task.split(":")[1].strip()
    task_date = selected_task.split(":")[0].split(" ")[1]
    task_priority = selected_task.split(" ")[0]
    messagebox.showinfo(
      title="Informações da Tarefa",
      message=f"Prioridade: {task_priority}\nData de Vencimento: {task_date}\nTarefa: {task_info}"
    )
    

  def refresh_list(self):    
    # Limpar lista atual
    self.task_list.delete(0, tk.END)

    # Obter lista de tarefas do banco de dados
    cursor = self.conn.cursor()
    cursor.execute("SELECT * FROM todo_list ORDER BY priority DESC")
    rows = cursor.fetchall()
    cursor.close()

    # Adicionar tarefas à lista
    for row in rows:
      task = row[1]
      due_date = row[2].strftime("%Y-%m-%d")
      priority = row[3]
      completed = row[4]
      if completed:
        task += " (Concluída)"
      self.task_list.insert(tk.END, f"({priority}) {due_date}: {task}")

  def add_task(self):
    id = self.id_entry.get()
    task = self.task_entry.get()
    date = self.date_entry.get()
    priority = int(self.priority_entry.get())
    if id:
      cursor = self.conn.cursor()
      cursor.execute("UPDATE todo_list SET task_name = %s, due_date = %s, priority = %s WHERE id = %s",(task, date, priority, id))
      self.conn.commit()
      cursor.close()
      # Limpar caixas de entrada
      self.id_entry.delete(0, tk.END)
      self.task_entry.delete(0, tk.END)
      self.date_entry.delete(0, tk.END)
      self.priority_entry.delete(0, tk.END)
      self.refresh_list()
      return

    # Adicionar tarefa ao banco de dados
    
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

    # Editar Tarefa
  def edit_task(self):
      selection = self.task_list.curselection()
      if not selection:
          return
      task = self.task_list.get(selection[0])
      task_name = task.split(": ")[1].split(" (")[0]

      # Excluir a tarefa do banco de dados
      cursor = self.conn.cursor()
      cursor.execute("SELECT * FROM todo_list WHERE task_name = %s", (task_name,))
      
      rows = cursor.fetchall()
      cursor.close()

      for row in rows:
        id = row[0]
        task = row[1]
        due_date = row[2].strftime("%Y-%m-%d")
        priority = row[3]
        completed = row[4]
        
        self.id_entry.insert(0, id)
        self.task_entry.insert(0, task)
        self.date_entry.insert(0, due_date)
        self.priority_entry.insert(0, priority)

      # Atualizar a lista
      self.refresh_list()
      
  def delete_task(self):
      # Obter a tarefa selecionada na lista
      selection = self.task_list.curselection()
      if not selection:
          return
      task = self.task_list.get(selection[0])
      task_name = task.split(": ")[1].split(" (")[0]

      # Excluir a tarefa do banco de dados
      cursor = self.conn.cursor()
      cursor.execute("DELETE FROM todo_list WHERE task_name = %s", (task_name,))
      self.conn.commit()
      cursor.close()

      # Atualizar a lista
      self.refresh_list()

root = tk.Tk()
app = TaskApp(master=root)
app.mainloop()