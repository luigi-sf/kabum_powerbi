import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\luigi\Downloads\study\power_automation\.env")

class PostgresPipeline:

    def open_spider(self, spider):
        url = os.getenv("DB_URL")
        print(f"🔍 DB_URL: {url}")  # ← adiciona isso
        self.conn = psycopg2.connect(url)
        self.cur = self.conn.cursor()
        self.salvos = 0
        print("Conectado ao banco!")

    def process_item(self, item, spider):
        preco = item.get("preco")

        if isinstance(preco, str):
            preco = preco.replace("R$", "").replace(".", "").replace(",", ".").strip()

        try:
            preco = float(preco)
        except:
            preco = None

        try:
            self.cur.execute(
                "SELECT id FROM produtos WHERE link = %s",
                (item.get("link"),)
            )
            result = self.cur.fetchone()

            if result:
                produto_id = result[0]
            else:
                self.cur.execute("""
                    INSERT INTO produtos (titulo, link, categoria)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """, (
                    item.get("titulo"),
                    item.get("link"),
                    item.get("categoria")
                ))
                produto_id = self.cur.fetchone()[0]

            self.cur.execute("""
                INSERT INTO historico_precos (produto_id, preco, rating, data_coleta)
                VALUES (%s, %s, %s, %s)
            """, (
                produto_id,
                preco,
                item.get("rating"),
                item.get("data_coleta")
            ))

            self.conn.commit()
            self.salvos += 1

        except Exception as e:
            spider.logger.error(f"Erro: {e}")
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
        print(f"\n✅ Finalizou!")
        print(f"📦 Registros salvos no histórico: {self.salvos}")