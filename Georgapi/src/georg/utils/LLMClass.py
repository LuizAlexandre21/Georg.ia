# Bibliotecas
from typing import TypedDict,List

class LLMparams(TypedDict):
    db_uri: str 
    tables: List[str]
    schema: str 
    model: str 
    model_url: str 
