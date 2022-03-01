import yadisk
import config
from pydantic import BaseModel
# from typing import NamedTuple
import requests
from loguru import logger
import asyncio

ya = yadisk.YaDisk(id=config.yadisk_id, secret=config.yadisk_password, token=config.token)


class YaDiskObject(BaseModel):
    name: str
    size: int
    file: str
    path: str
    type: str
    preview: str  # URL для скачивания превью
    mime_type: str  # тип файла image/jpeg


def get_public_meta(resource_link: str) -> YaDiskObject:
    obj = ya.get_public_meta(resource_link)
    logger.debug(obj)
    return YaDiskObject(obj.name, obj.size, obj.file, obj.path, obj.type, obj.preview, obj.mime_type)


def _get_public_listdir(public_dir_link, path='/на сайт'):
    list_dir = ya.public_listdir(public_key=public_dir_link, path=path, preview_size="L", limit=500)
    return list_dir


def download_image_from_public_dir(public_dir_link, img):
    ya.download_public(public_key=public_dir_link, path=f'/на сайт/{img.name}', file_or_path=img.name)
    return img.name


def create_img_list(public_dir_link, path='', img_list=[], names_list=[]) -> list():
    list_dir = _get_public_listdir(public_dir_link, path)
    for obj in list_dir:
        if obj.type == 'dir':
            create_img_list(public_dir_link, obj.path, img_list, names_list)
        elif obj.type == 'file' and obj.mime_type == 'image/jpeg':
            img = YaDiskObject(obj.name, obj.size, obj.file, obj.path, obj.type, obj.preview, obj.mime_type)
            if  obj.name not in names_list:
                img_list.append(img)
                names_list.append(obj.name)
            else:
                i = names_list.index(obj.name)
                if img_list[i].size > obj.size:
                    img_list.pop(i)
                    img_list.insert(i, img)

    del names_list
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


def download_file(img: YaDiskObject) -> str:
    with open(img.name, 'wb') as handle:
        response = requests.get(img.file, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    return img.name


def main():
    public_dir_link = "https://yadi.sk/i/oGDo85tTYHUVVA"