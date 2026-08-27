# -*- coding: utf-8 -*-
"""
Classificação de sentimento das publicações, usando o pysentimiento
(modelo aberto e gratuito, treinado para português).
"""
from config import SENTIMENT_LANG

_analyzer = None

LABEL_MAP = {
    "POS": "positivo",
    "NEG": "negativo",
    "NEU": "neutro",
}


def get_analyzer():
    """Carrega o modelo uma única vez por execução (é o passo mais lento)."""
    global _analyzer
    if _analyzer is None:
        from pysentimiento import create_analyzer
        _analyzer = create_analyzer(task="sentiment", lang=SENTIMENT_LANG)
    return _analyzer


def classify_sentiment(text: str) -> str:
    """Recebe um texto (título + resumo) e devolve 'positivo', 'neutro'
    ou 'negativo'. Texto vazio é tratado como neutro."""
    if not text or not text.strip():
        return "neutro"
    analyzer = get_analyzer()
    result = analyzer.predict(text)
    return LABEL_MAP.get(result.output, "neutro")
