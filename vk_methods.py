import json
import requests


class VkMethods:
    def __init__(self):
        self.cfg = self.load_config_from_json()
        self.v = self.cfg['v']
        self.group_id = self.cfg['group_id']
        self.access_token = self.cfg['access_token']
        self.from_group = self.cfg['from_group']
        self.getWallUploadServer = self.cfg['getWallUploadServer']

    @staticmethod
    def load_config_from_json():
        return json.load(open('config.json'))

    def WallPost(self, Message: str, PhotoPaths: list = None):
        BoxPhotoLink = []
        PhotoLink = None
        if PhotoPaths:
            response = requests.get('https://api.vk.com/method/photos.getWallUploadServer',
                                    params={'access_token': self.access_token, 'group_id': self.group_id, 'v': self.v})
            upload_url = response.json()['response']['upload_url']
            for Path in PhotoPaths:
                request = requests.post(
                    upload_url, files={'photo': open(Path, "rb")})
                photo_id = requests.get('https://api.vk.com/method/photos.saveWallPhoto',
                                        params={'access_token': self.access_token,
                                                'group_id': self.group_id,
                                                'photo': request.json()["photo"],
                                                'server': request.json()['server'],
                                                'hash': request.json()['hash'],
                                                'v': self.v})
                photo_owner_id = str(
                    photo_id.json()['response'][0]['owner_id'])
                photo_id = str(photo_id.json()['response'][0]['id'])
                photoLink = 'photo' + photo_owner_id + '_' + photo_id
                BoxPhotoLink.append(photoLink)

            PhotoLink = ",".join(BoxPhotoLink)
        # # Формируем параметры для размещения картинки в группе и публикуем её
        if PhotoPaths:
            params = {'access_token': self.access_token,
                      'owner_id': -self.group_id,
                      'from_group': 1,
                      'message': Message,
                      'attachments': PhotoLink,
                      'v': self.v}
        else:
            params = {'access_token': self.access_token,
                      'owner_id': -self.group_id,
                      'from_group': 1,
                      'message': Message,
                      'v': self.v}

        res = requests.get('https://api.vk.com/method/wall.post', params)
        print(res.json())
        return res.json()
