NAME=umbrellaBot

all: build_and_run
	
build_and_run:
	make build
	make run

build:
	sudo docker-compose build

run:
	sudo docker-compose up

console:
	sudo docker-compose run $(NAME) umbrellaBot_console

build_and_console:
	make build
	make console

# The following are non-docker options

nd_run:
	python umbrella_bot/umbrella_bot.py

nd_console:
	python -c "from umbrella_bot import test_console as f; f()"
