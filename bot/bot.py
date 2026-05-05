import subprocess
import os


class ScrapyBot:
    def __init__(self):
        self.spider_name = "kabum"
        self.projeto_path = r"C:\Users\luigi\Downloads\study\power_automation\data_scrapy\scraper"

    def rodar(self):
        print("\n🎯 Rodando Scrapy...\n")

        try:
            resultado = subprocess.run(
                ["scrapy", "crawl", self.spider_name],
                cwd=self.projeto_path
            )

            if resultado.returncode == 0:
                print("✅ Scrapy finalizado com sucesso!")
            else:
                print(f"❌ Scrapy finalizou com erro!")

        except Exception as e:
            print(f"❌ Erro ao executar: {e}")