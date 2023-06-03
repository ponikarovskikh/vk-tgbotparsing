import json
import time
import youtube_dl
import aiohttp
import requests
from auth_data import token
import os
import re
import asyncio
import telebot

# bruh_video
# everydaygosling
bot = telebot.TeleBot('xxxx')
channel_id = '-1001616800841'
# group_names = ['avemariika', 'hihigs_and_filials', 'justputin2024', 'oguzoksphilosophy', 'everydaygosling', 'e_memasik']
group_names=['fullgop', 'avemariika']
groups=[]
async def bot1():
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(chat_id=message.chat.id,
                         text="Привет! Я бот, который может получить фотографии из ссылок. Просто введите команду /parse и ссылку на фото.")

    @bot.message_handler(commands=['add'])
    def start1(message):
        link=message.text.split(' ')
        link=link[-1]
        if link not in group_names:
            group_names.append(link)
            bot.send_message(chat_id=message.chat.id,
                             text=f"{link} добавлена в список групп ")
        else:
            bot.send_message(chat_id=message.chat.id,
                             text=f"упс, {link} уже имеется в список групп ")

    @bot.message_handler(commands=['delete'])
    def start3(message):
        link = message.text.split(' ')
        link = link[-1]
        if link not in group_names:
            group_names.append(link)
            bot.send_message(chat_id=message.chat.id,
                             text=f"{link} нету в списке групп ")
        else:
            group_names.remove(link)
            bot.send_message(chat_id=message.chat.id,
                             text=f" {link} уже удалена из списка ")




    links = []

    # @bot.message_handler(commands=['add'])
    # def add_links(message):
    #     bot.send_message(chat_id=message.chat.id,
    #                      text="Введите ссылки, которые нужно добавить в список. Каждую ссылку в новой строке.")
    #
    #     # Устанавливаем следующий обработчик, который будет ожидать ввод ссылок
    #     bot.register_next_step_handler(message, process_links)
    #
    # def process_links(message):
    #     text = message.text.strip()  # Удаляем лишние пробелы в начале и конце сообщения
    #
    #     # Разделяем текст на строки и добавляем ссылки в список
    #     for line in text.split('\n'):
    #         link = line.strip()  # Удаляем лишние пробелы в начале и конце строки
    #         link = link.replace("https://vk.com/","")
    #         links.append(link)
    #         for link in linksfile.linksyet:
    #             if link not in linksfile.linksyet:
    #                 linksfile.linksyet(link)
    #             else:
    #                 bot.send_message(chat_id=message.chat.id, text=f"Ссылка : {link} уже есть   ")
    #
    #
    #
    #     bot.send_message(chat_id=message.chat.id, text="Ссылки успешно добавлены в список.")



    @bot.message_handler(commands=['parse'])
    def parse_photo(message):
        try:
            # Загружаем и отправляем фото
            download_img_and_video_send(message.chat.id)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id, text="Произошла ошибка при загрузке и отправке фото.")
            print(e)

    def download_img_and_video_send(chat_id):
        for group_name in group_names:
            # group_name='everydaygosling'
            url = f'https://api.vk.com/method/wall.get?domain={group_name}&count=30&access_token={token}&v=5.81'
            try:
                req = requests.get(url)
                src = req.json()
                posts = src['response']['items']
                print(posts)
            except Exception:
                print('shit conn')

            fresh_posts_id = []
            for fresh_post_id in posts:
                fresh_post_id=fresh_post_id['id']
                fresh_posts_id.append(fresh_post_id)
                print(fresh_post_id)

            if os.path.exists(f'{group_name}'):
                print(f'directory {group_name} already exists!')
            else:
                    os.mkdir(group_name)
            if not os.path.exists(f'{group_name}/exists_posts_{group_name}.txt'):
                print('no files such that ID','creating')
                postedyet = []


            else:
                print("we've just found this file ,starting filtring posts now")
                postedyet = []
                with open(f'{group_name}/exists_posts_{group_name}.txt', 'r') as file:
                    for line in file:
                        number = line.strip()
                        postedyet.append(int(number))
                print(postedyet)

            for post in posts:
                    time.sleep(1)
                    post_id = post['id']
                # if post_id in postedyet:
                #     print('такой пост уже обработан и отправлен')
                #     continue

                    print('\n')
                    print('send post ID ',post_id)

                    try:

                        text = post['text']
                        text = re.sub(r'\[club\d+\|', '', text).replace(']', '')

                        print(text)
                        if 'attachments' in post:
                            # функция для сохранения изображений
                            def download_img(url, post_id, group_name,chat_id):
                                nonlocal text_sent
                                res = requests.get(url)

                                # создаем папку group_name/files
                                if not os.path.exists(f"{group_name}/files"):
                                    os.mkdir(f"{group_name}/files")

                                with open(f"{group_name}/files/{post_id}.jpg", "wb") as img_file:
                                    img_file.write(res.content)
                                with open(f"{group_name}/files/{post_id}.jpg", "rb") as photo:
                                    if text_sent!=1:
                                        bot.send_photo(chat_id=channel_id, photo=photo,caption=text)
                                        text_sent=1
                                    else:
                                        bot.send_photo(chat_id=channel_id, photo=photo)
                                os.remove(f"{group_name}/files/{post_id}.jpg")


                            def download_video(url, post_id, group_name,chat_id):
                                try:
                                    nonlocal text_sent
                                    output_path = f"{group_name}/{post_id}"
                                    ydl_opts = {"outtmpl": f"{group_name}/{post_id}.%(ext)s",
                                                "format": "mp4"

                                                }
                                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                        # video_info = ydl.extract_info(url, download=False)
                                        ydl.download([url])
                                        with open(f"{output_path}.mp4", "rb") as video_file:
                                            if text_sent != 1:
                                                bot.send_video(chat_id=channel_id, video=video_file,caption=text)
                                                text_sent=1
                                            else:
                                                bot.send_video(chat_id=channel_id, video=video_file)


                                        os.remove(f"{output_path}.mp4")
                                except Exception:
                                    print("Не удалось скачать видео...")


                        # everydaygosling


                            post=post['attachments']
                            if len(post) ==1:
                                    text_sent=0
                                    if post[0]['type'] == 'photo':
                                        photo_post_count =0
                                        post_photo_url =post[0]['photo']['sizes'][-1]['url']
                                        print(post_photo_url)
                                        download_img(post_photo_url,post_id,group_name,chat_id)

                                    elif post[0]['type'] == 'video':
                                        time.sleep(2)
                                        # print("Видео пост")

                                        # формируем данные для составления запроса на получение ссылки на видео
                                        video_access_key = post[0]["video"]["access_key"]
                                        video_post_id = post[0]["video"]["id"]
                                        video_owner_id = post[0]["video"]["owner_id"]

                                        video_get_url = f"https://api.vk.com/method/video.get?videos={video_owner_id}_{video_post_id}_{video_access_key}&access_token={token}&v=5.81"

                                        res=requests.get(video_get_url).json()

                                        video_url = res["response"]["items"][0]["player"]

                                        download_video(video_url, post_id, group_name,chat_id)
                                    else:print('link or audio')
                            else:
                                    text_sent = 0

                                    for post_item_photo in post:
                                        if post_item_photo["type"] == "photo":
                                                post_photo_url =post[0]['photo']['sizes'][-1]['url']
                                                download_img(post_photo_url, post_id, group_name, chat_id)

                                        elif post[0]['type'] == 'video':
                                            time.sleep(2)
                                            video_access_key = post[0]["video"]["access_key"]
                                            video_post_id = post[0]["video"]["id"]
                                            video_owner_id = post[0]["video"]["owner_id"]

                                            video_get_url = f"https://api.vk.com/method/video.get?videos={video_owner_id}_{video_post_id}_{video_access_key}&access_token={token}&v=5.81"

                                            res = requests.get(video_get_url).json()

                                            video_url = res["response"]["items"][0]["player"]

                                            download_video(video_url, post_id, group_name, chat_id)
                                        else:print('link or audio')


                        else:
                            print('нет вложений')
                    except Exception:
                        print('чтото не так ')




            with open(f'{group_name}/exists_posts_{group_name}.txt', 'w') as file:
                    for item in fresh_posts_id:
                        file.write(str(item)+'\n')

    bot.polling()











async def main():
    await bot1()

if __name__ == "__main__":
        asyncio.run(main())




















