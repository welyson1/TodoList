# Use a imagem base do Python
FROM python:3.9

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos do código para o contêiner
COPY . /app

# Instale as dependências usando o gerenciador de pacotes pip
RUN pip install --no-cache-dir -r requirements.txt

# Defina o comando padrão para executar a aplicação
CMD ["python", "app.py"]