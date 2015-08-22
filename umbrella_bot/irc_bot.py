from irc.bot import SingleServerIRCBot

MESSAGE_THRESHOLD = 1

class IRCBotSettings(object):

	_settings = (
		('host',),
		('port', 6667),
		('nick', 'umbrellaBot'),
		('channels', ()),
	)

	def __init__(self, **kwargs):
		self.__dict__['_attrdict'] = dict()

		for setting in self._settings:
			if len(setting) == 2:
				key, default = setting
				self._attrdict[key] = kwargs.get(key, default)

			elif len(setting) == 1:
				try:
					key, = setting
					self._attrdict[key] = kwargs[key]
				except KeyError, e:
					raise Exception(
						"%s: Missing compulsory setting %s" % (self, e)
					)

	def __repr__(self):
		return "<{} {}>".format(self.__name__, self._attrdict)

	def __getattr__(self, attr):
		try:
			return self._attrdict[attr]
		except Keyerror:
			return super(IRCBotSettings, self).__getattr__(attr)

	def __setattr__(self, attr, val):
		# TODO is this the correct exception?
		raise Exception("%s instance does not support item assignment" % self)


class IRCApp(SingleServerIRCBot):

	def __init__(self, settings, handler):
		assert isinstance(settings, IRCBotSettings)
		self._handler_class = handler
		self._settings = settings

		host = settings.host
		port = settings.port
		nick = settings.nick

		super(IRCApp, self).__init__([(host, port)], nick, nick)

	def on_nicknameinuse(self, c, e):
		c.nick(c.get_nickname() + "_")

	def on_welcome(self, c, e):
		for channel in self._settings.channels:
			c.join(channel)

	def on_privmsg(self, c, e):
		nick = parse_nick(e)
		message = e.arguments[0]

		handler = self._handler_class(None, nick, message)
		self.run_handler(c, handler)

	def on_pubmsg(self, c, e):
		message = e.arguments[0]
		nick = parse_nick(e)
		channel = e.target

		my_nick = self.connection.get_nickname()
		if message.startswith('{}:'.format(my_nick)):
			message = message.split(':', 1)[1]

			handler = self._handler_class(channel, nick, message)
			self.run_handler(c, handler)

	def run_handler(self, c, handler):
		responses = handler.run()

		for resp in responses:
			resp.send_message(c)


class IRCResponse(object):
	def __init__(self, target, message):
		self.target = target
		self.message = message

	def send_message(self, c):
		c.privmsg(self.target, self.message)


class IRCHandler(object):
	def __init__(self, channel, nick, message):
		assert channel is None or channel.startswith('#')

		self.nick = nick
		self.channel = channel
		self.message = message

	def run(self):
		if self.channel is None:
			resp = self.priv_message(self.nick, self.message)
			default_target = self.nick
		else:
			resp = self.pub_message(self.channel, self.nick, self.message)
			default_target = self.channel

		return self._post_format_resp(resp, default_target)

	def _post_format_resp(self, resp, default_target):
		if resp is None:
			_resp = []

		elif isinstance(resp, basestring):
			_resp = [IRCResponse(target, resp)]

		elif isinstance(resp, list):
			_resp = list()
			for i, r in enumerate(resp):
				if isinstance(r, basestring):
					_resp.append(IRCResponse(target, r))

				elif isinstance(r, IRCResponse):
					_resp.append(r)

				else:
					raise Exception("Invalid item in resp at index %s: %s" % (i, r))
			return _resp

		else:
			raise Exception("Invalid response returned from handler: %s" % resp)

	def priv_message(self, nick, message):
		raise NotImplementedError()

	def pub_message(self, chanel, nick, message):
		raise NotImplementedError()


def parse_nick(e):
	return e.source.split('!')[0]
