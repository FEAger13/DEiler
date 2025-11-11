import os
import logging
from flask import Flask, request
import telegram

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем Flask приложение
app = Flask(__name__)

# Получаем токен из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telegram.Bot(token=BOT_TOKEN)

# Обработчик вебхука от Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        
        chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        text = update.message.text
        
        logger.info(f"Получено сообщение: {text} от пользователя {user_id}")
        
        # Если пользователь отправил /start или любое сообщение
        if text:
            response_text = f"👋 Твой ID: `{user_id}`\nID чата: `{chat_id}`"
            bot.send_message(chat_id=chat_id, text=response_text, parse_mode='Markdown')
        
        return 'ok'

# Устанавливаем вебхук при запуске
@app.route('/')
def set_webhook():
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    bot.set_webhook(webhook_url)
    return f"Webhook установлен: {webhook_url}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
