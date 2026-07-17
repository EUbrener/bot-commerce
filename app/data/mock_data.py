MOCK_PEDIDOS = {
    'PED-123456': {'status': 'Em trânsito', 'previsao': '25/01/2026', 'transportadora': 'Correios'},
    'PED-789012': {'status': 'Entregue', 'data_entrega': '20/01/2026', 'recebedor': 'Portaria'},
    'ORD-555777': {'status': 'Preparando envio', 'previsao': '28/01/2026', 'transportadora': 'Jadlog'},
    'PED-987654': {'status': 'Não encontrado'},
    'PED-456789': {'status': 'Aguardando pagamento', 'expira': '22/01/2026'},
    'PED-111222': {'status': 'Em separação', 'previsao': '30/01/2026', 'transportadora': 'Total Express'},
}

CASOS_TESTE = [
    {
        'id': 1,
        'mensagem': 'oi',
        'intencao_esperada': 'saudacao',
        'entidade_esperada': None,
        'descricao': 'Saudação simples'
    },
    {
        'id': 2,
        'mensagem': 'como rastrear meu pedido',
        'intencao_esperada': 'faq',
        'entidade_esperada': None,
        'descricao': 'Pergunta FAQ exata'
    },
    {
        'id': 3,
        'mensagem': 'quanto tempo demora para entregar',
        'intencao_esperada': 'faq',
        'entidade_esperada': None,
        'descricao': 'Pergunta FAQ com sinônimos (testa embeddings)'
    },
    {
        'id': 4,
        'mensagem': 'quero rastrear meu pedido PED-123456',
        'intencao_esperada': 'rastreamento',
        'entidade_esperada': 'PED-123456',
        'descricao': 'Rastreamento com número de pedido'
    },
    {
        'id': 5,
        'mensagem': 'onde esta meu pedido',
        'intencao_esperada': 'rastreamento',
        'entidade_esperada': None,
        'descricao': 'Rastreamento sem número (deve pedir)'
    },
    {
        'id': 6,
        'mensagem': 'quero devolver o produto que comprei em 15/01/2026',
        'intencao_esperada': 'devolucao',
        'entidade_esperada': '15/01/2026',
        'descricao': 'Devolução de produto com data'
    },
    {
        'id': 7,
        'mensagem': 'produto veio quebrado, paguei R$ 150,00 e to muito insatisfeito',
        'intencao_esperada': 'reclamacao',
        'entidade_esperada': 'R$ 150,00',
        'descricao': 'Reclamação com entidades (valor)'
    },
    {
        'id': 8,
        'mensagem': 'posso pagar com pix tem desconto',
        'intencao_esperada': 'pagamento',
        'entidade_esperada': None,
        'descricao': 'Pagamento - redireciona para FAQ'
    },
    {
        'id': 9,
        'mensagem': 'xyz abc palavras aleatorias sem sentido',
        'intencao_esperada': 'incerto',
        'entidade_esperada': None,
        'descricao': 'Mensagem ambígua (testa threshold)'
    },
    {
        'id': 10,
        'mensagem': 'muito obrigado pela ajuda tchau',
        'intencao_esperada': 'despedida',
        'entidade_esperada': None,
        'descricao': 'Despedida'
    }
]
