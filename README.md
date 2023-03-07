# To-do List em Python

Aplicação em python com interface gráfica e banco de dados postgreSQL.



## Funcionalidades

- Adicionar tarefas
- Recuperar lista de tarefas
## Screenshots

![App Screenshot](https://raw.githubusercontent.com/welyson1/TodoList/493108bba3ba5b50f7db7abe70cd2ed95a657f24/img/Tela.png)


## Instalação
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

    
## License

[MIT](https://choosealicense.com/licenses/mit/)

