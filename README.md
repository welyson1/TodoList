# To-do List em Python

O projeto é uma lista de tarefas que permite ao usuário adicionar e visualizar tarefas. Ele se integra com uma API criada no Supabase, uma plataforma de desenvolvimento de aplicativos, para armazenar e gerenciar as informações das tarefas. A interface do usuário é construída com a biblioteca Tkinter do Python.

## Funcionalidades

- Adicionar tarefas
- Recuperar lista de tarefas
## Screenshots

![App Screenshot](https://raw.githubusercontent.com/welyson1/TodoList/493108bba3ba5b50f7db7abe70cd2ed95a657f24/img/Tela.png)

## Instalação bando de dados offline
Instale python3+

Clone este repositório

Instale as bibliotecas necessarias

```bash
  pip install psycopg2
```

Instale o postgreSQL e crie um banco de dados e a tabela abaixo

```SQL
  CREATE TABLE todo_list (
    id SERIAL PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    due_date DATE,
    priority INT,
    completed BOOLEAN DEFAULT false
  );
```

## Instalação bando de dados online
Crie uma conta no Supabase em https://supabase.com/

Crie um projeto

Use o SQL Editor para criar a tabela
```SQL
  CREATE TABLE todo_list (
    id SERIAL PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    due_date DATE,
    priority INT,
    completed BOOLEAN DEFAULT false
  );
```

Pegue as credenciais em Project Settings > Database

Preencha a função abaixo com as credenciais
```
self.conn = psycopg2.connect(
  # Coloque as credenciais do banco de dados postgres aqui
  host="db.dfmqkzxfikspeqlukshk.supabase.co",
  database="postgres",
  user="postgres",
  password="nfUzzkjuxmB4bXdK"
)
```
    
## License

[MIT](https://choosealicense.com/licenses/mit/)

