from langgraph.graph import StateGraph
from typing import TypedDict
from model.langchain_database import LLMdatabase


# Definição do estado do grafos 
class GraphState(TypedDict):
    input_text: str
    processed_text:str 
    llm_database: str

class TextProcessingGraph:
    """Classe que implementa um grafo para processamento de texto usando LangGraph."""

    def __init__(self,llm_model:LLMdatabase):

        self.graph = StateGraph(GraphState)
        self.graph.add_node("process_text",self.process_text)
        self.graph.add_node("llm_database",self.llm_database)

        # Definindo a entrada e saída do grafo 
        self.graph.set_entry_point("process_text")
        self.graph.set_finish_point("llm_integration")

        # Compilado o grafo 
        self.graph_executor = self.graph.compile()
        # Instanciando o LLM
        self.llm_model = llm_model


    def process_text(self, state:GraphState) -> GraphState:
        """Processa o texto (exemplo: converte para maiúsculas)."""
        input_text = state["input_text"]
        processed_text = input_text.upper()
        return {"processed_text":processed_text}
    

    def llm_database(self,state:GraphState):
        processed_text = state["processed_text"]
        llm_response = self.llm_model.llm_agent(processed_text)
        return {"llm_response":llm_response}
    
    def run(self,input_text:str) ->dict:
        """Executa o grafo com o texto de entrada."""
        result = self.graph_executor.invoke({"input_text":input_text})
        return result 