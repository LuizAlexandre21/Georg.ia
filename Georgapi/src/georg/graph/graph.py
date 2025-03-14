from langgraph.graph import StateGraph
from src.georg.model.langchain_database import LLMdatabase
from src.georg.graph.node import GraphState
from typing import TypedDict, Optional


# Definição do estado do grafo
class GraphState(TypedDict):
    input_text: str
    processed_text: Optional[str]  # Pode ser None inicialmente
    llm_response: Optional[str]  # Pode ser None inicialmente


class TextProcessingGraph:
    """Classe que implementa um grafo para processamento de texto usando LangGraph."""

    def __init__(self, llm_model: LLMdatabase):
        self.graph = StateGraph(GraphState)

        # Adicionando os nós corretamente
        self.graph.add_node("process_text", self.process_text)
        self.graph.add_node("llm_database", self.query_llm)
        self.graph.add_node("chatbot",self.chatbot)

        # Conectando os nós (sem ciclos!)
        self.graph.add_edge("process_text", "llm_database")
        self.graph.add_edge("llm_database","chatbot")

        # Definindo entrada e saída do grafo
        self.graph.set_entry_point("process_text")
        self.graph.set_finish_point("chatbot")

        # Compilando o grafo
        self.graph_executor = self.graph.compile()
        self.llm_model = llm_model  # Instanciando o modelo de linguagem


    # Criando o nó de processamento do dado 
    def process_text(self, state: GraphState) -> GraphState:
        """Processa o texto (exemplo: converte para minúsculas)."""
        input_text = state.get("input_text", "")
        if not input_text:
            raise ValueError("O campo 'input_text' não pode estar vazio.")

        state["processed_text"] = input_text.lower()
        return state  # Retorna o estado original atualizado


    def query_llm(self, state: GraphState) -> GraphState:
        """Consulta o LLM usando o texto processado."""
        processed_text = state.get("processed_text", "")
        if not processed_text:
            raise ValueError("O campo 'processed_text' não pode estar vazio.")

        # Obtendo o agente do LLM e a memória
        agent, memory = self.llm_model.llm_agent()

        try:
            # Chamando o agente para gerar uma resposta
            response = agent.run(processed_text)
            state["llm_response"] = response  # Salvando a resposta corretamente

        except ValueError as e:
            print("Erro ao processar resposta do LLM:", e)
            state["llm_response"] = "Erro ao obter resposta do LLM."

        return state


    def run(self, input_text: str) -> dict:
        """Executa o grafo com o texto de entrada."""
        if not input_text:
            raise ValueError("O texto de entrada não pode estar vazio.")

        # Inicializando o estado inicial
        initial_state: GraphState = {
            "input_text": input_text,
            "processed_text": input_text.lower(),  # Garante que `processed_text` já tenha um valor válido
            "llm_response": None
        }

        # Executando o grafo
        result = self.graph_executor.invoke(initial_state)
        return result


    def chatbot(self, state: GraphState) -> GraphState:
        """Formata e retorna a resposta do LLM como mensagens do chatbot."""
        llm_response = state.get("llm_response", "")

        # Garante que há uma resposta válida antes de formatar
        if not llm_response:
            raise ValueError("O campo 'llm_response' não pode estar vazio.")

        # Formata a saída do chatbot no formato esperado
        state["chatbot_messages"] = {"messages": [{"role": "assistant", "content": llm_response}]}

        return state