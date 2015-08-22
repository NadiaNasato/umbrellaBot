from umbrellaBot_IRC import UmbrellaBot


def main():

#	server = 'registry-0.lohs.geneity'
	server = '192.168.0.8'
	port = 6667
	nickname = 'umbrellaBot'
#	channel = '#frontend'
	channel = '#test'

	bot = UmbrellaBot(channel, nickname, server, port)
	bot.start()

if __name__ == "__main__":
	main()

def test_console():
	"""
	Entry point for noun test console.
	"""
	message = raw_input("> ")

	print "Announcement: {}".format(umbrellaBot_IRC.get_forecast())
