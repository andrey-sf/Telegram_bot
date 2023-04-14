import telebot
from telebot import types
from config import TOKEN, exchanges
from extensions import ConvertionException, Convertor

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = f'Привет, <b>{message.from_user.first_name}</b>, введите имя валюты цену которой хочете узнать, затем имя валюты в которой надо узнать цену первой валюты и количество первой валюты. \nЧтобы узнать  информация о всех доступных валютах введите /values'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    start = types.KeyboardButton('/start')
    help = types.KeyboardButton('/help')
    values = types.KeyboardButton('/values')
    markup.add(start, help, values)
    bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров!')
        quote, base, amount = values
        total_base = Convertor.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
