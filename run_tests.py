import sys
# Define encoding do console para UTF-8 no Windows para evitar UnicodeEncodeError para emojis
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from app.data.mock_data import CASOS_TESTE
from app.services.chatbot_service import processar_mensagem, obter_analytics
from app.nlp.classifier import load_classifier
from app.nlp.faq import load_faq_models

def executar_casos_teste():
    print("Executando Casos de Teste de Validação...")
    print("=" * 70)

    # 1. Carregar modelos
    try:
        load_classifier()
        load_faq_models()
    except FileNotFoundError as e:
        print(f"❌ Erro: {e}")
        print("Certifique-se de treinar os modelos primeiro executando: python train.py")
        sys.exit(1)

    detalhes = []
    passou = 0

    # 2. Iterar sobre cada caso
    for caso in CASOS_TESTE:
        # Processa a mensagem usando o pipeline central do chatbot
        resultado = processar_mensagem(caso['mensagem'])

        # Verificar se a intenção está correta
        intencao_correta = resultado['intencao'] == caso['intencao_esperada']

        # Verificar se a entidade esperada está presente nos resultados válidos
        entidade_correta = True
        if caso['entidade_esperada']:
            todas_validas = []
            for cat in resultado['entidades'].values():
                todas_validas.extend(cat['validos'])
            entidade_correta = caso['entidade_esperada'] in todas_validas

        # Sucesso se intenção E entidade estiverem corretas
        caso_passou = intencao_correta and entidade_correta
        if caso_passou:
            passou += 1

        detalhes.append({
            'id': caso['id'],
            'descricao': caso['descricao'],
            'mensagem': caso['mensagem'],
            'intencao_esperada': caso['intencao_esperada'],
            'intencao_obtida': resultado['intencao'],
            'intencao_correta': intencao_correta,
            'confianca': resultado['confianca'],
            'entidade_esperada': caso['entidade_esperada'],
            'entidade_correta': entidade_correta,
            'nivel_busca': resultado.get('nivel_busca'),
            'requer_humano': resultado['requer_humano'],
            'passou': caso_passou
        })

    # 3. Exibir Relatório
    total = len(CASOS_TESTE)
    falhou = total - passou
    taxa_sucesso = passou / total if total > 0 else 0

    print(f"\n📊 RELATÓRIO DE TESTES")
    print(f"   Total: {total}")
    print(f"   Passou: {passou}")
    print(f"   Falhou: {falhou}")
    print(f"   Taxa de sucesso: {taxa_sucesso*100:.1f}%")
    print("-" * 70)
    print("📝 DETALHES POR CASO:")
    print("-" * 70)

    for d in detalhes:
        status_icon = "✅" if d['passou'] else "❌"
        print(f"\n{status_icon} Caso {d['id']}: {d['descricao']}")
        print(f"   Input: '{d['mensagem']}'")
        print(f"   Intenção: {d['intencao_obtida']} (esperado: {d['intencao_esperada']}) - {'✓' if d['intencao_correta'] else '✗'}")
        print(f"   Confiança: {d['confianca']:.2%}")
        if d['entidade_esperada']:
            print(f"   Entidade esperada: {d['entidade_esperada']} - {'✓' if d['entidade_correta'] else '✗'}")
        if d['nivel_busca']:
            print(f"   Nível de busca FAQ: {d['nivel_busca']}")
        if d['requer_humano']:
            print(f"   🔴 Requer humano")

    print("=" * 70)
    
    # 4. Avaliar taxa mínima de sucesso (notebook exige >= 50%)
    if taxa_sucesso >= 0.5:
        print(f"\n✅ Q6 validada com sucesso! Taxa de sucesso: {taxa_sucesso*100:.1f}%")
        return True
    else:
        print(f"\n⚠️ Taxa de sucesso abaixo de 50%: {taxa_sucesso*100:.1f}%")
        return False

if __name__ == "__main__":
    executar_casos_teste()
