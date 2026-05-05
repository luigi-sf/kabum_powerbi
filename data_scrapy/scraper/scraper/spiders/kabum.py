import scrapy
from datetime import datetime
import re


class KabumSpider(scrapy.Spider):
    name = "kabum"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 🔥 controle global de duplicados
        self.links_vistos_global = set()

    def start_requests(self):
        categorias = {
            
            "placa_video": "https://www.kabum.com.br/hardware/placa-de-video-vga",
            "processador": "https://www.kabum.com.br/hardware/processadores",
            "memoria_ram": "https://www.kabum.com.br/hardware/memorias-ram",
            "ssd": "https://www.kabum.com.br/hardware/ssd-2-5",
            "fonte": "https://www.kabum.com.br/hardware/fontes",
            "placa_mae": "https://www.kabum.com.br/hardware/placas-mae",
            "notebook": "https://www.kabum.com.br/computadores/notebooks",
            "desktop": "https://www.kabum.com.br/computadores/computadores-desktop",
            "monitor": "https://www.kabum.com.br/computadores/monitores",
            "celular": "https://www.kabum.com.br/celular-smartphone/smartphones",
            "impressora": "https://www.kabum.com.br/computadores/impressoras",
        }

        for categoria, base_url in categorias.items():
            for page in range(1, 30):
                url = f"{base_url}?page={page}"

                yield scrapy.Request(
                    url=url,
                    meta={
                        "playwright": True,
                        "playwright_include_page": True,
                        "categoria": categoria,
                        "page_num": page,
                        "base_url": base_url,
                    },
                    callback=self.parse
                )

    async def parse(self, response):
        page = response.meta.get("playwright_page")
        categoria = response.meta.get("categoria")
        page_num = response.meta.get("page_num")

        if not page:
            return

        try:
            await page.wait_for_selector('a[href*="/produto/"]', timeout=15000)
        except:
            self.logger.warning(f"Timeout página {page_num} de {categoria}")
            await page.close()
            return

        # 🔎 detecta redirect
        url_atual = page.url
        if page_num > 1 and f"page={page_num}" not in url_atual:
            self.logger.info(f"🛑 Redirect em {categoria} página {page_num} — parando")
            await page.close()
            return

        content = await page.content()
        new_response = response.replace(body=content)

        # 🕒 timestamp real
        data = datetime.now()

        produtos = new_response.css('a[href*="/produto/"]')

        if not produtos:
            self.logger.info(f"Página {page_num} de {categoria} vazia — parando")
            await page.close()
            return

        count = 0

        for produto in produtos:
            aria = produto.css("::attr(aria-label)").get()
            link = produto.css("::attr(href)").get()

            if not aria or not link:
                continue

            if not link.startswith("/produto/"):
                continue

            link_completo = f"https://www.kabum.com.br{link}"

            # 🔥 deduplicação GLOBAL
            if link_completo in self.links_vistos_global:
                continue

            self.links_vistos_global.add(link_completo)

            # 🎯 título
            titulo_match = re.match(r'^(.+?)(?:,\s*avaliação|,\s*R\$)', aria)
            titulo = titulo_match.group(1).strip() if titulo_match else aria.split(",")[0].strip()

            # 💰 preço
            preco_match = re.search(r'R\$\s*([\d.,]+)', aria)
            preco = preco_match.group(1).strip() if preco_match else None

            # ⭐ rating
            rating_match = re.search(r'avaliação\s+([\d.]+)\s+estrelas', aria)
            rating = float(rating_match.group(1)) if rating_match else None

            count += 1

            yield {
                "titulo": titulo,
                "link": link_completo,
                "preco": preco,
                "rating": rating,
                "categoria": categoria,
                "data_coleta": data
            }

        self.logger.info(f"📦 Página {page_num} | {categoria} | {count} produtos")
        self.logger.info(f"🔢 Total únicos até agora: {len(self.links_vistos_global)}")

        await page.close()