from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

service_b1 = KeyboardButton('г. Санкт-Петербург')
service_b2 = KeyboardButton('Ленинградская обл.')

kb_service: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)

kb_service.row(service_b1, service_b2)

customer_b1 = KeyboardButton('E&V3')
customer_b2 = KeyboardButton('E&V privet')

kb_customer: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)

kb_customer.row(customer_b1, customer_b2)