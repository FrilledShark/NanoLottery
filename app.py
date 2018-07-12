from flask import Flask, render_template
from modules.database import Ticket, Lottery, tables, db
from decimal import Decimal
from modules.fair import last_blockchain

import os, json  # Reading config file
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'config.json')
with open(filename, 'r') as file:
    config = json.load(file)


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    for lottery in Lottery.select().order_by(Lottery.endblock.desc()):
        lottery = lottery
        break

    # Calculating pot
    pot = Decimal(0)
    for _ in lottery.tickets:
        pot += Decimal("0.01")

    # Calculating remaining time

    remaining_blocks = lottery.endblock - last_blockchain() - config["block_limit"]

    remaining_time = remaining_blocks*10
    table = []
    for ticket in lottery.tickets.order_by(Ticket.time.desc()):
        ticket_info = {"date": str(ticket.time)[:19], "ticket": ticket.ticket, "account": ticket.account,
                       "endblock": ticket.lottery.endblock}
        table.append(ticket_info)

    return render_template("index.html", pot=pot, time=remaining_time,
                           account=config["account"], table=table, endblock=lottery.endblock)


@app.route('/lottery', methods=['GET', 'POST'])
def lotteries():
    # Lotteries
    lottery_table = []
    for lottery in Lottery.select().order_by(Lottery.endblock.desc()):
        pot = Decimal(0)
        for _ in lottery.tickets:
            pot += Decimal("0.01")
        lottery_dir = {"endblock": lottery.endblock, "time": str(lottery.time)[:19],
                       "pot": pot, "roll": lottery.roll, "winner": lottery.winner}
        lottery_table.append(lottery_dir)

    return render_template("lottery.html", lottery_table=lottery_table)


@app.route('/ticket', methods=['GET', 'POST'])
def tickets():
    # Tickets
    ticket_table = []
    for ticket in Ticket.select().join(Lottery).order_by(Lottery.endblock.desc(), Ticket.ticket.desc()):
        ticket_dir = {"endblock": ticket.lottery.endblock, "ticket": ticket.ticket,
                      "time": str(ticket.time)[:19], "account": ticket.account, "hash": ticket.hash}
        ticket_table.append(ticket_dir)

    return render_template("ticket.html", ticket_table=ticket_table)


if __name__ == "__main__":
    app.run()
