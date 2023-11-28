# Documentação Técnica: Aplicativo de Lista de Tarefas

## Visão Geral

O aplicativo de Lista de Tarefas é uma interface gráfica de usuário (GUI) desenvolvida em Python utilizando Tkinter e PostgreSQL do Supabase. O Supabase fornece um sistema de gerenciamento de banco de dados PostgreSQL totalmente gerenciado, trazendo facilidade de uso e recursos avançados para a aplicação. Este aplicativo permite aos usuários adicionar, visualizar, editar e excluir tarefas de uma lista. Cada tarefa possui atributos como nome, data de vencimento, prioridade e status de conclusão (este último ainda não implementado).

## Captura de tela da interface
![Texto alternativo](https://raw.githubusercontent.com/welyson1/TodoList/projeto-arquitetura-software/img/Telav2.png)

## Bibliotecas

- `tkinter`: Biblioteca padrão do Python para criar interfaces gráficas.
- `psycopg2`: Biblioteca para interagir com bancos de dados PostgreSQL.
- `messagebox`: Parte do módulo `tkinter` para exibir caixas de diálogo de mensagem.

## Requisitos
### Requisitos Funcionais

1. **Gerenciamento de Tarefas**: A aplicação deve permitir que os usuários adicionem, editem, e excluam tarefas.
2. **Armazenamento de Dados**: As tarefas, juntamente com detalhes como nome da tarefa, data de vencimento, prioridade e status de conclusão, devem ser armazenadas em um banco de dados.
3. **Listagem de Tarefas**: A aplicação deve exibir uma lista das tarefas existentes, ordenadas por prioridade.
4. **Atualização de Tarefas**: A aplicação deve permitir a edição de tarefas existentes, incluindo a alteração do nome da tarefa, data de vencimento e prioridade.
5. **Remoção de Tarefas**: A aplicação deve permitir a exclusão de tarefas da lista e do banco de dados.
6. **Visualização de Detalhes da Tarefa**: Ao clicar em uma tarefa, a aplicação deve mostrar os detalhes completos da tarefa, como prioridade, data de vencimento e descrição.
7. **Interface Gráfica do Usuário**: A aplicação deve oferecer uma interface gráfica para interação com o usuário, utilizando a biblioteca Tkinter.

### Requisitos Não Funcionais

1. **Usabilidade**: A interface gráfica deve ser intuitiva e fácil de usar.
2. **Desempenho**: A aplicação deve responder rapidamente às entradas do usuário e atualizar a lista de tarefas sem atrasos significativos.
3. **Segurança**: A aplicação deve proteger informações sensíveis, como detalhes de conexão ao banco de dados. (Nota: o código atual contém credenciais expostas, o que é uma prática insegura.)
4. **Confiabilidade**: A aplicação deve ser capaz de gerenciar os dados de forma consistente, evitando perdas ou corrupção de dados.
5. **Compatibilidade**: A aplicação deve ser compatível com diferentes versões do sistema operacional onde será executada.
6. **Manutenibilidade**: O código deve ser bem organizado e documentado para facilitar atualizações e manutenção futura.
7. **Portabilidade**: A aplicação deve ser facilmente transferível para diferentes ambientes de execução sem a necessidade de extensas reconfigurações.

## Estrutura da Tabela do bando de dados

```sql
CREATE TABLE todo_list (
  id SERIAL PRIMARY KEY,
  task_name VARCHAR(255) NOT NULL,
  due_date DATE,
  priority INT,
  completed BOOLEAN DEFAULT false
);
```
## Arquivos do projeto

### Dockerfile
O `Dockerfile` é um script de configuração usado para criar uma imagem Docker para o aplicativo de Lista de Tarefas. Ele especifica o ambiente operacional, as dependências necessárias e os comandos para executar o aplicativo.

### requirements.txt
O `requirements.txt` lista todas as dependências Python necessárias para executar o aplicativo. Este arquivo é crucial para gerenciar e instalar as bibliotecas necessárias de maneira consistente e automatizada.

### Integração com Dockerfile
- O Dockerfile usa o `requirements.txt` na etapa `RUN pip install --no-cache-dir -r requirements.txt` para instalar todas as dependências necessárias dentro do contêiner Docker.

### app.py
O arquivo `app.py` contém o código-fonte do aplicativo de Lista de Tarefas. Ele utiliza as bibliotecas tkinter para a interface gráfica e psycopg2 para interagir com um banco de dados PostgreSQL hospedado no Supabase. 

#### Classe `TaskApp`

#### Métodos

- `__init__(self, master=None)`: Inicializa a aplicação, cria a conexão com o banco de dados e os widgets.
- `create_widgets(self)`: Cria e posiciona os widgets na janela.
- `show_task_info(self, event)`: Mostra informações detalhadas da tarefa selecionada.
- `refresh_list(self)`: Atualiza a lista de tarefas.
- `add_task(self)`: Adiciona uma nova tarefa ao banco de dados ou atualiza uma tarefa existente.
- `edit_task(self)`: Prepara a edição de uma tarefa selecionada.
- `delete_task(self)`: Deleta a tarefa selecionada do banco de dados.

#### Atributos

- `master`: Janela principal do Tkinter.
- `conn`: Conexão com o banco de dados PostgreSQL.
- `cursor`: Cursor para execução de comandos SQL.
- Widgets diversos (ex.: `task_label`, `task_entry`, `add_button`).

#### Função `run_app()`

Inicia a aplicação criando uma instância de `TaskApp` e entra no loop principal do Tkinter.

## Diagramas

### Diagrama de Atividade
```mermaid
flowchart TD
    A[Iniciar Aplicação] --> B[Interface Gráfica]
    B --> C[Conexão com Banco de Dados]
    C --> D[Atualizar Lista de Tarefas]
    D --> E{Ações do Usuário}
    E -->|Adicionar| F[Adicionar Tarefa]
    E -->|Editar| G[Editar Tarefa]
    E -->|Apagar| H[Apagar Tarefa]
    E -->|Selecionar| I[Exibir Informações]
    F --> D
    G --> D
    H --> D
    I --> E
```
---
### Diagrama de Máquina de Estados

```mermaid
stateDiagram-v2
    [*] --> Inicialização
    Inicialização --> InterfacePronta: Interface Gráfica Criada
    InterfacePronta --> ConexãoBD: Conectar ao Banco de Dados
    ConexãoBD --> ListaAtualizada: Atualizar Lista
    ListaAtualizada --> EsperaAção
    EsperaAção --> AdicionarTarefa: Adicionar Tarefa
    EsperaAção --> EditarTarefa: Editar Tarefa
    EsperaAção --> ApagarTarefa: Apagar Tarefa
    EsperaAção --> ExibirInfo: Selecionar Tarefa
    AdicionarTarefa --> ListaAtualizada
    EditarTarefa --> ListaAtualizada
    ApagarTarefa --> ListaAtualizada
    ExibirInfo --> EsperaAção
    ListaAtualizada --> EsperaAção
    ConexãoBD --> FalhaConexão: Falha
    FalhaConexão --> [*]
    EsperaAção --> [*]: Fechar Aplicação
```
---
### Diagrama de Sequência

```mermaid
sequenceDiagram
    participant U as Usuário
    participant A as Aplicação
    participant DB as Banco de Dados
    U->>A: Inicia Aplicação
    A->>DB: Conecta ao Banco de Dados
    loop Atualização de Tarefas
        A->>DB: Solicita tarefas
        DB-->>A: Retorna tarefas
        A-->>U: Exibe tarefas
    end
    U->>A: Adiciona/Modifica/Deleta tarefa
    A->>DB: Atualiza Banco de Dados
    DB-->>A: Confirmação
    A-->>U: Atualiza interface
    Note over U,A: Interações do Usuário
    Note over A,DB: Comunicação com Banco de Dados
```
---
### Diagrama de Caso de Uso
```mermaid
graph LR
    A[Usuário] -->|Adicionar Tarefa| B((TaskApp))
    A -->|Editar Tarefa| B
    A -->|Apagar Tarefa| B
    A -->|Visualizar Tarefa| B
    A -->|Atualizar Lista| B
    B -->|Conectar ao Banco de Dados| C[Suprabase PostgreSQL]
    B -->|Inserir Tarefa| C
    B -->|Atualizar Tarefa| C
    B -->|Excluir Tarefa| C
    B -->|Selecionar Tarefas| C
```  

# Instruções de Uso

1. **Iniciar a Aplicação**: Execute o script Python para iniciar a aplicação.
2. **Configuração do Banco de Dados**: Certifique-se de configurar corretamente as credenciais de acesso ao PostgreSQL do Supabase no código. Recomenda-se o uso de variáveis de ambiente ou arquivos de configuração para armazenar informações sensíveis.
3. **Adicionar Tarefa**: Preencha os campos de tarefa, data de vencimento e prioridade. Clique em "Adicionar Tarefa".
4. **Visualizar Tarefas**: As tarefas são exibidas na lista principal.
5. **Editar Tarefa**: Selecione uma tarefa e clique em "Editar Tarefa". Modifique os campos desejados e clique em "Salvar alteração".
6. **Excluir Tarefa**: Selecione uma tarefa e clique em "Apagar Tarefa".
7. **Informações da Tarefa**: Dê um duplo clique em uma tarefa para ver detalhes.

# Arquitetura em Camadas

## Processos Referentes à Arquitetura em Camadas

A arquitetura em camadas é um modelo de design que ajuda a separar as responsabilidades e funcionalidades de um aplicativo em diferentes níveis ou "camadas". Para o aplicativo de Lista de Tarefas desenvolvido com Tkinter e PostgreSQL do Supabase, podemos definir a seguinte estrutura de arquitetura em camadas:

## 1. Camada de Apresentação (Front-End)

### Responsabilidades:

- **Interface Gráfica do Usuário (GUI)**: Desenvolver e manter a interface com a qual o usuário interage. Inclui a criação de janelas, botões, campos de entrada de texto, listas e outros elementos gráficos.
- **Interatividade**: Gerenciar a interação do usuário com a interface, como cliques em botões, entradas de texto e seleção de itens da lista.
- **Exibição de Dados**: Mostrar informações ao usuário, como a lista de tarefas, detalhes da tarefa e mensagens de erro ou sucesso.

### Tecnologias Utilizadas:

- Tkinter para a construção da interface gráfica.

## 2. Camada de Lógica de Negócios (Back-End)

### Responsabilidades:

- **Processamento de Dados**: Implementar a lógica necessária para processar as ações do usuário, como adicionar, editar, excluir e visualizar tarefas.
- **Validação**: Verificar a validade dos dados fornecidos pelo usuário antes de enviá-los para a camada de dados.
- **Manipulação de Estados**: Gerenciar o estado das tarefas (por exemplo, concluído ou não concluído).

### Tecnologias Utilizadas:

- Python para a implementação da lógica de negócios.

## 3. Camada de Dados (Banco de Dados)

### Responsabilidades:

- **Persistência de Dados**: Armazenar e recuperar dados relacionados às tarefas, como nome, data de vencimento, prioridade e status.
- **Gerenciamento de Banco de Dados**: Criar, ler, atualizar e deletar registros no banco de dados (CRUD).
- **Segurança de Dados**: Garantir a segurança dos dados, protegendo-os contra acesso não autorizado ou corrupção.

### Tecnologias Utilizadas:

- **Supabase (PostgreSQL)**: Utilizado como sistema de gerenciamento de banco de dados. O Supabase fornece uma plataforma de banco de dados PostgreSQL completa, oferecendo recursos avançados e uma interface amigável para facilitar o desenvolvimento e gerenciamento de dados.

## Processos de Integração entre as Camadas

1. **Comunicação entre Camada de Apresentação e Lógica de Negócios**: Quando o usuário realiza uma ação na GUI (por exemplo, adiciona uma nova tarefa), a camada de apresentação envia esses dados para a camada de lógica de negócios.

2. **Processamento na Camada de Lógica de Negócios**: A lógica de negócios processa a solicitação (validando dados, aplicando regras de negócio) e interage com a camada de dados para persistir ou recuperar informações.

3. **Operações na Camada de Dados**: A camada de dados executa as operações de banco de dados necessárias e retorna os resultados para a camada de lógica de negócios.

4. **Resposta à Camada de Apresentação**: A camada de lógica de negócios envia os resultados de volta para a camada de apresentação, que atualiza a GUI de acordo.

### Camada de Interface Gráfica

Esta camada é responsável por toda a interação com o usuário, utilizando a biblioteca `tkinter`. Os elementos gráficos, como rótulos, caixas de entrada e botões, são definidos nesta camada.

#### Recursos:
- Labels (rótulos) para exibição de informações.
- Entry (caixas de entrada) para entrada de dados.
- Buttons (botões) para acionar ações.
- Listbox para exibição da lista de tarefas.

#### Principais Processos:
- **create_widgets():** Criação dos elementos gráficos.
- **show_task_info(event):** Exibe informações detalhadas de uma tarefa selecionada.
- **refresh_list():** Atualiza a lista de tarefas na interface.

### Camada de Lógica de Negócios

Nesta camada, estão as funções relacionadas à lógica da aplicação, como adicionar, editar, excluir e visualizar tarefas. Além disso, há a lógica para limpar campos de entrada, obter dados do banco de dados e atualizar a lista de tarefas.

#### Recursos:
- Funções para adicionar, editar, excluir e visualizar tarefas.
- Funções auxiliares para limpar campos de entrada e obter dados do banco de dados.

#### Principais Processos:
- **add_task():** Adiciona uma nova tarefa ou edita uma existente.
- **edit_task():** Permite a edição de uma tarefa existente.
- **delete_task():** Exclui uma tarefa selecionada.

### Camada de Acesso ao Banco de Dados

Nesta camada, ocorre a interação com o banco de dados PostgreSQL do Supabase usando a biblioteca `psycopg2`. São realizadas operações como inserção, atualização, exclusão e consulta de dados.

#### Recursos:
- Conexão com o banco de dados.
- Execução de consultas SQL.

#### Principais Processos:
- **refresh_list():** Obtém a lista de tarefas do banco de dados e atualiza a interface.
- **add_task():** Adiciona ou atualiza uma tarefa no banco de dados.
- **edit_task():** Obtém os dados de uma tarefa do banco de dados para edição.
- **delete_task():** Exclui uma tarefa do banco de dados.


# Estratégias para Escalabilidade e Refatoração

## Escalabilidade

A escalabilidade de um aplicativo refere-se à sua capacidade de lidar com o crescimento, seja em termos de volume de dados, número de usuários ou complexidade das operações. Para o aplicativo de Lista de Tarefas, várias estratégias podem ser adotadas:

1. **Uso de ORM (Object-Relational Mapping)**: Introduzir um ORM, como SQLAlchemy para Python, pode simplificar a interação com o banco de dados e tornar o código mais adaptável a mudanças.

    Integrar SQLAlchemy ao código pode simplificar a interação com o banco de dados, fornecendo uma camada de abstração e facilitando operações CRUD (Create, Read, Update, Delete). Abaixo está um exemplo simplificado de como modificar o código para usar SQLAlchemy.

    1. **Instale a biblioteca SQLAlchemy:**
      ```bash
      pip install sqlalchemy
      ```

    2. **Criação do Modelo com SQLAlchemy:**
      ```python
      from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean
      from sqlalchemy.ext.declarative import declarative_base
      from sqlalchemy.orm import sessionmaker

      Base = declarative_base()

      class Task(Base):
          __tablename__ = 'todo_list'

          id = Column(Integer, primary_key=True)
          task_name = Column(String(255), nullable=False)
          due_date = Column(Date)
          priority = Column(Integer)
          completed = Column(Boolean, default=False)
      ```

    3. **Conexão com o Banco de Dados:**
      ```python
      engine = create_engine('postgresql://postgres:p3lYGX5VAtixx9qS@db.yathucylvsjqreyzmqlf.supabase.co/postgres')
      Base.metadata.create_all(engine)
      Session = sessionmaker(bind=engine)
      ```

    4. **Atualização das Funções de Manipulação de Dados:**
      ```python
      class TaskController:
          def __init__(self, master):
              self.session = Session()
              self.view = TaskView(master)
              self.view.add_button.config(command=self.add_task)
              self.view.edit_button.config(command=self.edit_task)
              self.view.delete_button.config(command=self.delete_task)
              self.view.save_button.config(command=self.add_task)
              self.view.task_list.bind("<Double-Button-1>", self.view.show_task_info)
              self.view.refresh_list()

          def add_task(self):
              task = Task(task_name=self.view.task_entry.get(),
                          due_date=self.view.date_entry.get(),
                          priority=int(self.view.priority_entry.get()))
              self.session.add(task)
              self.session.commit()
              self.view.refresh_list()

          def edit_task(self):
              # Obter a tarefa selecionada na lista
              selection = self.view.task_list.curselection()
              if not selection:
                  return

              task = self.view.task_list.get(selection[0])
              task_name = task.split(": ")[1].split(" (")[0]

              # Buscar a tarefa no banco de dados
              task = self.session.query(Task).filter_by(task_name=task_name).first()

              # Atualizar os dados
              task.task_name = self.view.task_entry.get()
              task.due_date = self.view.date_entry.get()
              task.priority = int(self.view.priority_entry.get())

              self.session.commit()
              self.view.refresh_list()

          def delete_task(self):
              # Obter a tarefa selecionada na lista
              selection = self.view.task_list.curselection()
              if not selection:
                  return

              task = self.view.task_list.get(selection[0])
              task_name = task.split(": ")[1].split(" (")[0]

              # Buscar e excluir a tarefa no banco de dados
              task = self.session.query(Task).filter_by(task_name=task_name).first()
              self.session.delete(task)
              self.session.commit()

              # Atualizar a lista
              self.view.refresh_list()
      ```

2. **Serviços de Cache**: Implementar caching para reduzir o tempo de resposta e a carga sobre o banco de dados, especialmente para operações de leitura frequentes.

    Pode ser implementado caching para reduzir a carga sobre o banco de dados, especialmente para operações de leitura frequentes. Uma abordagem simples usando a biblioteca `functools.lru_cache` do Python. Esta biblioteca oferece caching de funções com uma política "Least Recently Used" (LRU).

    ```python
    from functools import lru_cache

    class TaskModel:
        def __init__(self, conn):
            self.conn = conn

        @lru_cache(maxsize=None)  # None significa um cache ilimitado
        def fetch_tasks(self):
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM todo_list ORDER BY priority DESC")
            rows = cursor.fetchall()
            cursor.close()
            return rows
    ```

    Nesse exemplo, a função `fetch_tasks` foi decorada com `@lru_cache`. Isso significa que os resultados dessa função serão armazenados em cache e reutilizados quando a mesma entrada de parâmetro for fornecida novamente. Isso é útil se as tarefas não mudarem frequentemente e a lista é solicitada repetidamente.

    Além disso, é importante mencionar que o caching pode ser útil para outras funções que realizam leituras frequentes no banco de dados, dependendo dos padrões de acesso do aplicativo. No entanto, é necessário ter cuidado para invalidar o cache quando os dados no banco de dados são modificados (por exemplo, ao adicionar, editar ou excluir tarefas).

    Implementar caching pode melhorar significativamente o desempenho, especialmente em operações de leitura que não mudam com frequência.

3. **Escalabilidade Horizontal do Banco de Dados**: Preparar o banco de dados para ser escalável horizontalmente (por exemplo, usando sharding ou replicação) para lidar com um aumento no volume de dados.

    Para preparar o banco de dados para escalabilidade horizontal, é importante considerar algumas sugestões. No caso do PostgreSQL algumas abordagens incluem:

    **Replicação:**
      - Configurar replicação para criar cópias dos dados em servidores adicionais.
      - Utilizar replicação síncrona ou assíncrona, dependendo dos requisitos de consistência.

      Exemplo:
      ```sql
      -- Configuração para replicação assíncrona
      replica = replication
      replica_sync_method = async
      ```

    **Particionamento (Sharding):**
      - Dividir a tabela `todo_list` em partições (shards) distribuídas em diferentes servidores.
      - Utilizar uma estratégia de particionamento que faça sentido para a aplicação, como por data, ID, ou outra chave distinta.

      Exemplo:
      ```sql
      -- Criar uma tabela particionada por data
      CREATE TABLE todo_list (
          id SERIAL PRIMARY KEY,
          task_name VARCHAR(255) NOT NULL,
          due_date DATE,
          priority INT,
          completed BOOLEAN DEFAULT false
      ) PARTITION BY RANGE (due_date);
      ```

    **Balanceamento de Carga:**
      - Utilizar um sistema de balanceamento de carga para distribuir as consultas entre os servidores de banco de dados.

      Exemplo:
      ```python
      # Configuração básica de balanceamento de carga
      pgpool_host = "load_balancer_ip"
      pgpool_port = "5432"
      ```

    **Índices Adequados:**
      - Garantir que os índices sejam otimizados para o ambiente distribuído.
      - Utilizar índices locais sempre que possível para reduzir a sobrecarga de consultas distribuídas.

      Exemplo:
      ```sql
      -- Criar um índice local na coluna priority
      CREATE INDEX idx_priority ON todo_list (priority) LOCAL;
      ```

    **Configuração de Conexão:**
      - Configurar a aplicação para se conectar a um pool de conexões gerenciado, que pode escalar horizontalmente com o número de servidores de banco de dados.

      Exemplo:
      ```python
      # Configuração para conexão a um pool de conexões
      connection_pool = get_connection_pool()
      ```

4. **Adoção de Microserviços**: Se a aplicação se tornar muito grande, considerar a arquitetura de microserviços, onde diferentes funcionalidades são geridas por serviços independentes.

    A arquitetura de microserviços envolve dividir uma aplicação monolítica em serviços independentes, cada um responsável por uma funcionalidade específica. Isso proporciona maior escalabilidade e facilidade de manutenção. Abaixo estão algumas sugestões simplificadas:

    **Divisão em Microserviços:**
      - **Monolítico (`app.py`):**
        - Toda a lógica, interface gráfica e interações com o banco de dados estão no mesmo arquivo.
      - **Microserviços:**
        - Crie serviços independentes para funcionalidades distintas, como o serviço de tarefas, serviço de autenticação, etc.

    **Exemplo Simplificado (considerando apenas Tarefas):**
      - **Monolítico (`app.py`):**
        - Todo o código está no mesmo arquivo, misturando a lógica da interface gráfica e interações com o banco de dados.
      - **Microserviços:**
        - Crie um serviço para a lógica das tarefas (`tasks_service.py`), um para a interface gráfica (`ui_service.py`), e outro para interações com o banco de dados (`db_service.py`).

    **Comunicação entre Serviços:**
      - **Monolítico (`app.py`):**
        - Tudo é tratado no mesmo lugar.
      - **Microserviços:**
        - O serviço de interface gráfica pode fazer chamadas ao serviço de tarefas para obter informações sobre tarefas, e o serviço de tarefas pode interagir com o serviço de banco de dados para persistência.


## Refatoração

Refatoração é o processo de reestruturar o código existente sem alterar seu comportamento externo, com o objetivo de melhorar a legibilidade, reduzir a complexidade e facilitar a manutenção.

1. **Padrões de Projeto**: Adotar padrões de projeto como MVC (Model-View-Controller) para melhor separação entre a lógica de negócios, a interface do usuário e a interação com o banco de dados.

    Uma possível implementação do padrão MVC seria criar três módulos separados para Model, View e Controller.

    - **Model (`model.py`):**
      ```python
      import psycopg2

      class TaskModel:
          def __init__(self, conn):
              self.conn = conn

          def fetch_tasks(self):
              cursor = self.conn.cursor()
              cursor.execute("SELECT * FROM todo_list ORDER BY priority DESC")
              rows = cursor.fetchall()
              cursor.close()
              return rows

          def add_task(self, task, date, priority):
              cursor = self.conn.cursor()
              cursor.execute("INSERT INTO todo_list (task_name, due_date, priority) VALUES (%s, %s, %s)", (task, date, priority))
              self.conn.commit()
              cursor.close()

          # Adicionar métodos para editar e excluir tarefas

      ```

    - **View (`view.py`):**
      ```python
      import tkinter as tk
      from tkinter import messagebox

      class TaskView(tk.Frame):
          def __init__(self, master=None):
              super().__init__(master)
              self.master = master
              self.pack()
              # ... restante do código para criação de widgets

          def show_task_info(self, event):
              # ... restante do código para exibir informações da tarefa

          def refresh_list(self):
              # ... restante do código para atualizar a lista
      ```

    - **Controller (`controller.py`):**
      ```python
      from model import TaskModel
      from view import TaskView

      class TaskController:
          def __init__(self, master, conn):
              self.model = TaskModel(conn)
              self.view = TaskView(master)
              self.view.add_button.config(command=self.add_task)
              self.view.edit_button.config(command=self.edit_task)
              self.view.delete_button.config(command=self.delete_task)
              self.view.save_button.config(command=self.add_task)
              self.view.task_list.bind("<Double-Button-1>", self.view.show_task_info)
              self.view.refresh_list()

          def add_task(self):
              # ... restante do código para adicionar tarefa

          def edit_task(self):
              # ... restante do código para editar tarefa

          def delete_task(self):
              # ... restante do código para excluir tarefa
      ```

2. **Otimização de Consultas SQL**: Revisar e otimizar as consultas SQL para melhorar a performance com o banco de dados. Abaixo algumas sugestões simples:

    **Selecionar Apenas as Colunas Necessárias:**
      - Em vez de usar `SELECT *`, especifique apenas as colunas necessárias. Isso reduz a quantidade de dados transferidos do banco de dados para a aplicação.

      Exemplo:
      ```python
      cursor.execute("SELECT task_name, due_date, priority, completed FROM todo_list ORDER BY priority DESC")
      ```

    **Utilizar Índices:**
      - Certifique-se de que as colunas usadas em cláusulas WHERE e ORDER BY têm índices. Isso acelera as operações de consulta.

      Exemplo (para uma coluna `priority`):
      ```sql
      CREATE INDEX idx_priority ON todo_list (priority);
      ```

    **Evitar Subconsultas Desnecessárias:**
      - Evite subconsultas sempre que possível. Elas podem impactar negativamente o desempenho. Em vez disso, use joins ou estratégias mais eficientes.

      Exemplo (evitar subconsulta):
      ```sql
      -- Evite subconsulta
      SELECT * FROM todo_list WHERE priority = (SELECT MAX(priority) FROM todo_list);

      -- Use JOIN ou outra estratégia
      SELECT t1.* FROM todo_list t1 JOIN (SELECT MAX(priority) AS max_priority FROM todo_list) t2 ON t1.priority = t2.max_priority;
      ```

    **Limitar o Número de Linhas Retornadas:**
      - Se você não precisa de todas as linhas, use a cláusula `LIMIT` para limitar o número de resultados.

      Exemplo:
      ```python
      cursor.execute("SELECT * FROM todo_list ORDER BY priority DESC LIMIT 10")
      ```

    **Cache de Consultas Frequentes:**
      - Se certas consultas são executadas frequentemente e os resultados não mudam com frequência, considere usar algum tipo de cache para armazenar os resultados e evitar consultas repetitivas.


3. **Uso de Funções e Métodos Genéricos**: Substituir código duplicado por funções ou métodos genéricos para reduzir a redundância e facilitar futuras alterações.

    Podemos identificar uma oportunidade de criar uma função genérica para a execução de consultas no banco de dados. Atualmente, há duplicação de código na execução de consultas em diferentes partes do script.

    **Exemplo de Implementação:**

    **Criar uma Função Genérica para Consultas SQL:**

    ```python
    import psycopg2

    def execute_query(conn, query, *args):
        cursor = conn.cursor()
        cursor.execute(query, args)
        result = cursor.fetchall()
        cursor.close()
        return result
    ```

    Essa função `execute_query` recebe a conexão `conn`, a consulta SQL `query` e quaisquer parâmetros necessários para a consulta. Ela executa a consulta, busca os resultados e fecha o cursor.

    **Utilizar a Função Genérica no Código:**
    ```python
    # Utilizando a função genérica
    query = "SELECT * FROM todo_list ORDER BY priority DESC"
    rows = execute_query(self.conn, query)
    ```

    Essa alteração reduz a redundância, melhora a legibilidade do código e facilita futuras alterações nas consultas.

4. **Testes Automatizados**: Implementar testes automatizados para garantir que as refatorações não quebrem funcionalidades existentes.

    No exemplo a seguir, suponha que o código tenha sofrido refatorações para separar o código em modelos (`model.py`), visualizações (`view.py`), e controladores (`controller.py`).

    Um novo arquivo chamado `test_app.py` devera ser criado para testes:

    ```python
    import unittest
    from unittest.mock import patch
    from model import TaskModel
    from view import TaskView
    from controller import TaskController

    class TestTaskApp(unittest.TestCase):
        def setUp(self):
            # Configuração inicial para o teste
            self.conn = None  # Substitua pela conexão real do banco de dados se necessário
            self.model = TaskModel(self.conn)
            self.view = TaskView()
            self.controller = TaskController(self.view, self.model)

        @patch("view.TaskView.show_task_info")
        def test_add_task(self, mock_show_task_info):
            # Configuração do teste
            task_name = "Nova Tarefa"
            date = "2023-12-31"
            priority = 3

            # Executar a ação que está sendo testada
            self.controller.add_task(task_name, date, priority)

            # Verificar se a tarefa foi adicionada
            tasks = self.model.fetch_tasks()
            added_task = tasks[0][1] if tasks else None

            self.assertIsNotNone(added_task)
            self.assertEqual(added_task, task_name)

            # Verificar se o método de exibição de informações da tarefa foi chamado
            mock_show_task_info.assert_called_once()

    if __name__ == "__main__":
        unittest.main()
    ```

    Neste exemplo, o teste `test_add_task` simula a adição de uma nova tarefa, verifica se a tarefa foi adicionada corretamente ao banco de dados e se o método de exibição de informações da tarefa foi chamado.

5. **Documentação do Código**: Melhorar a documentação interna do código para facilitar o entendimento e a manutenção por outros desenvolvedores.

    **Adição de Comentários Explicativos:**
      - **Antes:**
        ```python
        self.task_list = tk.Listbox(self, bg="lightgray", font=("Arial", 14), bd=3, relief="groove")
        ```
      - **Depois:**
        ```python
        # Lista para exibir as tarefas na interface gráfica
        self.task_list = tk.Listbox(self, bg="lightgray", font=("Arial", 14), bd=3, relief="groove")
        ```

    **Documentação de Métodos:**
      - **Antes:**
        ```python
        def refresh_list(self):
            # Código para atualizar a lista de tarefas
            self.task_list.delete(0, tk.END)
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM todo_list ORDER BY priority DESC")
            rows = cursor.fetchall()
            cursor.close()
            for row in rows:
                # Adiciona tarefas à lista
                task = row[1]
                # ...
                self.task_list.insert(tk.END, f"({priority}) {due_date}: {task}")
        ```
      - **Depois:**
        ```python
        def refresh_list(self):
            """
            Atualiza a lista de tarefas na interface gráfica.
            """
            # Limpa a lista atual
            self.task_list.delete(0, tk.END)
            
            # Obtém a lista de tarefas do banco de dados
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM todo_list ORDER BY priority DESC")
            rows = cursor.fetchall()
            cursor.close()
            
            # Adiciona tarefas à lista na interface
            for row in rows:
                task = row[1]
                due_date = row[2].strftime("%Y-%m-%d")
                priority = row[3]
                completed = row[4]
                if completed:
                    task += " (Concluída)"
                self.task_list.insert(tk.END, f"({priority}) {due_date}: {task}")
        ```

    **Esclarecimento de Parâmetros:**
      - **Antes:**
        ```python
        def add_task(self):
            id = self.id_entry.get()
            task = self.task_entry.get()
            date = self.date_entry.get()
            priority = int(self.priority_entry.get())
            ```
      - **Depois:**
        ```python
        def add_task(self):
            """
            Adiciona uma nova tarefa ao banco de dados ou atualiza uma existente.
            """
            # Obtém os dados da interface gráfica
            id = self.id_entry.get()
            task = self.task_entry.get()
            date = self.date_entry.get()
            priority = int(self.priority_entry.get())
            ```

    Abaixo exemplos de como os comentparios no código fornecem clareza sobre o propósito de variáveis, métodos e trechos de código, facilitando a compreensão e manutenção do código por outros desenvolvedores.

6. **Revisão da Interface Gráfica**: Avaliar a interface gráfica do usuário (GUI) para melhorar a usabilidade e a experiência do usuário, o que pode incluir a reorganização de elementos ou a implementação de novos componentes visuais.

    As sugestões abaixo visam melhorar a usabilidade e a estética geral da interface do usuário, proporcionando uma experiência mais agradável para o usuário final.

    **Melhoria da Experiência do Usuário (UX):**
      - Adicionar rótulos explicativos aos campos de entrada para orientar o usuário.
      - Incluir um widget de calendário para a seleção mais fácil da data de vencimento.
      - Utilizar cores ou ícones para indicar a prioridade da tarefa.

      ```python
      # Exemplo de rótulos explicativos e widget de calendário
      self.task_label = tk.Label(self.input_frame, text="Tarefa:", ...)
      self.task_label.grid(row=0, column=0, ...)

      self.date_label = tk.Label(self.input_frame, text="Data de Vencimento:", ...)
      self.date_label.grid(row=1, column=0, ...)

      self.date_entry = tk.Entry(self.input_frame, bg="lightgray", ...)
      self.date_entry.grid(row=1, column=1, ...)

      # Exemplo de uso de um widget de calendário (pode ser necessário instalar uma biblioteca externa)
      from tkcalendar import DateEntry
      self.date_calendar = DateEntry(self.input_frame, ...)
      self.date_calendar.grid(row=1, column=1, ...)
      ```

    **Botões e Feedback Visual:**
      - Alterar o estilo dos botões para tornar as ações mais visíveis.
      - Adicionar mensagens de feedback após a conclusão de uma ação.

      ```python
      # Exemplo de botões com estilos mais visíveis e mensagens de feedback
      self.add_button = tk.Button(self.input_frame, text="Adicionar Tarefa ➕", ..., relief="raised")
      self.add_button.grid(row=3, column=1, ...)

      self.delete_button = tk.Button(self.input_frame, text="Apagar Tarefa ❌", ..., relief="raised")
      self.delete_button.grid(row=3, column=0, ...)

      # Adicionar mensagens de feedback após a conclusão de uma ação
      messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
      ```

7. **Implementação da Conclusão de Tarefas**: A funcionalidade de conclusão de tarefas, embora presente no banco de dados, ainda não foi implementada na interface gráfica. Essa funcionalidade pode ser integrada permitindo que os usuários marquem as tarefas como concluídas com um duplo clique na interface do aplicativo.

    ### Modificação da Classe `TaskApp`:

    - **Método `complete_task(self, task_id)`:** Este método será responsável por atualizar o status de conclusão de uma tarefa no banco de dados. Quando o usuário realiza um duplo clique em uma tarefa, o aplicativo marca essa tarefa como concluída.
    - **Alteração no Método `refresh_list(self)`:** Deve ser modificado para refletir visualmente quais tarefas foram concluídas, talvez alterando a cor ou adicionando um ícone específico ao lado das tarefas concluídas.
    - **Integração com a Interface Gráfica:** Na função `create_widgets(self)`, vincular um evento de duplo clique para cada item na lista de tarefas. Esse evento chamará o método `complete_task`, passando o ID da tarefa como argumento.

    ### Exemplo de Implementação de `complete_task`:

    ```python
    def complete_task(self, task_id):
        try:
            self.cursor.execute("UPDATE todo_list SET completed = True WHERE id = %s", (task_id,))
            self.conn.commit()
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # Exemplo de vinculação do evento de duplo clique
    self.task_listbox.bind("<Double-1>", lambda event: self.complete_task(self.get_selected_task_id()))

    ```
    Neste exemplo, `get_selected_task_id()` seria um método auxiliar para obter o ID da tarefa selecionada, e `task_listbox` é o widget que lista as tarefas.

8. **Segurança**: O código contém credenciais de banco de dados expostas, o que é uma prática insegura. Recomenda-se o uso de variáveis de ambiente ou arquivos de configuração.

9. **Validação de Dados**: Adicionar validação para os campos de entrada para evitar dados inválidos ou incompletos.
