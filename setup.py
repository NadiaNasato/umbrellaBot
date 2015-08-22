from setuptools import setup

setup(
	name='umbrella_bot',
	version='0.1a',
	author="Nadia Nasato",
	packages=['umbrella_bot'],
	install_requires=[
		'irc',
	],
	entry_points={
		'console_scripts': [
			'umbrellaBot=umbrella_bot:main',
			'umbrella_bot=umbrella_bot:test_console',
		],
	},
)
