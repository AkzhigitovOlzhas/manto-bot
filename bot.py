import telebot
import config
import random
import requests
from telebot import types
from more_func import weather

bot = telebot.TeleBot(config.TOKEN)

# Кнопки
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton("Цитата")
button2 = types.KeyboardButton("Анекдот")
button3 = types.KeyboardButton("Мемы")
button4 = types.KeyboardButton("Помощь")
button5 = types.KeyboardButton("Музыка для души❤")
button6 = types.KeyboardButton("Love калькулятор")

markup.add(button1, button2, button3, button4,button5,button6)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('sticker/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id,
                     "Привет <b>{0.first_name}!</b> Меня зовут <b>{1.first_name}</b>.<i>\n<b>Я создан чтобы "
                     "развлекать тебя если тебе скучно</b></i>\n".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.send_message(616639915, 'Написал(а): {0.first_name}:@{0.username}:{0.id}\n'.format(message.from_user,bot.get_me()))
    fileID = message.photo[-1].file_id
    bot.send_photo(616639915,fileID)


@bot.message_handler(content_types=['text'])
def main_func(message):
    try:
        bot.send_message(616639915,'Написал(а): {0.first_name}:@{0.username}:{0.id}\n'.format(message.from_user, bot.get_me()) + message.text+'\n')
        if message.chat.type == 'private':
            if message.text.lower() == 'цитата':
                # Адрес api метода для запроса get
                quote = requests.get(
                    'https://api.forismatic.com/api/1.0/?method=getQuote&format=json&jsonp=parseQuote&lang=ru')
                # Отправляем get request (запрос GET)
                bot.send_message(message.chat.id,
                                 '<i>"' + str(quote.json()["quoteText"]) + '"</i>\n\n' + str(quote.json()["quoteAuthor"]),
                                 parse_mode='html')
                bot.send_message(616639915,
                                 '<i>"' + str(quote.json()["quoteText"]) + '"</i>\n\n' + str(quote.json()["quoteAuthor"]),
                                 parse_mode='html')
            elif message.text.lower() == 'анекдот':
                joke = requests.get('http://rzhunemogu.ru/Rand.aspx?CType=1')
                bot.send_message(message.chat.id, str(
                    joke.text.replace('<?xml version="1.0" encoding="utf-8"?><root><content>', '').replace(
                        '</content></root>', '')))
                bot.send_message(616639915, str(
                    joke.text.replace('<?xml version="1.0" encoding="utf-8"?><root><content>', '').replace(
                        '</content></root>', '')))
            elif message.text.lower().split()[0] == 'weather' or message.text.lower().split()[0] == 'погода':
                try:
                    bot.send_message(message.chat.id, 'Погода в городе ' + message.text.lower().split()[1] + ' ' + ' ' +
                                     str(weather.current_weather(message.text.lower().split()[1])) + '  градусов')
                    bot.send_message(616639915, 'Погода в городе ' + message.text.lower().split()[1] + ' ' + ' ' +
                                     str(weather.current_weather(message.text.lower().split()[1])) + '  градусов')
                except Exception as e:
                    bot.send_message(message.chat.id, 'Ошибка! Возможно не верный ввод.')
                    bot.send_message(616639915, 'Ошибка! Возможно не верный ввод.')
            elif message.text == 'Факты':
                bot.send_message(message.chat.id, 'Еще не готово')
                bot.send_message(616639915, 'Еще не готово')
            elif message.text == 'Love калькулятор':
                bot.send_message(message.chat.id, 'Отправте боту сообщение "Love Любое_Имя + Любое_Имя"')
                bot.send_message(616639915, 'Отправте боту сообщение "Love Любое_Имя + Любое_Имя"')
            elif message.text.lower() == 'мемы':
                meme = 'http://admem.ru/content/images/' + str(random.randint(1391093637, 1391119653)) + '.jpg'
                bot.send_photo(message.chat.id, meme)
                bot.send_photo(616639915, meme)
            elif message.text.lower() == 'cat' or message.text.lower() == 'кошка':
                cat = requests.get('https://aws.random.cat/meow')
                bot.send_photo(message.chat.id, cat.json()['file'])
                bot.send_photo(616639915, cat.json()['file'])
            elif message.text.lower() == 'dog' or message.text.lower() == 'собака':
                dog = requests.get('https://random.dog/woof.json')
                bot.send_photo(message.chat.id, dog.json()['url'])
                bot.send_photo(616639915, dog.json()['url'])
            elif message.text.lower() == 'fox' or message.text.lower() == 'лиса':
                fox = requests.get('https://randomfox.ca/floof/')
                bot.send_photo(message.chat.id, fox.json()['image'])
                bot.send_photo(616639915, fox.json()['image'])

            elif str(message.text).lower() == 'author' or str(message.text).lower() == 'автор':
                bot.send_message(message.chat.id, 'Разработал: Акжигитов Олжас\nПи-4-19')
                bot.send_message(616639915, 'Разработал: Акжигитов Олжас\nПи-4-19')
            elif message.text.split()[0].lower() == 'курс' or message.text.split()[0].lower() == 'rate':
                try:
                    currency1 = str(message.text.split()[1].split('/')[0]).upper()
                    currency2 = str(message.text.split()[1].split('/')[1]).upper()
                    url = 'https://v6.exchangerate-api.com/v6/4df7e119c2d27098d8c369ac/latest/' + currency1
                    rate = requests.get(url)
                    bot.send_message(message.chat.id,
                                     'Курс: 1 ' + currency1 + ' стоит ' + str(
                                         rate.json()['conversion_rates'][currency2]) + ' ' + currency2)
                    bot.send_message(616639915,
                                     'Курс: 1 ' + currency1 + ' стоит ' + str(
                                         rate.json()['conversion_rates'][currency2]) + ' ' + currency2)

                except Exception as e:
                    bot.send_message(message.chat.id, 'Ошибка! Возможно не верный ввод.')
                    bot.send_message(616639915, 'Ошибка! Возможно не верный ввод.')
            elif str(message.text).split()[0].lower() == 'love' or str(message.text).split()[0].lower() == 'лав':
                try:
                    if str(message.text).split()[1].lower() == 'олжас' or str(message.text).split()[3].lower() == 'олжас':
                        x = random.randint(200, 1000)
                        bot.send_message(message.chat.id, message.text.split()[1] + ' + ' +
                                         message.text.split()[3] + ' = ' + str(x) + '%❤')
                        bot.send_message(616639915, message.text.split()[1] + ' + ' +
                                         message.text.split()[3] + ' = ' + str(x) + '%❤')
                    else:
                        x = random.randint(1, 100)
                        bot.send_message(message.chat.id, str(message.text).split()[1] + ' + ' +
                                         str(message.text).split()[3] + ' = ' + str(x) + '%❤')
                        bot.send_message(616639915, str(message.text).split()[1] + ' + ' +
                                         str(message.text).split()[3] + ' = ' + str(x) + '%❤')

                except Exception as e:
                    bot.send_message(message.chat.id, 'Ошибка! Вводите:\nlove name1 + name2 \nили \nлав name1 + name2')
                    bot.send_message(616639915, 'Ошибка! Вводите:\nlove name1 + name2 \nили \nлав name1 + name2')
            elif message.text == 'Помощь':
                bot.send_message(message.chat.id,
                                 'Привет! Если хочешь полностью испытать бота то попробуй следующие команды:\n\n'
                                 '1) Чтобы загадать случайное число просто напиши \'Число от 1 до 100\' или \'rand 20:100\' диапазон можно задать любой.'
                                 '\n\n2) Ты можешь написать в чат одного из трех животных (собака, кошка, лиса) и бот скинет фотографию этого животного (можно писать на английском)'
                                 '\n\n3) Ты можешь узнать курс валют командой \'Курс usd/rub\''
                                 '\n\n4) Ты можешь узнать погоду написав \'Погода Бишкек\''
                                 '\n\n5) Тут даже есть love калькулятор)) Напиши:\'лав имя1 + имя2 или love имя1 + имя2\''
                                 '\n\nИ еще регистр букв не учитывается ты можешь писать с заглавными буквами или прописными :D\n\n')
                bot.send_message(616639915,
                                 'Привет! Если хочешь полностью испытать бота то попробуй следующие команды:\n\n'
                                 '1) Чтобы загадать случайное число просто напиши \'Число от 1 до 100\' или \'rand 20:100\' диапазон можно задать любой.'
                                 '\n\n2) Ты можешь написать в чат одного из трех животных (собака, кошка, лиса) и бот скинет фотографию этого животного (можно писать на английском)'
                                 '\n\n3) Ты можешь узнать курс валют командой \'Курс usd/rub\''
                                 '\n\n4) Ты можешь узнать погоду написав \'Погода Бишкек\''
                                 '\n\n5) Тут даже есть love калькулятор)) Напиши:\'лав имя1 + имя2 или love имя1 + имя2\''
                                 '\n\nИ еще регистр букв не учитывается ты можешь писать с заглавными буквами или прописными :D\n\n')

            elif str(message.text).split()[0].lower() == 'музыка':
                bot.send_message(message.chat.id, 'Сорян скоро появиться:d (это не точно)')
                bot.send_message(616639915, 'Сорян скоро появиться:d (это не точно)')
            elif str(message.text).split()[0].lower() == 'rand' or str(message.text).split()[0].lower() == 'число':
                try:
                    if str(message.text).split()[0].lower() == 'число':
                        x = message.text.split()
                        bot.send_message(message.chat.id, 'Случайное число: ' + str(random.randint(int(x[2]), int(x[4]))))
                        bot.send_message(616639915, 'Случайное число: ' + str(random.randint(int(x[2]), int(x[4]))))
                    else:
                        x = message.text.split()[1]
                        bot.send_message(message.chat.id, 'Случайное число: ' + str(
                            random.randint(int(x.split(':')[0]), int(x.split(':')[1]))))
                        bot.send_message(616639915, 'Случайное число: ' + str(
                            random.randint(int(x.split(':')[0]), int(x.split(':')[1]))))

                except Exception as e:
                    bot.send_message(message.chat.id,
                                     'Ошибка! Возможно не верный ввод.\nВведите запрос \'rand 1:10\', где числа 1 и 10 диапазон \nили \'Число от 1 до 10\'')
                    bot.send_message(616639915,
                                     'Ошибка! Возможно не верный ввод.\nВведите запрос \'rand 1:10\', где числа 1 и 10 диапазон \nили \'Число от 1 до 10\'')
            elif message.chat.id == 616639915:
                try:
                    if str(message.text).split()[0].lower() == 'написать':
                        bot.send_message(message.text.split()[1].lower(), str(message.text).split('#')[1])
                        bot.send_message(616639915, str(message.text).split('#')[1])
                except Exception as e:
                    bot.send_message(616639915, 'Не удалось отправить сообщение')
            else:
                bot.send_message(message.chat.id, 'Я тебя не понимаю')
                bot.send_message(616639915, 'Я тебя не понимаю')
    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла системная ошибка, попробуйте еще раз!')
        bot.send_message(616639915, 'Произошла системная ошибка, попробуйте еще раз!')

print('Бот запущен')
# Run
bot.polling(none_stop=True)
