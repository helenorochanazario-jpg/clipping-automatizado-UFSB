# -*- coding: utf-8 -*-
"""
Configuração do Clipping Institucional — ACS/UFSB
Edite as listas abaixo conforme a necessidade da equipe. Não é preciso
mexer em nenhum outro arquivo para ajustar o que é coletado.
"""

# Termos usados para buscar publicações sobre a UFSB.
# A busca só considera uma correspondência de VERDADE quando o termo
# aparece como palavra/expressão inteira (evita falso positivo, ex.:
# "porto" isolado não deve casar com nada só por causa de "Porto Seguro").
SEARCH_TERMS = [
    "UFSB",
    "Universidade Federal do Sul da Bahia",
    "Campus Sosígenes Costa",
    "Campus Jorge Amado",
    "Campus Paulo Freire UFSB",
]

# Nomes e cargos da UFSB a serem identificados no texto das publicações.
# Adicione variações (com e sem título) para melhorar a detecção, ex.:
# "Fabrício Zanchi", "Reitor Fabrício Berton Zanchi".
UFSB_PEOPLE = [
    # "Fabrício Berton Zanchi",
    # "Nome Sobrenome",
]

# Idioma usado pelo pysentimiento para classificar sentimento (não altere).
SENTIMENT_LANG = "pt"

# Nome da aba (worksheet) dentro da planilha do Google Sheets onde os
# dados serão gravados. Pode ser alterado via variável de ambiente
# UFSB_SHEET_NAME no workflow, se preferir.
DEFAULT_SHEET_NAME = "clipping tratado"
