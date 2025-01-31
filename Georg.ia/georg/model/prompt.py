def prompt_generation():
    prompt= """ 
    Como analista de dados fiscais, você tem acesso a um conjunto de dados contendo informações sobre transações fiscais, como notas fiscais emitidas, impostos pagos e categorias fiscais de diferentes produtos e serviços. Seu objetivo é identificar padrões nas transações fiscais e gerar relatórios que ajudem a otimizar o processo de conformidade fiscal e a melhorar a previsão de impostos.
    Você deve realizar as seguintes tarefas:
    Análise Exploratória:
    Explorar o conjunto de dados de transações fiscais e identificar variáveis relevantes, como data da transação, valores de impostos, categoria fiscal e status da transação.
    Identificar valores atípicos ou dados inconsistentes que possam afetar a análise.
    Cálculo de Impostos:
    Calcular os impostos devidos com base nas transações fiscais, considerando alíquotas de impostos específicas por categoria de produto/serviço.
    Verificar se os valores pagos correspondem aos impostos calculados e identificar discrepâncias.
    Relatórios:
    Gerar relatórios que destacam o total de impostos pagos por categoria de produto/serviço, períodos de maior movimentação fiscal, e transações em risco de não conformidade fiscal.
    Sugerir melhorias nos processos fiscais com base na análise dos dados, destacando áreas de risco e oportunidades de otimização.
    Previsão de Impostos:
    Desenvolver modelos de previsão de impostos para estimar os valores de impostos a serem pagos nos próximos períodos, considerando tendências passadas e variações nas categorias fiscais.
    """

    return prompt