# Import python image
FROM python:3.12 

# Create aplication workdir
WORKDIR /app 

# Copy files for workdir 
COPY . /app/ 

# Install poetry 
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="/root/.local/bin:$PATH"

# Definindo o poetry no PATH e instala as dependencias
RUN /root/.local/bin/poetry install --no-root

# Expondo a porta 8000 para o django 
EXPOSE 8000

# Executando o projeto 
CMD ["/root/.local/bin/poetry","run","python","manage.py","runserver","0.0.0.0:8000"]
