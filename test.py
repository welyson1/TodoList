import unittest
import psycopg2
import tkinter as tk
from unittest.mock import patch
from tkinter import messagebox
from tkinter import END

from app import TaskApp

class TestTaskApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configurar conexão com o banco de dados de teste
        cls.conn = psycopg2.connect(
            host="db.dfmqkzxfikspeqlukshk.supabase.co",
            database="postgres",
            user="postgres",
            password="SYt5A0lRZ7d9LgCV"
        )
        cls.cursor = cls.conn.cursor()

    @classmethod
    def setUp(self):
        # Configurar aplicação de teste
        self.root = tk.Tk()
        self.app = TaskApp(master=self.root)
        self.app.conn = self.conn
        self.app.cursor = self.cursor

    def tearDown(self):
        # Limpar campos de entrada
        self.app.id_entry.delete(0, END)
        self.app.task_entry.delete(0, END)
        self.app.date_entry.delete(0, END)
        self.app.priority_entry.delete(0, END)
        self.app.task_list.delete(0, END)

    def test_add_task(self):
        # Simular entrada de dados
        self.app.task_entry.insert(0, "Test Task")
        self.app.date_entry.insert(0, "2023-06-11")
        self.app.priority_entry.insert(0, "3")

        # Simular clique no botão Adicionar Tarefa
        with patch.object(messagebox, "showinfo") as mock_showinfo:
            self.app.add_task()

        # Verificar se a tarefa foi adicionada à lista
        self.assertEqual(self.app.task_list.size(), 1)
        self.assertEqual(self.app.task_list.get(0), "(3) 2023-06-11: Test Task")

        # Verificar se a tarefa foi adicionada ao banco de dados
        self.cursor.execute("SELECT * FROM todo_list")
        rows = self.cursor.fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "Test Task")
        self.assertEqual(rows[0][2].strftime("%Y-%m-%d"), "2023-06-11")
        self.assertEqual(rows[0][3], 3)

        # Verificar se a caixa de entrada foi limpa
        self.assertEqual(self.app.task_entry.get(), "")
        self.assertEqual(self.app.date_entry.get(), "")
        self.assertEqual(self.app.priority_entry.get(), "")        

    def test_edit_task(self):
        # Inserir tarefa de teste no banco de dados
        self.cursor.execute("INSERT INTO todo_list (task_name, due_date, priority) VALUES (%s, %s, %s)",
            ("Test Task", "2023-06-11", 3))
        self.conn.commit()

        # Selecionar tarefa de teste na lista
        self.app.task_list.insert(0, "(3) 2023-06-11: Test Task")
        self.app.task_list.selection_set(0)

        # Simular clique no botão Editar Tarefa
        self.app.edit_task()

        # Verificar se os campos de entrada foram preenchidos corretamente        
        self.assertEqual(self.app.task_entry.get(), "Test Task")
        self.assertEqual(self.app.date_entry.get(), "2023-06-11")
        self.assertEqual(self.app.priority_entry.get(), "3")

    def test_delete_task(self):
        # Inserir tarefa de teste no banco de dados
        self.cursor.execute("INSERT INTO todo_list (task_name, due_date, priority) VALUES (%s, %s, %s)",
            ("Test Task", "2023-06-11", 3))
        self.conn.commit()

        # Selecionar tarefa de teste na lista
        self.app.task_list.insert(0, "(3) 2023-06-11: Test Task")
        self.app.task_list.selection_set(0)

        # Simular clique no botão Apagar Tarefa
        self.app.delete_task()

        # Verificar se a tarefa foi removida da lista
        self.assertEqual(self.app.task_list.size(), 0)

        # Verificar se a tarefa foi removida do banco de dados
        self.cursor.execute("SELECT * FROM todo_list")
        rows = self.cursor.fetchall()
        self.assertEqual(len(rows), 0)

if __name__ == "__main__":
    unittest.main()
