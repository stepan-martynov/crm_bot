from pydantic import BaseModel
from tortoise import Tortoise, fields, run_async
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise.models import Model


class Entity(Model):
    name = fields.CharField(max_length=255)
    full_name = fields.TextField(null=True)
    legal_adress = fields.TextField(null=True)
    postal_adress = fields.TextField(null=True)
    tax_id = fields.CharField(max_length=15)
    kpp = fields.CharField(max_length=15, null=True)
    okpo = fields.CharField(max_length=15)

    # tax_id = fields.CharField(max_length=15)

    def __repr__(self):
        return f'{self.name} {self.full_name}'

    def __str__(self):
        return f'{self.name} {self.full_name}'


class Photosession(Model):
    name = fields.CharField(max_length=255)
    num = fields.IntField()


'''
class Deal(BaseModel):
    url: str
    service: str
    location: str
    broker: str
    price: str

    def serelize_for_doc(self):
        deal_data = {
            'link': self.url,
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
'''


async def run():
    await Tortoise.init(db_url="sqlite://:memory", modules={"models": ["__main__"]})
    await Tortoise.generate_schemas()
    Entity_pydantic = pydantic_model_creator(Entity)

    entity = await Entity.create(
        name="Puzzle",
        full_name="АО Пазл",
        legal_adres="Энгельса 4",
        postal_adres="Энгельса 114",
        tax_id="408907345",
        kpp="8275913749",
        okpo="8275913749"
    )
    print(await Entity.all())


if __name__ == '__main__':
    run_async(run())

    # link: str #URL
    # num: str  #contract_number
    # NUM: str #contract_number.upper()
    # date: str #contract_date
    # DATE: str #contract_date.upper()
    # cost: str #str(price)
    # letter_cost: str #litter_price
    # service_name: str #service_name
    # final_cost: str #str(price)
    # cur_date: str #cur_date
    # adress: str#f'{location}, {dir.name[4:]}'
    # photos: str #'{{photos}}'
    # num_of_photos: str#str(len(image_list)
