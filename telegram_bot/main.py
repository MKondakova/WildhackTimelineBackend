import telebot
import os

from config import TOKEN
from strings import WELCOME

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	
	bot.reply_to(message, WELCOME)

@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, WELCOME)

@bot.message_handler(commands=['post'])
def handle_post(message):
	title = message.text.split()
	if (len(title) <= 1):
		msg = bot.reply_to(message, "А заголовок где?")
		return
	print(' '.join(title[1:]))
	fact={ 'title': ' '.join(title[1:]) }
	msg = bot.reply_to(message, 'Жду дату в ответ на это сообщение')
	bot.register_next_step_handler(msg, handle_post_data, fact=fact)

def handle_post_data(message, fact):
	date = message.text.split()
	if (len(date) == 0):
		msg = bot.reply_to(message, "А дата где?")
		bot.register_next_step_handler(msg, handle_post_data, fact=fact)
		return 
	print(date[0])
	fact['date'] = date[0]
	msg = bot.reply_to(message, 'Жду текст в ответ на это сообщение')
	bot.register_next_step_handler(msg, handle_post_text, fact=fact)

def handle_post_text(message, fact):
	text = message.text
	if (len(text) == 0):
		msg = bot.reply_to(message, "А текст где?")
		bot.register_next_step_handler(msg, handle_post_text, fact=fact)
		return 
	print(text)
	fact['text'] = text
	msg = bot.reply_to(message, 'Молодец, так держать!')
	send_fact(fact)

def send_fact(fact):
	pass

	
@bot.message_handler(commands=['get'])
def get_news(message):
	news = 'blablablabla'
	bot.reply_to(message, news)

print('Started')
bot.polling()