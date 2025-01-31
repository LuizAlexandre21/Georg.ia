# Bibliotecas 
from langchain.llms import ollama 
from model.langchain_database import LLMdatabase 
from state import State
import os
from dotenv import load_dotenv
 
# Criando a classe do modelo 
class llm_fiscal:
    load_dotenv()

    # Criando a init 
    def __init__(self):
        self.args = {
            'db_uri': os.getenv("DB_URI"),
            'model_name': os.getenv("MODEL_NAME"),
            'model_url': os.getenv("MODEL_URL"),
            'secret_key': os.getenv("SECRET_KEY"),
            'table': os.getenv("TABLE").split(',')  
        }

        self.llm_database = LLMdatabase(self.args)  

    # Criando o chatbot 
    def chatbot(self,state:State):
        return {"messages": [self.llm_database]} 