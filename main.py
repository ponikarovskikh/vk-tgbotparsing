import json
import time
import youtube_dl
import aiohttp
import requests
from auth_data import token
import os
import re
import asyncio
import vkapi
from pytube import YouTube
import subprocess
import ffmpeg
# bruh_video
# everydaygosling



async def get_wall_posts(group_name):


    url = f'https://api.vk.com/method/wall.get?domain={group_name}&count=20&access_token={token}&v=5.81'
    try:
        req = requests.get(url)
    except Exception:
        print('shit conn')
    src = req.json()

    posts = src['response']['items']
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






    # for post in posts:





    for post in posts:
        time.sleep(1)
        post_id = post['id']
        if post_id in postedyet:
            print('такой пост уже обработан и отправлен')
            continue
        else:
            print('\n')
            print('send post ID ',post_id)

            try:
                text = post['text']
                text = re.sub(r'\[club\d+\|', '', text).replace(']', '')

                print(text)
                if 'attachments' in post:
                    # функция для сохранения изображений
                    def download_img(url, post_id, group_name):
                        res = requests.get(url)

                        # создаем папку group_name/files
                        if not os.path.exists(f"{group_name}/files"):
                            os.mkdir(f"{group_name}/files")

                        with open(f"{group_name}/files/{post_id}.jpg", "wb") as img_file:
                            img_file.write(res.content)

                    def download_video(url, post_id, group_name):
                        # создаем папку group_name/files
                        if not os.path.exists(f"{group_name}/video_files"):
                            os.mkdir(f"{group_name}/video_files")


                        try:
                            output_path = f"{group_name}/video_files/{post_id}"
                            ydl_opts = {"outtmpl": f"{group_name}/video_files/{post_id}.%(ext)s",
                                        "format": "mp4"

                                        }
                            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                video_info = ydl.extract_info(url, download=False)
                                video_duration = video_info["duration"]
                                if video_duration > 300:
                                    print("Видео слишком долгое")
                                else:
                                    print(f"Видео длится {video_duration} секунд. Сохраняем видео...")
                                    ydl.download([url])
                        except Exception:
                            print("Не удалось скачать видео...")


                # everydaygosling


                    post=post['attachments']
                    if len(post) ==1:

                            if post[0]['type'] == 'photo':
                                photo_post_count =0
                                post_photo =post[0]['photo']
                                # print(post_photo)
                                sizes=post_photo['sizes']
                                # print('блок sizes')
                                # print(sizes,type(sizes))
                                # print('\n\n')
                                maxresolve=[]
                                # print('блок size1')
                                for size in sizes:
                                    # print(size,type(size))
                                    width=size['width']
                                    # print(width)
                                    maxresolve.append(int(width))
                                # print(maxresolve)
                                maxresolve=str(max(maxresolve))
                                # print(maxresolve)
                                # print('блок size2')
                                for size in sizes:
                                    url=size['url']
                                    if f'{str(maxresolve)}x' in url:
                                        post_photo=url
                                        print(post_photo)
                                        download_img(post_photo,post_id,group_name)
                                        break
                            elif post[0]['type'] == 'video':
                                print("Видео пост")

                                # формируем данные для составления запроса на получение ссылки на видео
                                video_access_key = post[0]["video"]["access_key"]
                                video_post_id = post[0]["video"]["id"]
                                video_owner_id = post[0]["video"]["owner_id"]

                                video_get_url = f"https://api.vk.com/method/video.get?videos={video_owner_id}_{video_post_id}_{video_access_key}&access_token={token}&v=5.81"

                                async def fetch_data(url):
                                    async with aiohttp.ClientSession() as session:
                                        async with session.get(url) as response:
                                            response_json = await response.json()
                                            return response_json
                                res = await fetch_data(video_get_url)

                                video_url = res["response"]["items"][0]["player"]
                                print(video_url)
                                download_video(video_url, post_id, group_name)
                            else:print('link or audio')
                    else:
                            for post_item_photo in post:
                                    # print(post_item_photo)
                                photo_post_count = 0
                                if post_item_photo["type"] == "photo":
                                        post_photo = post_item_photo['photo']
                                        # print(post_photo)

                                        sizes = post_photo['sizes']
                                        # print('блок sizes')
                                        # print(sizes,type(sizes))
                                        # print('\n\n')
                                        maxresolve = []
                                        # print('блок size1')
                                        for size in sizes:
                                            # print(size,type(size))
                                            width = size['width']
                                            # print(width)
                                            maxresolve.append(int(width))
                                        # print(maxresolve)
                                        maxresolve = str(max(maxresolve))
                                        # print(maxresolve)
                                        # print('блок size2')
                                        for size in sizes:
                                            url = size['url']
                                            if f'{str(maxresolve)}x' in url:
                                                post_photo=url
                                                print(post_photo)
                                                photo_post_count += 1
                                                photo_post_counter=str(post_id)+photo_post_count
                                                download_img(post_photo,photo_post_counter,post_id)
                                                break

                                elif post[0]['type'] == 'video':
                                    print("Видео пост")

                                    # формируем данные для составления запроса на получение ссылки на видео
                                    video_access_key = post[0]["video"]["access_key"]
                                    video_post_id = post[0]["video"]["id"]
                                    video_owner_id = post[0]["video"]["owner_id"]

                                    video_get_url = f"https://api.vk.com/method/video.get?videos={video_owner_id}_{video_post_id}_{video_access_key}&access_token={token}&v=5.81"

                                    async def fetch_data(url):
                                        async with aiohttp.ClientSession() as session:
                                            async with session.get(url) as response:
                                                response_json = await response.json()
                                                return response_json

                                    res = await fetch_data(video_get_url)
                                    photo_post_count += 1
                                    photo_post_counter = str(post_id) + photo_post_count
                                    video_url = res["response"]["items"][0]["player"]
                                    print(video_url)
                                    download_video(video_url,photo_post_counter,group_name)
                                else:print('link or audio')


                else:
                    print('нет вложений')
            except Exception:
                print('чтото не так ')




    with open(f'{group_name}/exists_posts_{group_name}.txt', 'w') as file:
            for item in fresh_posts_id:
                file.write(str(item)+'\n')

async def main():
    group_name = input('введите название группы:')
    await get_wall_posts(group_name)


if __name__ == "__main__":
        asyncio.run(main())


















# if __name__ == '__main__':


