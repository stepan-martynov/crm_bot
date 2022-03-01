from pydantic import BaseModel

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