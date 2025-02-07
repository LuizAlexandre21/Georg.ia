# Bibliotecas 
from typing import Annotated 
from typing_extensions import TypedDict 
from langgraph.graph import StateGraph,START,END 
from langgraph.graph.message import add_messages 

# Definindo a estrutura do chatbot 
class State(TypedDict):

    messages:Annotated[list,add_messages]

    