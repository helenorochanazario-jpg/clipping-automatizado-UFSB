# -*- coding: utf-8 -*-
"""
Coleta publicações sobre a UFSB via RSS (Google News e Bing News),
identifica pessoas citadas, classifica o sentimento e grava tudo na
planilha Google Sheets.

Uso:
    python collector.py
"""
import re
import time
from datetime import datetime
from urllib.parse import quote

import feedparser
import pytz

from config import SEARCH_TERMS, UFSB_PEOPLE
from sentiment_analyzer import classify_sentiment
from sheets_writer import get_existing_links, append_rows

BAHIA_TZ = pytz.timezone("America/Bahia")

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
BING_NEWS_RSS = "https://www.bing.com/news/search?q={query}&format=RSS"


def build_queries():
    """Monta as URLs de busca para cada termo configurado em config.py."""
    queries = []
    for term in SEARCH_TERMS:
        encoded = quote(f'"{term}"')
        queries.append(GOOGLE_NEWS_RSS.format(query=encoded))
        queries.append(BING_NEWS_RSS.format(query=encoded))
    return queries


def word_boundary_match(term: str, text: str) -> bool:
    """Confirma se o termo aparece como palavra/expressão inteira no
    texto — é o que evita falsos positivos (ex.: 'porto' dentro de outra
    palavra não deve casar com 'Porto Seguro')."""
    pattern = r"\b" + re.escape(term) + r"\b"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def is_relevant(title: str, summary: str) -> bool:
    """Só é considerada relevante a publicação que de fato menciona a
    UFSB diretamente (escopo: menções diretas, não assuntos correlatos)."""
    text = f"{title} {summary}"
    return any(word_boundary_match(term, text) for term in SEARCH_TERMS)


def find_people(text: str) -> str:
    found = [p for p in UFSB_PEOPLE if word_boundary_match(p, text)]
    return ", ".join(found)


def parse_entry(entry, existing_links, seen_in_run):
    link = entry.get("link", "").strip()
    if not link or link in existing_links or link in seen_in_run:
        return None

    title = entry.get("title", "").strip()
    summary = entry.get("summary", "")

    if not is_relevant(title, summary):
        return None

    published = entry.get("published_parsed")
    if published:
        dt = datetime(*published[:6], tzinfo=pytz.utc).astimezone(BAHIA_TZ)
    else:
        dt = datetime.now(BAHIA_TZ)
    data_hora = dt.strftime("%d/%m/%Y %H:%M")

    source = entry.get("source")
    veiculo = source.get("title", "") if source else ""
    if not veiculo:
        veiculo = entry.get("author", "Fonte não identificada")

    pessoas = find_people(f"{title} {summary}")
    sentimento = classify_sentiment(f"{title}. {summary}")

    return {
        "data_hora": data_hora,
        "veiculo": veiculo,
        "titulo": title,
        "link": link,
        "pessoas": pessoas,
        "sentimento": sentimento,
    }


def collect():
    existing_links = get_existing_links()
    seen_in_run = set()
    new_rows = []

    for url in build_queries():
        try:
            feed = feedparser.parse(url)
        except Exception as exc:
            print(f"Erro ao buscar {url}: {exc}")
            continue

        for entry in feed.entries:
            row = parse_entry(entry, existing_links, seen_in_run)
            if row:
                new_rows.append(row)
                seen_in_run.add(row["link"])

        time.sleep(1)  # gentileza com os servidores de RSS

    if new_rows:
        append_rows(new_rows)
        print(f"{len(new_rows)} nova(s) publicação(ões) adicionada(s).")
    else:
        print("Nenhuma publicação nova encontrada nesta rodada.")


if __name__ == "__main__":
    collect()
