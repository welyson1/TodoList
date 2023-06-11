import unittest
import tkinter as tk
import psycopg2
from tkinter import messagebox

from app import TaskApp

class TestTaskApp(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(
            # Coloque as credenciais do banco de dados postgres aqui
            host="db.dfmqkzxfikspeqlukshk.supabase.co",
            database="postgres",
            user="postgres",
            password="SYt5A0lRZ7d9LgCV"
        )

        # Criar a tabela para os testes
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS test_todo_list (id SERIAL PRIMARY KEY, task_name VARCHAR(255) NOT NULL, due_date DATE, priority INT, completed BOOLEAN DEFAULT false)")
        self.conn.commit()
        cursor.close()

        root = tk.Tk()
        self.app = TaskApp(master=root)
        self.app.pack()

    def tearDown(self):
        # Excluir os registros após cada teste
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM test_todo_list")
        self.conn.commit()
        cursor.close()
        self.conn.close()
        self.app.destroy()

    def test_add_task(self):
        # Adicionar uma tarefa de teste
        self.app.task_entry.insert(0, "Tarefa de Teste")
        self.app.date_entry.insert(0, "2023-06-10")
        self.app.priority_entry.insert(0, "1")
        self.app.add_task()

        # Verificar se a tarefa foi adicionada corretamente
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM test_todo_list")
        rows = cursor.fetchall()
        cursor.close()

        self.assertEqual(cursor.rowcount, 1)

    def test_delete_task(self):
        # Adicionar uma tarefa de teste
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO test_todo_list (task_name, due_date, priority) VALUES ('Tarefa de Teste', '2023-06-10', 1)")
        self.conn.commit()
        cursor.close()

        # Excluir a tarefa de teste
        self.app.task_list.select_set(0)
        self.app.delete_task()

        # Verificar se a tarefa foi excluída corretamente
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM test_todo_list")
        rows = cursor.fetchall()
        cursor.close()

        self.assertEqual(cursor.rowcount, 0)

    def test_edit_task(self):
        # Adicionar uma tarefa de teste
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO test_todo_list (task_name, due_date, priority) VALUES ('Tarefa de Teste', '2023-06-10', 1)")
        self.conn.commit()
        cursor.close()

        # Editar a tarefa de teste
        self.app.task_list.select_set(0)
        self.app.edit_task()
        self.app.date_entry.delete(0, tk.END)
        self.app.date_entry.insert(0, "2023-06-20")
        self.app.add_task()

        # Verificar se a tarefa foi editada corretamente
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM test_todo_list")
        rows = cursor.fetchall()
        cursor.close()

        self.assertIn("2023-06-20", rows[0][2])

if __name__ == '__main__':
    unittest.main()
