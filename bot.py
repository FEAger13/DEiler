import os
import logging
from flask import Flask, request
import requests

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Получаем токен бота из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Обработчик вебхука от Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        data = request.get_json()
        
        # Извлекаем данные из сообщения
        chat_id = data['message']['chat']['id']
        user_id = data['message']['from']['id']
        text = data['message'].get('text', '')
        
        logger.info(f"Сообщение от {user_id}: {text}")
        
        # Отправляем ответ с ID
        response_text = f"👋 Твой ID: `{user_id}`\nID чата: `{chat_id}`"
        send_message(chat_id, response_text)
        
        return 'ok'

# Функция отправки сообщения
def send_message(chat_id, text):
    url = f"{TELEGRAM_URL}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, json=payload)
    return response.json()

# Устанавливаем вебхук при запуске
@app.route('/')
def set_webhook():
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    response = requests.post(f"{TELEGRAM_URL}/setWebhook", data={'url': webhook_url})
    return f"✅ Webhook установлен!<br>URL: {webhook_url}<br>Response: {response.text}"

# Проверка здоровья
@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
