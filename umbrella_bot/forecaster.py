import json
from urllib import urlopen

from umbrella_bot.irc_bot import IRCApp, IRCHandler, IRCBotSettings


class ForecastHandle(IRCHandler):
	def priv_message(self, nick, message):
		return "Go away!"

	def pub_message(self, channel, nick, message):
		forecast = get_forecast()
		return "{}: {}".format(nick, forecast)


def get_app(host, port, nick, channels):
	settings = IRCBotSettings(
		host=host, port=port, nick=nick, channels=channels
	)
	app = IRCApp(settings, ForecastHandle)
	return app


def get_forecast():
	url = urlopen('http://api.openweathermap.org/data/2.5/forecast?q=London,uk&api_key=109ae645f9be1d0b44f7db0675b90cbf').read()
	url = json.loads(url)

	return url.get('list')[0].get('weather')[0].get('description')

