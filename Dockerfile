FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala as dependências necessárias do seu projeto
# (Se você tiver um requirements.txt depois, pode substituir esta linha por COPY requirements.txt . e RUN pip install -r requirements.txt)
RUN pip install --no-cache-dir grpcio grpcio-tools pydantic pyyaml

# Copia todos os arquivos do projeto atual para o diretório de trabalho no container
COPY . /app

# Expõe a porta que o servidor gRPC utiliza (conforme configurado no main.py)
EXPOSE 50051

# Comando para iniciar o servidor quando o container rodar
CMD ["python", "main.py"]