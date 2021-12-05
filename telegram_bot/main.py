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

exit_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
itembtn11 = telebot.types.KeyboardButton('exit')
exit_markup.add(itembtn11)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, WELCOME, reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
	bot.send_message(message.chat.id, WELCOME, reply_markup=markup)

@bot.message_handler(commands=['post_fact'])
def handle_post(message, first = True):
	if message.text == 'exit':
		bot.send_message(message.chat.id, 'Возврат в меню', reply_markup=markup)
		return
	title = message.text.split()
	if (len(title) <= 1 and first or len(title) == 0):
		msg = bot.send_message(message.chat.id, "Введите заголовок", reply_markup=exit_markup)
		bot.register_next_step_handler(msg, handle_post, first=False)
		return
	fact={ 'title': ' '.join(title[1:] if first else title) }
	msg = bot.send_message(message.chat.id, 'Жду дату в формате dd.mm.yyyy в ответ на это сообщение', reply_markup=exit_markup)
	bot.register_next_step_handler(msg, handle_post_data, fact=fact)

def handle_post_data(message, fact):
	if message.text == 'exit':
		bot.send_message(message.chat.id, 'Возврат в меню', reply_markup=markup)
		return
	date = message.text.split()
	if (len(date) == 0):
		msg = bot.send_message(message.chat.id, "Введите дату в формате dd.mm.yyyy", reply_markup=exit_markup)
		bot.register_next_step_handler(msg, handle_post_data, fact=fact)
		return 
	dateList = date[0].split('.')
	if (len(dateList) != 3):
		msg = bot.send_message(message.chat.id, "Введите дату в формате dd.mm.yyyy", reply_markup=exit_markup)
		bot.register_next_step_handler(msg, handle_post_data, fact=fact)
		return
	try:
		dateList.reverse()
		datetime.date.fromisoformat('-'.join(dateList))
	except:
		msg = bot.send_message(message.chat.id, "Введите дату в формате dd.mm.yyyy", reply_markup=exit_markup)
		bot.register_next_step_handler(msg, handle_post_data, fact=fact)
		return
	fact['date'] = '-'.join(dateList)
	msg = bot.send_message(message.chat.id, 'Жду текст в ответ на это сообщение', reply_markup=exit_markup)
	bot.register_next_step_handler(msg, handle_post_text, fact=fact)

def handle_post_text(message, fact):
	if message.text == 'exit':
		bot.send_message(message.chat.id, 'Возврат в меню', reply_markup=markup)
		return
	text = message.text
	if (len(text) == 0):
		msg = bot.send_message(message.chat.id, "Введите текст", reply_markup=exit_markup)
		bot.register_next_step_handler(msg, handle_post_text, fact=fact)
		return 
	print(text)
	fact['text'] = text
	msg = bot.send_message(message.chat.id, 'Добавьте источник факта', reply_markup=exit_markup)
	bot.register_next_step_handler(msg, handle_post_source, fact=fact)

def handle_post_source(message, fact):
	if message.text == 'exit':
		bot.send_message(message.chat.id, 'Возврат в меню', reply_markup=markup)
		return
	text = message.text
	if (len(text) == 0 or not validators.url(text)):
		msg = bot.send_message(message.chat.id, "Введите корректный источник", reply_markup=exit_markup)
		bot.register_next_step_handler(msg, handle_post_source, fact=fact)
		return 
	print(text)
	fact['source'] = text
	msg = bot.send_message(message.chat.id, 'Введите важность в формате от 0 до 10.', reply_markup=exit_markup)
	bot.register_next_step_handler(msg, handle_post_importance, fact=fact)


def handle_post_importance(message, fact):
	if message.text == 'exit':
		bot.send_message(message.chat.id, 'Возврат в меню', reply_markup=markup)
		return
	importance = message.text
	if (len(importance) == 0):
		msg = bot.send_message(message.chat.id, 'Введите важность в формате от 0 до 10.', reply_markup=exit_markup)
		bot.register_next_step_handler(msg, handle_post_importance, fact=fact)
		return
	try:
		importance = int(importance)
		if (importance < 0 or importance > 10):
			raise 
	except:
		msg = bot.send_message(message.chat.id, 'Введите важность в формате от 0 до 10.', reply_markup=exit_markup)
		bot.register_next_step_handler(msg, handle_post_importance, fact=fact)
		return
	fact['importance'] = importance
	bot.reply_to(message, "Данные отправлены на сервер")
	code = send_fact(fact)
	results = "Записано." if code else "Что-то не так..."
	bot.send_message(message.chat.id, results, reply_markup=markup)


def send_fact(fact):
	payload = json.dumps(fact, ensure_ascii=False)
	response = requests.post('http://127.0.0.1:8000/facts/',  data=payload.encode('utf-8'),
                  headers={'Content-Type': 'application/json; charset=utf-8'})

	return response.status_code == 200

	
@bot.message_handler(commands=['get_next_news'])
def get_next_news(message):
	response = requests.get('http://127.0.0.1:8000/news/')
	news_json = json.loads(response.json())
	if 'error' in news_json:
		bot.send_message(message.chat.id, news_json['error'], reply_markup=markup)
		return
	news_json = news_json[0]
	bot.send_message(message.chat.id, f'{news_json["fields"]["title"]}: {news_json["fields"]["source"]} ({news_json["fields"]["date"]})', reply_markup=markup)


@bot.message_handler(commands=['get_facts'])
def get_facts(message):
	response = requests.get('http://127.0.0.1:8000/facts/')
	list = json.loads(response.json())
	strings = [ f'{fact["pk"]}. {fact["fields"]["title"]} ({fact["fields"]["source"]})' for fact in list]
	bot.send_message(message.chat.id, '\n'.join(strings), reply_markup=markup)
	


print('Started')
bot.polling()