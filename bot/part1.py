import os
import json

import youtube_dl
import requests

my_secret = 'ad96fe5b51f6d9c0bd241bc4cb01afc7af0e507be9eb7e2b0995a71aa35bd2fc263537ac736d8e41fd35b'


def get_wall_posts1(group_name):
    """Проверка, если файла не существует, значит это первый
    парсинг группы(отправляем все новые посты). Иначе начинаем
    проверку и отправляем только новые посты."""
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=199&access_token={my_secret}&v=5.157"
    req = requests.get(url)
    src = req.json()

    # проверяем существует ли директория с именем группы
    if os.path.exists(f"{group_name}"):
        print(f"Директория с именем {group_name} уже существует!")
    else:
        os.mkdir(group_name)

    # сохраняем данные в json файл, чтобы видеть структуру
    with open(f"{group_name}/{group_name}.json", "w",
              encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)

    # собираем ID новых постов в список
    fresh_posts_id = []
    posts = src["response"]["items"]

    for fresh_post_id in posts:
        fresh_post_id = fresh_post_id["id"]
        fresh_posts_id.append(fresh_post_id)

    if not os.path.exists(f"{group_name}/exist_posts_{group_name}.txt"):
        print("Файла с ID постов не существует, создаём файл!")

        with open(f"{group_name}/exist_posts_{group_name}.txt", "w") as file:
            for item in fresh_posts_id:
                file.write(str(item) + "\n")

        # извлекаем данные из постов
        for post in posts:

            post_id = post["id"]
            print(f"Отправляем пост с ID {post_id}")

            try:
                if "attachments" in post:
                    post = post["attachments"]

                    # забираем фото
                    if post[0]["type"] == "photo":

                        photo_quality = [
                            "photo_2560", "photo_1280", "photo_807",
                            "photo_604", "photo_130", "photo_75"
                        ]

                        if len(post) == 1:

                            for pq in photo_quality:
                                if pq in post[0]["photo"]:
                                    post_photo = post[0]["photo"][pq]
                                    print(f"Фото с расширением {pq}")
                                    print(post_photo)
                                    break
                        else:
                            for post_item_photo in post:
                                if post_item_photo["type"] == "photo":
                                    for pq in photo_quality:
                                        if pq in post_item_photo["photo"]:
                                            post_photo = post_item_photo[
                                                "photo"][pq]
                                            print(f"Фото с расширением {pq}")
                                            print(post_photo)
                                            break
                                else:
                                    print("Линк или аудио пост")
                                    break

            except Exception:
                print(f"Что-то пошло не так с постом ID {post_id}!")

    else:
        print("Файл с ID постов найден, начинаем выборку свежих постов!")
