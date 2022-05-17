import yadisk
import config
from dataclasses import dataclass, field, asdict
from typing import NamedTuple
import requests
from loguru import logger

ya = yadisk.YaDisk(id=config.yadisk_id, secret=config.yadisk_password, token=config.ya_token)


@dataclass
class YaDiskObject:
    name: str
    size: int = field(repr=False)
    file: str = field(repr=False)
    path: str
    type: str = field(repr=False)
    preview: str  # URL для скачивания превью
    mime_type: str  # тип файла image/jpeg


def get_public_meta(resource_link: str) -> YaDiskObject:
    obj = ya.get_public_meta(resource_link)
    return YaDiskObject(obj.name, obj.size, obj.file, obj.path, obj.type, obj.preview, obj.mime_type)


def _get_public_listdir(public_dir_link, path='/на сайт'):
    list_dir = ya.public_listdir(public_key=public_dir_link, path=path, preview_size="L", limit=500)
    return list_dir


def download_image_from_public_dir(public_dir_link, img):
    ya.download_public(public_key=public_dir_link, path=f'/на сайт/{img.name}', file_or_path=img.name)
    return img.name


def create_img_list(public_dir_link, path='', img_list: list = [], names_list: list = []) -> list():
    list_dir = _get_public_listdir(public_dir_link, path)
    for obj in list_dir:
        if obj.type == 'dir':
            create_img_list(public_dir_link, obj.path, img_list, names_list)
        elif obj.type == 'file' and obj.mime_type == 'image/jpeg':
            img = YaDiskObject(obj.name, obj.size, obj.file, obj.path, obj.type, obj.preview, obj.mime_type)
            if obj.name not in names_list:
                img_list.append(img)
                names_list.append(obj.name)
            else:
                i = names_list.index(obj.name)
                if img_list[i].size > obj.size:
                    img_list.pop(i)
                    img_list.insert(i, img)

    return img_list


def download_preview(img: YaDiskObject) -> str:
    with open(img.name, 'wb') as handle:
        response = requests.get(img.preview, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    return img.name


ya_dir = {
    'name': '20211111-SM-SMD08120.jpg',
    'size': 844264, 'file': 'https://downloader.disk.yandex.ru/disk/23a5f67fb53cd9e5f57d22186b8710c2baf5898b012e1e556c6af0d278a28a28/626d528a/kv0YqZEPvVB11OQiueeH5gQK9u78njdP3eGsHI0c_PkCJuiCuENvwfWR68ypaDnpwttRIrBXmHZMepbVaonFZA%3D%3D?uid=0&filename=20211111-SM-SMD08120.jpg&disposition=attachment&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&fsize=844264&hid=ccfce4cc60498254bc0fc5803d194426&media_type=image&tknv=v2&etag=94fb37a78308bed937ff42e34572bd5d',
    'path': '/',
    'type': 'file',
    'preview': 'https://downloader.disk.yandex.ru/preview/d07489a61bf76ba11bde2dbdc96c3df4a0e018aa7e3b78587b110d163a6c24fb/626d528a/RE-uM-63fsnsBWeaSpcD6g4MN1VCdMxIaca_HA2s-br3t4EGGFq__asxaB7d0PBiJDKzH4RPQKIXNeJCZ4-4_g%3D%3D?uid=0&filename=20211111-SM-SMD08120.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=S&crop=0',
    'mime_type':
    'image/jpeg'
}

def main():
    public_dir_link: str = "https://yadi.sk/i/oGDo85tTYHUVVA"
    logger.info(type(get_public_meta(public_dir_link)))
    logger.info(get_public_meta(public_dir_link))


if __name__ == "__main__":
    main()