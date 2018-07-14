from flask import Flask, render_template, request
from modules.database import Ticket, Lottery, tables, db
from decimal import Decimal
from modules.fair import last_blockchain

import os, json  # Reading config file
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'config.json')
with open(filename, 'r') as file:
    config = json.load(file)

app = Flask(__name__)


def limit_table_size(table):
    table_size = 100
    if request:
        if request.args:
            table_size = int(request.args["size"])
    if len(table) > table_size:
        return table[:table_size]
    return table


@app.route('/', methods=['GET', 'POST'])
def index():
    # for lottery in Lottery.select().order_by(Lottery.endblock.desc()):
    #    lottery = lottery
    #    break
    curr_lottery = Lottery.select().order_by(Lottery.endblock.desc()).get()

    # Calculating pot
    # pot = Decimal(0)
    # for _ in lottery.tickets:
    #    pot += Decimal("0.01")
    pot = curr_lottery.tickets.count() * Decimal("0.01")

    # Calculating remaining time
    remaining_blocks = curr_lottery.endblock - last_blockchain() - config["block_limit"]

    remaining_time = remaining_blocks*10
    table = []
    for ticket in curr_lottery.tickets.order_by(Ticket.time.desc()):
        ticket_info = {"date": str(ticket.time)[:19], "ticket": ticket.ticket, "account": ticket.account,
                       "endblock": ticket.lottery.endblock, "hash": ticket.hash,
                       "altaccount": f'{ticket.account[:8]}...{ticket.account[-4:]}'}
        table.append(ticket_info)

    table = limit_table_size(table)

    return render_template("index.html", pot=pot, time=remaining_time,
                           account=config["account"], table=table, endblock=curr_lottery.endblock)


@app.route('/lottery', methods=['GET', 'POST'])
def lotteries():
    # Lotteries
    lottery_table = []
    for lottery in Lottery.select().order_by(Lottery.endblock.desc()):
        if lottery.winner:
            lottery_winner = lottery.winner
            alt_winner = f'{lottery.winner[:8]}...{lottery.winner[-4:]}'
        else:
            lottery_winner = None
            alt_winner = None

        pot = lottery.tickets.count() * Decimal("0.01")

        if lottery.due is False:  # Has to be 'is False' as it would otherwise trigger on None.
            lottery_dir = {"id": lottery.id, "endblock": lottery.endblock, "time": str(lottery.time)[:19],
                           "pot": pot, "roll": lottery.roll, "winner": lottery_winner,
                           "winner_hash": lottery.winner_hash, "alt_winner": alt_winner}
        elif lottery.due:
            lottery_dir = {"id": lottery.id, "endblock": lottery.endblock, "time": str(lottery.time)[:19],
                           "pot": pot, "roll": "Waiting for block ", "winner": lottery_winner, "alt_winner": alt_winner}
        elif lottery.due is None:
            lottery_dir = {"id": lottery.id, "endblock": lottery.endblock, "time": str(lottery.time)[:19],
                           "pot": pot, "roll": "In progress", "winner": lottery_winner, "alt_winner": alt_winner}

        lottery_table.append(lottery_dir)

        lottery_table = limit_table_size(lottery_table)

    return render_template("lottery.html", lottery_table=lottery_table)


@app.route('/ticket', methods=['GET', 'POST'])
def tickets():
    # Tickets
    ticket_table = []
    for ticket in Ticket.select().join(Lottery).order_by(Lottery.endblock.desc(), Ticket.ticket.desc()):
        ticket_dir = {"id": ticket.lottery.id, "endblock": ticket.lottery.endblock, "ticket": ticket.ticket,
                      "time": str(ticket.time)[:19], "account": ticket.account, "hash": ticket.hash}
        ticket_table.append(ticket_dir)

    ticket_table = limit_table_size(ticket_table)

    return render_template("ticket.html", ticket_table=ticket_table)


@app.route('/ticketdetail/<drawing_number>', methods=['GET', 'POST'])
def drawing_details(drawing_number):
    # Display details on the specific drawing
    lottery_table = []
    for ticket in Ticket.select().join(Lottery).where(Lottery.id == drawing_number):
        ticket_dir = {"id": ticket.lottery.id, "endblock": ticket.lottery.endblock, "ticket": ticket.ticket,
                      "time": str(ticket.time)[:19], "account": ticket.account, "hash": ticket.hash,
                      "altaccount": f'{ticket.account[:8]}...{ticket.account[-4:]}'}
        lottery_table.append(ticket_dir)

    lottery_table = limit_table_size(lottery_table)

    return render_template("ticketdetail.html", ticket_table=lottery_table)


@app.route('/fair', methods=['GET', 'POST'])
def fair():
    return render_template("fair.html")


if __name__ == "__main__":
    app.run()
