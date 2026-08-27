# -*- coding: utf-8 -*-
"""
Leitura e escrita na planilha Google Sheets do clipping.
Autenticação via Conta de Serviço do Google (gratuita, sem assinatura).
"""
import os
import json

import gspread
from google.oauth2.service_account import Credentials

from config import DEFAULT_SHEET_NAME

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = os.environ.get("UFSB_SPREADSHEET_ID", "")
SHEET_NAME = os.environ.get("UFSB_SHEET_NAME", DEFAULT_SHEET_NAME)

# Estas colunas são a "fonte da verdade" — o painel de visualização
# (dashboard/index.html) espera exatamente estes nomes, nesta ordem.
HEADERS = [
    "Data/Hora",
    "Veículo/Perfil",
    "Título",
    "Link",
    "Pessoas UFSB citadas",
    "Sentimento",
]


def _get_client():
    creds_json = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)


def _get_worksheet():
    if not SPREADSHEET_ID:
        raise RuntimeError(
            "Defina a variável de ambiente UFSB_SPREADSHEET_ID com o ID da planilha."
        )
    client = _get_client()
    sh = client.open_by_key(SPREADSHEET_ID)
    try:
        ws = sh.worksheet(SHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=SHEET_NAME, rows=1000, cols=len(HEADERS))
        ws.append_row(HEADERS)
        return ws

    if ws.row_values(1) != HEADERS:
        ws.update("A1", [HEADERS])
    return ws


def get_existing_links():
    """Devolve o conjunto de links já presentes na planilha, para não
    coletar a mesma publicação duas vezes."""
    ws = _get_worksheet()
    values = ws.get_all_values()
    if len(values) <= 1:
        return set()
    link_col = HEADERS.index("Link")
    return {row[link_col] for row in values[1:] if len(row) > link_col and row[link_col]}


def append_rows(rows):
    """Recebe uma lista de dicionários (data_hora, veiculo, titulo, link,
    pessoas, sentimento) e acrescenta ao final da planilha."""
    ws = _get_worksheet()
    formatted = [
        [r["data_hora"], r["veiculo"], r["titulo"], r["link"], r["pessoas"], r["sentimento"]]
        for r in rows
    ]
    if formatted:
        ws.append_rows(formatted, value_input_option="USER_ENTERED")
