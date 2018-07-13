# Nano Lottery
A lottery for Nano currency with the purpose of funding the goals of different projects. The lottery website and lottery itself is completely open source on Github.

# Running
Nano lottery is written in Python-3.6.5 and the library requirements can be found in requirements.txt. The main interest is Flask, which is used to display the web page and show users the lottery.

The Flask app can easily be edited along with the templates in the template folder if additional features are wanted.
Another interest would be the Nano node. Nano-python is used to communicate with the Nano. If node is not running locally (which is recommended), change the settings in config.json. Keep in mind, the software does not lock/unlock the wallet and running a node with a public RPC is a security concern.


The first thing to be done is to generate the database. Currently the lottery uses SQLite, but the database can easily be swapped for another by making changes to the database.py file. If SQLite is used, run database.py. This will also generate 1 blank lottery, which lottery_app.py can use.

When generated, start lottery_app in a secure place and keep it be. It will be checking the Nano node for any transactions and if it sees any, sell them a ticket.

After running lottery_app once, the flask_app can be started without issues.
Nano Lottery uses Gunicorn and nginx to display the Flask application. They are not a requirement and Flask applications can be run in a number of different ways. This page will not include a description on how to setup the Flask application in a production environment.

# Provably Fair
Nano Lottery uses the randomness in the block hash of Bitcoin blocks. Draw number is a Bitcoin block in the future lottery_app will be checking for and finding the random number to calculate the winner from.
The code used for provably fair can be found in modules/fair.py.
