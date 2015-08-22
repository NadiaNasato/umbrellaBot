import time
import random
import json

from urllib import urlopen

from irc.bot import SingleServerIRCBot

MESSAGE_THRESHOLD = 1

class UmbrellaBot(SingleServerIRCBot):

	last_msg_time = time.time()

	def __init__(self, channel, nickname, server, port=6667):
		super(UmbrellaBot, self).__init__([(server, port)], nickname, nickname)
		self.channel = channel

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		c.join(self.channel)

	def on_privmsg(self, c, e):
		nick = e.source.split('!')[0]
		message = e.arguments[0]
		self.do_command(c, nick, nick, message, True)

	def on_pubmsg(self, c, e):
		curr_time = time.time()

		if self.last_msg_time + MESSAGE_THRESHOLD >= curr_time:
			return

		self.last_msg_time = curr_time

		my_nick = self.connection.get_nickname()
		nick = e.source.split('!')[0]
		message = e.arguments[0]

		at_me = my_nick in message

		self.do_command(c, e.target, nick, message, at_me)

	def do_command(self, c, target, nick, message, at_me):
		
		if do_chance:
			forecast_descr = get_forecast()
			msg = "Announcement: {}".format(forecast_descr)

			c.privmsg(target, msg)

def get_forecast():
	url = urlopen('http://api.openweathermap.org/data/2.5/forecast?q=London,uk&api_key=109ae645f9be1d0b44f7db0675b90cbf').read()
	url = json.loads(url)

	return url.get('list')[0].get('weather')[0].get('description')

def do_chance():
	return random.random() > 0.6
