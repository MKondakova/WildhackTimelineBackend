import datetime
from django.http import response
import telebot
import requests
import json
import validators

from config import TOKEN
from strings import WELCOME

bot = telebot.TeleBot(TOKEN, parse_mode=None)

markup =  telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
itembtn1 = telebot.types.KeyboardButton('/post_fact')
itembtn2 = telebot.types.KeyboardButton('/get_next_news')
itembtn3 = telebot.types.KeyboardButton('/get_facts')
markup.add(itembtn1, itembtn2, itembtn3)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, WELCOME, reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
	bot.send_message(message.chat.id, WELCOME, reply_markup=markup)

@bot.message_handler(commands=['post_fact'])
def handle_post(message, first = True):
	title = message.text.split()
	if (len(title) <= 1 and first or len(title) == 0):
		msg = bot.reply_to(message, "Введите заголовок")
		bot.register_next_step_handler(msg, handle_post, first=False)
		return
	fact={ 'title': ' '.join(title[1:] if first else title) }
	msg = bot.reply_to(message, 'Жду дату в формате dd.mm.yyyy в ответ на это сообщение')
	bot.register_next_step_handler(msg, handle_post_data, fact=fact)

def handle_post_data(message, fact):
	date = message.text.split()
	if (len(date) == 0):
		msg = bot.reply_to(message, "Введите дату в формате dd.mm.yyyy")
		bot.register_next_step_handler(msg, handle_post_data, fact=fact)
		return 
	dateList = date[0].split('.')
	if (len(dateList) != 3):
		msg = bot.reply_to(message, "Введите дату в формате dd.mm.yyyy")
		bot.register_next_step_handler(msg, handle_post_data, fact=fact)
		return
	try:
		dateList.reverse()
		datetime.date.fromisoformat('-'.join(dateList))
	except:
		msg = bot.reply_to(message, "Введите дату в формате dd.mm.yyyy")
		bot.register_next_step_handler(msg, handle_post_data, fact=fact)
		return
	fact['date'] = '-'.join(dateList)
	msg = bot.reply_to(message, 'Жду текст в ответ на это сообщение')
	bot.register_next_step_handler(msg, handle_post_text, fact=fact)

def handle_post_text(message, fact):
	text = message.text
	if (len(text) == 0):
		msg = bot.reply_to(message, "Введите текст")
		bot.register_next_step_handler(msg, handle_post_text, fact=fact)
		return 
	print(text)
	fact['text'] = text
	msg = bot.reply_to(message, 'Добавьте источник факта')
	bot.register_next_step_handler(msg, handle_post_source, fact=fact)

def handle_post_source(message, fact):
	text = message.text
	if (len(text) == 0 or not validators.url(text)):
		msg = bot.reply_to(message, "Введите корректный источник")
		bot.register_next_step_handler(msg, handle_post_source, fact=fact)
		return 
	print(text)
	fact['source'] = text
	msg = bot.reply_to(message, 'Введите важность в формате от 0 до 10.')
	bot.register_next_step_handler(msg, handle_post_importance, fact=fact)


def handle_post_importance(message, fact):
	importance = message.text
	if (len(importance) == 0):
		msg = bot.reply_to(message, 'Введите важность в формате от 0 до 10.')
		bot.register_next_step_handler(msg, handle_post_importance, fact=fact)
		return
	try:
		importance = int(importance)
		if (importance < 0 or importance > 10):
			raise 
	except:
		msg = bot.reply_to(message, 'Введите важность в формате от 0 до 10.')
		bot.register_next_step_handler(msg, handle_post_importance, fact=fact)
		return
	fact['importance'] = importance
	bot.reply_to(message, "Данные отправлены на сервер")
	code = send_fact(fact)
	results = "Записано." if code else "Что-то не так..."
	bot.send_message(message.chat.id, results, reply_markup=markup)


def send_fact(fact):
	payload = json.dumps(fact, ensure_ascii=False)
	response = requests.post('http://127.0.0.1:8000/moderator/',  data=payload.encode('utf-8'),
                  headers={'Content-Type': 'application/json; charset=utf-8'})

	return response.status_code == 200

	
@bot.message_handler(commands=['get_next_news'])
def get_next_news(message):
	#todo добавить запрос и его правильно выводить
	news = 'blablablabla'
	bot.send_message(message.chat.id, news, reply_markup=markup)



@bot.message_handler(commands=['get_facts'])
def get_facts(message):
	response = requests.get('http://127.0.0.1:8000/moderator/')
	list = json.loads(response.json())
	bot.send_message(message.chat.id, "скоро", reply_markup=markup) #todo
	


print('Started')
bot.polling()