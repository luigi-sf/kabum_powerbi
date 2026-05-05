# 📊 Kabum Price Tracker + Power BI

Projeto desenvolvido para monitorar automaticamente os preços de produtos do site Kabum.com.br, armazenando o histórico em um banco de dados na nuvem e visualizando as informações em um dashboard interativo no Power BI.

## 🎯 Objetivo

Acompanhar a variação de preços de produtos de tecnologia ao longo do tempo, identificando os produtos mais caros, mais baratos e aqueles que sofreram alterações de preço, permitindo uma análise completa do mercado de tecnologia brasileiro.

## 🚀 Tecnologias

- **Python** — linguagem principal
- **Scrapy + Playwright** — web scraping com suporte a JavaScript
- **PostgreSQL (Supabase)** — banco de dados na nuvem
- **Power BI** — dashboard interativo
- **Schedule** — agendamento automático semanal

## 📁 Estrutura do Projeto
power_automation/
├── bot/
│   ├── bot.py
│   └── main.py
├── data_scrapy/
│   └── scraper/
│       └── scraper/
│           ├── spiders/
│           │   └── kabum.py
│           ├── pipelines.py
│           └── settings.py
├── .env.example
├── requirements.txt
└── README.md

## ⚙️ Como rodar

**1. Clone o repositório**
```bash
git clone https://github.com/luigi-sf/kabum_powerbi.git
cd kabum_powerbi
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Configure o `.env`**
```bash
cp .env.example .env
```
Preencha com suas credenciais do Supabase:
DB_URL=postgresql://postgres:SUA_SENHA@seu_host:5432/postgres

**4. Crie as tabelas no Supabase**
```sql
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    titulo TEXT,
    link TEXT UNIQUE,
    categoria TEXT
);

CREATE TABLE historico_precos (
    id SERIAL PRIMARY KEY,
    produto_id INTEGER REFERENCES produtos(id),
    preco NUMERIC,
    rating NUMERIC,
    data_coleta DATE
);
```

**5. Rode o bot**
```bash
python bot/main.py
```

## 🔄 Como funciona

O bot roda automaticamente toda semana, acessando as páginas de cada categoria do Kabum e coletando título, preço, avaliação e link de cada produto. Os dados são salvos no Supabase em duas tabelas — uma com os produtos cadastrados e outra com o histórico de preços de cada coleta. O Power BI conecta diretamente na API do Supabase e atualiza o dashboard automaticamente.

## 📦 Categorias coletadas

- Hardware — placa de vídeo, processador, memória RAM, SSD, fonte, placa mãe
- Computadores — notebook, desktop, monitor
- Celular — smartphones, tablets

- ## 📊 Preview
![Dashboard] (image/relatorio.png)

## 📈 Dashboard Power BI

- Preço médio por categoria
- Produto mais caro e mais barato com nome dinâmico

- Variação de preço com indicadores ▲ vermelho e ▼ verde
- Histórico de preços ao longo do tempo
- Distribuição de produtos por categoria
- Relação entre preço e avaliação dos produtos
- Total de produtos e total de coletas realizadas
