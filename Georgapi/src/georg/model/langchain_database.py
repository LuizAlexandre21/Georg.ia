# Biblioteca
from langchain.llms import Ollama
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from typing import List
from src.georg.utils.LLMClass import LLMparams
from langchain.memory import ConversationBufferMemory

# Criando a classe do modelo de linguagem natural 
class LLMdatabase:
    
    """ Classe para instanciar o modelo neural de linguagem para interpretação de dados d"""
    def __init__(self,args:LLMparams):
        self._db_uri = args['db_uri']
        self._tables = args['tables']
        self._schema = args['schema']
        self._model = args['model']
        self._model_url = args['model_url']


    @property
    def db_uri(self) -> str:
        """Retorna a URI do banco de dados"""
        return self._db_uri 


    @property
    def tables(self)-> str:
        """Retorna as tabelas utilizadas""" 
        return self._tables 


    @property 
    def model_url(self)->str:
        """Retorna a url do servidor da url"""    
        return self._model_url


    @property 
    def model(self)->str:
        """Retorna o modelo para ser utilizado"""
        return self._model 
    

    @tables.setter
    def tables(self,new_tables:List[str]):
        """Permite atualizar a lista de tabelas"""
        if not isinstance(new_tables,list):
            raise ValueError("A lista de tabelas devem ser do tipo list[str]")
        self._tables = new_tables 


    def database_conn(self):
        """ Connection into database with langchain toolkit """
        try:
            return SQLDatabase.from_uri(
                self._db_uri, 
                include_tables=self._tables, 
                schema=self._schema)
        except Exception as e:
            raise ConnectionError(f"Falha ao conectar ao banco de dados:{e}")
    
    def llm_agent(self):
        """Configura o agente com memória conversacional."""
        llm = Ollama(
            model=self._model,
            base_url=self._model_url,
            temperature=0.2
        )
        db = self.database_conn()  # Supondo que esse método conecta ao seu banco de dados
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Cria o agente com o tratamento de erro de parsing ativado
        agent = create_sql_agent(
            llm=llm, 
            toolkit=toolkit, 
            verbose=True, 
            memory=memory, 
            handle_parsing_errors=True
        )
        
        return agent, memory