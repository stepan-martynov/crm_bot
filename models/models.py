from pydantic import BaseModel

class Deal(BaseModel):
    link: str #URL
    num: str  #contract_number
    NUM: str #contract_number.upper()
    date: str #contract_date
    DATE: str #contract_date.upper()
    cost: str #str(price)
    letter_cost: str #litter_price
    service_name: str #service_name
    final_cost: str #str(price)
    cur_date: str #cur_date
    adress: str#f'{location}, {dir.name[4:]}'
    photos: str #'{{photos}}'
    num_of_photos: str#str(len(image_list)