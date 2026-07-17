import re
from datetime import datetime
from typing import Dict, List
from app import config

def extrair_e_validar_entidades(texto: str) -> Dict[str, Dict[str, List]]:
    """
    Extrai e valida entidades de um texto.

    Validações:
    - Pedido: formato PED/ORD-XXXXX com 5-10 dígitos
    - Data: ano entre 2020-2030, não mais de 1 ano no futuro
    - Valor: entre R$ 0 e R$ 10.000
    - Email: formato básico válido
    - Telefone: DDD brasileiro válido (ou 0800)

    Args:
        texto: Texto para extração

    Returns:
        Dicionário com entidades extraídas e validadas
    """
    # 1. Encontrar todos os matches com base nas regexes configuradas
    pedidos = re.findall(config.REGEX_PEDIDO, texto)
    datas = re.findall(config.REGEX_DATA, texto)
    valores = re.findall(config.REGEX_VALOR, texto)
    emails = re.findall(config.REGEX_EMAIL, texto)
    telefones = re.findall(config.REGEX_TELEFONE, texto)

    # 2. Validar Pedidos (formato já restrito pela regex, mas remover duplicados)
    pedidos_validos = []
    for p in pedidos:
        # Remover duplicados
        if p not in pedidos_validos:
            # Dupla validação do comprimento de dígitos após o hífen
            parts = p.split('-')
            digits = parts[-1] if len(parts) > 1 else p
            if 5 <= len(re.sub(r'\D', '', digits)) <= 10:
                pedidos_validos.append(p)

    # 3. Validar Datas (ano 2020-2030, não superior a 1 ano no futuro)
    datas_validas = []
    for d in datas:
        if d in datas_validas:
            continue
        try:
            # Tentar parsear a data (formatos comuns: DD/MM/AAAA ou DD-MM-AAAA)
            parts = re.split(r'[/-]', d)
            if len(parts) == 3:
                dia, mes, ano = int(parts[0]), int(parts[1]), int(parts[2])
                if 2020 <= ano <= 2030:
                    dt = datetime(ano, mes, dia)
                    # Checar se não é mais de 365 dias no futuro
                    diff = (dt - datetime.now()).days
                    if diff <= 366:
                        datas_validas.append(d)
        except ValueError:
            pass

    # 4. Validar Valores (R$ 0 a R$ 10.000)
    valores_validos = []
    for v in valores:
        if v in valores_validos:
            continue
        try:
            # Limpar string do valor (remover R$, espaços, pontos de milhar, e substituir vírgula decimal)
            val_str = v.replace('R$', '').strip()
            val_str = val_str.replace('.', '').replace(',', '.')
            val_float = float(val_str)
            if 0.0 <= val_float <= 10000.0:
                valores_validos.append(v)
        except ValueError:
            pass

    # 5. Validar Emails (remover duplicados)
    emails_validos = []
    for e in emails:
        if e not in emails_validos:
            emails_validos.append(e)

    # 6. Validar Telefones (DDD brasileiro válido ou 0800)
    telefones_validos = []
    for t in telefones:
        if t in telefones_validos:
            continue
        
        # Se for um número 0800, é válido
        if '0800' in t:
            telefones_validos.append(t)
            continue

        # Tentar extrair o DDD (primeiros 2 dígitos numéricos do telefone)
        digitos = re.sub(r'\D', '', t)
        if len(digitos) >= 10:  # DDD + telefone (mínimo 10 dígitos)
            ddd = digitos[:2]
            if ddd in config.DDDS_VALIDOS:
                telefones_validos.append(t)

    return {
        'pedidos': {'valores': pedidos, 'validos': pedidos_validos},
        'datas': {'valores': datas, 'validos': datas_validas},
        'valores': {'valores': valores, 'validos': valores_validos},
        'emails': {'valores': emails, 'validos': emails_validos},
        'telefones': {'valores': telefones, 'validos': telefones_validos}
    }
