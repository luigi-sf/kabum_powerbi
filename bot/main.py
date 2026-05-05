import schedule
import time
from bot import ScrapyBot

bot = ScrapyBot()

# roda uma vez imediatamente
print("🚀 Rodando primeira vez...")
bot.rodar()

# agenda pra toda segunda às 8h
schedule.every().monday.at("08:00").do(bot.rodar)

print("⏰ Agendamento ativo...")

while True:
    schedule.run_pending()
    time.sleep(60)