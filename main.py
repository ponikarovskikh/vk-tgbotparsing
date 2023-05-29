import vk_api
import telebot
from telebot import types
from vk_api.exceptions import ApiError

vk_token = 'xxxxxx'

telegram_token = 'xxxxxx'
channel_id = '-1001616800841'

vk_session = vk_api.VkApi(token=vk_token)
vk = vk_session.get_api()
bot = telebot.TeleBot(telegram_token)

group_ids = {
    'Group 1': -188192816,
    'Group 2': -203927743,
    'Group 3': -214871449
}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, 'Привет! Я бот, который будет парсить публикации из ВКонтакте и отправлять их в Телеграм-канал.')

@bot.message_handler(commands=['parse'])
def parse_vk_posts(message):
    try:
        group_id = -124024643
        response = vk.wall.get(owner_id=group_id, count=10)
        posts = response['items']

        # Парсим информацию из каждого поста
        for post in posts:
            text = post.get('text')
            attachments = post.get('attachments', [])

            if text:
                bot.send_message(channel_id, text)

            for attachment in attachments:
                if attachment['type'] == 'photo':
                    photo_url = attachment['photo']['sizes'][-1]['url']
                    bot.send_photo(channel_id, photo_url)

        bot.reply_to(message, 'Публикации успешно отправлены в Телеграм-канал.')

    except ApiError as e:
        bot.reply_to(message, f'Ошибка при парсинге публикаций ВКонтакте: {e}')

bot.polling()
