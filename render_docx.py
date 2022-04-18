import os
from datetime import datetime
from PIL import Image
from loguru import logger
import random

from docx import Document
from docxtpl import DocxTemplate
from docx.shared import Cm
from babel.dates import format_date
from num2words import num2words

from yadisk_api import get_public_meta, create_img_list, download_preview


# location = ""
# doc_template = ""
# service_name = ""

# =========== INPUT ===========

# doc_template = "E&V3 private.docx"
doc_template = "akt_peredachI_reynaers.docx"
# location = "Ленинградская обл."
# service_name = 'Профессиональная фотосъемка загородной недвижимости'

URL = "https://disk.yandex.ru/d/P2tu4u-1JR0KNg"
broker = "Анна Романова"
price = 2000

# ========== END INPUT ==========

doc_template = doc_template or "E&V3.docx"
DOCX_TEMPLATE_PATH = os.path.join(os.getcwd(), doc_template)

dir = get_public_meta(URL)

litter_price = num2words(price, lang="ru")
contract_number = f'ev-sm-{dir.name.split(" ")[0]}'  # TODO заменить на порядковый номер контракта из ДБ


def filter_img_list(image_list: list, img_filter: str) -> list:
    l = []
    img_filter = img_filter.split(", ")
    logger.debug(img_filter)
    for img in img_filter:
        for raw_img in image_list:
            if img in raw_img.name:
                l.append(raw_img)
    logger.debug(l)
    return l


def date_format_to_ru(d: datetime) -> str:
    return format_date(d, format='long', locale='ru')[:-3]


image_list = create_img_list(URL)
image_list = filter_img_list(image_list, img_filter) if img_filter else image_list

shooting_date = random.choice(image_list).name[:8]
contract_date = date_format_to_ru(datetime.strptime(shooting_date, "%Y%m%d"))  # '9 сентября 2020'
short_date = datetime.strptime(shooting_date, "%Y%m%d").strftime("%d.%m.%Y")
cur_date = date_format_to_ru(datetime.now())

location = location or 'Санкт-Петербург'
service_name = service_name or "Профессиональная фотосъемка недвижимости"
context = {
    'link': URL,
    'num': contract_number,
    'NUM': contract_number.upper(),
    'date': contract_date,
    'DATE': contract_date.upper(),
    'cost': str(price),
    'letter_cost': litter_price,
    'service_name': service_name,
    'final_cost': str(price),
    'cur_date': cur_date,
    'adress': f'{location}, {dir.name[4:]}',
    'photos': '{{photos}}',
    'num_of_photos': str(len(image_list))
}


def add_images(image_list, doc):
    for p in doc.paragraphs:
        if '{{photos}}' in p.text:
            p.text = ''
            run = p.add_run()
            for image in image_list:
                f = download_preview(image)
                try:
                    with Image.open(f) as img:
                        img.save(f, "JPEG")
                        if img.width > img.height:
                            run.add_picture(f, width=Cm(2.7))
                        else:
                            run.add_picture(f, height=Cm(1.8))
                    os.remove(f)
                except Exception as e:
                    logger.error(e)

    return doc


if __name__ == '__main__':
    doc = DocxTemplate(DOCX_TEMPLATE_PATH)
    # doc.render(context)
    # file_name = f"{contract_number}.docx"
    # doc.save(file_name)
    #
    # pprint.pprint(context)
    #
    # print('\nВывод для exel')
    # str_to_exel = f'{short_date}\t\t{dir.name[4:]}\t\t\t{broker}\t\t\t{contract_number}' \
    #               f' не оплачено\t{str(price)}\t\t{str(URL)}\n\n' \
    #               f'\n Для портала:\n' \
    #               f'Ссылка на объект: {URL}\n' \
    #               f'Ответственный за фотосессию: {broker}\n' \
    #               f'{contract_number}'
    #
    # print(str_to_exel)

    # doc = Document(file_name)
    doc = Document(doc_template)
    add_images(image_list, doc)
    # doc.save(file_name)
    doc.save(doc_template)
    # print(upload_file(URL, file_name))

    # os.remove(file_name)
