import os
import logging
from flask import Flask, request
from telegram import Bot
from telegram.ext import Dispatcher, MessageHandler, filters

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем Flask приложение
app = Flask(__name__)

# Получаем токен из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# Обработчик всех сообщений
async def echo(update, context):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    
    response_text = f"👋 Твой ID: `{user_id}`\nID чата: `{chat_id}`"
    await update.message.reply_text(response_text, parse_mode='Markdown')

# Добавляем обработчик
dispatcher.add_handler(MessageHandler(filters.ALL, echo))

# Обработчик вебхука от Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return 'ok'

# Устанавливаем вебхук при запуске
@app.route('/')
def set_webhook():
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    bot.set_webhook(webhook_url)
    return f"Webhook установлен: {webhook_url}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
