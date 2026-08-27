# Clipping Institucional — ACS/UFSB

Ferramenta gratuita e customizável de monitoramento de mídia (clipping) sobre a
Universidade Federal do Sul da Bahia. Coleta publicações automaticamente, classifica
o sentimento e disponibiliza um painel de visualização — tudo sem custo de assinatura.

## O que a ferramenta faz

- **Coleta automática 2x ao dia** (08h e 18h, horário da Bahia) via RSS do Google
  News e Bing News, buscando pelos termos definidos em `config.py`.
- **Classifica o sentimento** (positivo, neutro, negativo) de cada publicação com o
  [pysentimiento](https://github.com/pysentimiento/pysentimiento), modelo aberto e
  gratuito treinado para português.
- **Identifica pessoas da UFSB** citadas no texto, a partir de uma lista editável.
- **Evita duplicatas**: só grava publicações cujo link ainda não está na planilha.
- **Grava tudo em uma planilha Google Sheets**, com as colunas: Data/Hora,
  Veículo/Perfil, Título, Link, Pessoas UFSB citadas, Sentimento.
- **Painel de visualização** (`dashboard/index.html`) com filtros, gráficos e
  tabela — publicável de graça no GitHub Pages.

## Sobre redes sociais

Instagram, Facebook e X/Twitter restringiram bastante o acesso gratuito às suas
APIs, então não é possível fazer coleta automática confiável e gratuita nessas
plataformas sem violar os termos de uso. Duas soluções ficam disponíveis:

1. A coleta via RSS já traz matérias jornalísticas que embutem ou citam posts de
   redes sociais.
2. **Entrada manual**: a equipe pode adicionar diretamente na planilha (mesma aba,
   mesmas 6 colunas) qualquer publicação de rede social encontrada manualmente. O
   painel de visualização lê a aba inteira, então essas linhas entram
   automaticamente nos gráficos e filtros — não precisa mexer em nenhum código.

---

## Passo a passo de implantação (tudo gratuito)

### 1. Criar a planilha no Google Sheets

Crie uma planilha nova (ou use uma existente) e anote o **ID da planilha** — é o
trecho da URL entre `/d/` e `/edit`:
`https://docs.google.com/spreadsheets/d/ESTE_TRECHO_AQUI/edit`

O script cria a aba e o cabeçalho automaticamente na primeira execução — não
precisa formatar nada manualmente.

### 2. Criar uma conta de serviço no Google Cloud (gratuita)

1. Acesse [console.cloud.google.com](https://console.cloud.google.com/), crie um
   projeto (ou use um existente).
2. Em **APIs e Serviços → Biblioteca**, ative a **Google Sheets API**.
3. Em **APIs e Serviços → Credenciais → Criar credenciais → Conta de serviço**,
   crie uma conta de serviço.
4. Na conta de serviço criada, vá em **Chaves → Adicionar chave → JSON** e baixe o
   arquivo. Guarde-o com segurança (ele dá acesso à planilha).
5. Copie o e-mail da conta de serviço (algo como
   `nome@projeto.iam.gserviceaccount.com`) e **compartilhe a planilha** do passo 1
   com esse e-mail, dando permissão de **Editor**.

### 3. Criar o repositório no GitHub e subir estes arquivos

Crie um repositório (pode ser privado) e envie todos os arquivos desta pasta,
mantendo a estrutura, especialmente `.github/workflows/clipping.yml`.

### 4. Configurar os "Secrets" do repositório

Em **Settings → Secrets and variables → Actions → New repository secret**, crie:

| Nome | Valor |
|---|---|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Cole o **conteúdo inteiro** do arquivo JSON baixado no passo 2 |
| `UFSB_SPREADSHEET_ID` | O ID da planilha (passo 1) |

### 5. Ativar a coleta automática

O workflow já está configurado para rodar sozinho 2x ao dia. Para testar
imediatamente: vá na aba **Actions** do repositório → **Clipping Institucional
UFSB** → **Run workflow**.

### 6. Publicar a aba da planilha como CSV (para o painel ler os dados)

1. Na planilha, abra a aba `Clipping`.
2. **Arquivo → Compartilhar → Publicar na Web**.
3. Selecione a aba `Clipping` e o formato **CSV**, depois clique em **Publicar**.
4. Copie o link gerado.
5. Abra `dashboard/index.html` e cole o link na constante `SHEET_CSV_URL`, no topo
   do bloco `<script>`.

> **Sobre privacidade:** "Publicar na Web" torna a aba acessível a quem tiver o
> link (não aparece em buscas do Google, mas também não exige login). Para um
> painel de uso puramente interno, publique o link apenas para a equipe da ACS ou
> hospede o painel em um ambiente de acesso restrito, em vez do GitHub Pages
> público.

### 7. Publicar o painel no GitHub Pages (gratuito)

Em **Settings → Pages**, selecione a branch `main` e a pasta `/dashboard` (ou
`/root`, movendo `index.html` para a raiz, se preferir). O link ficará disponível
em poucos minutos.

---

## Como personalizar

- **Termos de busca e pessoas da UFSB**: edite `config.py` — não precisa mexer em
  mais nada.
- **Nome da aba na planilha**: variável de ambiente `UFSB_SHEET_NAME` (opcional,
  padrão é `Clipping`).
- **Horários da coleta**: altere os valores de `cron` em
  `.github/workflows/clipping.yml` (os horários estão em UTC).
- **Cores e fontes do painel**: no início do `<style>` de `dashboard/index.html`,
  já usando a paleta institucional da UFSB (azul-marinho, azul, amarelo e verde) e
  as fontes Poppins/PT Sans.

## Estrutura dos arquivos

```
ufsb-clipping/
├── config.py                  # termos de busca e lista de pessoas (edite aqui)
├── collector.py                # script principal de coleta
├── sentiment_analyzer.py       # classificação de sentimento
├── sheets_writer.py            # leitura/escrita na planilha
├── requirements.txt            # dependências Python
├── .github/workflows/
│   └── clipping.yml            # agenda a coleta 2x ao dia
├── dashboard/
│   └── index.html              # painel de visualização (GitHub Pages)
└── README.md
```

## Executando localmente (opcional, para testes)

```bash
pip install -r requirements.txt
export GOOGLE_SERVICE_ACCOUNT_JSON="$(cat caminho/para/credenciais.json)"
export UFSB_SPREADSHEET_ID="id_da_planilha"
python collector.py
```

## Limitações conhecidas

- RSS de notícias cobre bem portais de imprensa, mas não substitui totalmente
  redes sociais — use a entrada manual para isso (ver seção acima).
- A primeira execução do workflow demora alguns minutos a mais, pois instala o
  modelo de análise de sentimento; as execuções seguintes usam o cache de pip.
- O reconhecimento de pessoas é por correspondência de nome (texto), então nomes
  muito comuns podem gerar falsos positivos — ajuste a lista em `config.py`
  conforme necessário.
