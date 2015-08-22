from __future__ import print_function
import forecaster


def main():

	host = '192.168.0.8'
	port = 6667
	nick = 'umbrellaBot'
	channels = ['#test']

	app = forecaster.get_app(
		host=host,
		port=port,
		nick=nick,
		channels=channels,
	)

	app.start()


def test_console():

	"""
	Entry point for test console
	"""
	try:
		while True:
			message = raw_input("> ")
			response = forecaster.get_forecast()
			print("Announcement: {}".format(response))
	except KeyboardInterrupt:
		exit(0)


if __name__ == "__main__":
	main()
