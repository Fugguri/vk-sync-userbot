from pyrogram import Client, types, enums
from vk_methods import VkMethods
import os

vkontakte = VkMethods()
cfg = vkontakte.load_config_from_json()

client = Client(name=cfg["phone"],
                api_id=cfg["api_id"],
                api_hash=cfg["api_hash"],
                phone_number=cfg["phone"],
                )

last_photos = list()
last_video = list()


@client.on_message()
async def handle(client: Client, message: types.Message):

    if message.chat.id != cfg["channel_id"]:
        return
    if message.text:
        vkontakte.WallPost(message.text)
        return

    if not message.media:
        return

    media_type = message.media

    match media_type:
        case enums.MessageMediaType.PHOTO:
            caption = None
            photos = list()
            try:
                global last_photos
                mg = await client.get_media_group(message.chat.id, message.id)
                photos_id = [m.photo.file_id for m in mg]
                if last_photos == set(photos_id):
                    return
                last_photos = set(photos_id)
                for m in mg:
                    if m.caption:
                        caption = m.caption
                    photo = await client.download_media(m)
                    photos.append(photo)
                vkontakte.WallPost(caption, photos)
            except:
                photo = await client.download_media(message)
                vkontakte.WallPost(message.caption, [photo,])
                os.remove(photo)
            finally:
                for photo in photos:
                    os.remove(photo)
            return

        case enums.MessageMediaType.VIDEO:
            caption = None
            videos = list()
            try:
                global last_video
                mg = await client.get_media_group(message.chat.id, message.id)
                video_id = [m.video.file_id for m in mg]
                if last_video == set(video_id):
                    return
                last_video = set(video_id)
                for m in mg:
                    if m.caption:
                        caption = m.caption
                    video = await client.download_media(m)
                    videos.append(video)
                vkontakte.WallPost(caption, VideoPaths=videos)
            except:
                video = await client.download_media(message)
                vkontakte.WallPost(message.caption, VideoPaths=[video,])
                os.remove(video)
            finally:
                for video in videos:
                    os.remove(video)
            return

print("starting")
client.run()
