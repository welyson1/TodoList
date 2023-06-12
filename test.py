import datetime
import unittest
import psycopg2


class TestTaskApp(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(
            host="db.dfmqkzxfikspeqlukshk.supabase.co",
            database="postgres",
            user="postgres",
            password="SYt5A0lRZ7d9LgCV"
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("DELETE FROM todo_list")
        self.conn.commit()

    def test_add_edit_delete_task(self):
        # Adicionar uma tarefa
        self.cursor.execute(
            "INSERT INTO todo_list (task_name, due_date, priority) VALUES (%s, %s, %s)",
            ("Tarefa Teste", datetime.date(2023, 6, 15), 3)
        )
        self.conn.commit()

        # Editar a tarefa
        self.cursor.execute("SELECT id FROM todo_list WHERE task_name = %s", ("Tarefa Teste",))
        task_id = self.cursor.fetchone()[0]
        self.cursor.execute(
            "UPDATE todo_list SET task_name = %s, due_date = %s, priority = %s WHERE id = %s",
            ("Tarefa Editada", datetime.date(2023, 6, 20), 5, task_id)
        )
        self.conn.commit()

        # Verificar se a tarefa foi editada corretamente
        self.cursor.execute("SELECT task_name, due_date, priority FROM todo_list WHERE id = %s", (task_id,))
        edited_task = self.cursor.fetchone()
        edited_task_date = datetime.date(2023, 6, 20)
        self.assertEqual(edited_task, ("Tarefa Editada", edited_task_date, 5))

        # Deletar a tarefa
        self.cursor.execute("DELETE FROM todo_list WHERE id = %s", (task_id,))
        self.conn.commit()

        # Verificar se a tarefa foi excluída corretamente
        self.cursor.execute("SELECT * FROM todo_list WHERE id = %s", (task_id,))
        deleted_task = self.cursor.fetchone()
        self.assertIsNone(deleted_task)

    def tearDown(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    unittest.main()
