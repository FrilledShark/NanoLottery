from modules import fair
from modules.database import Ticket, Lottery, tables, db
from datetime import datetime, timedelta, date, time
from time import time as timenow
from time import sleep
from decimal import Decimal

import os, json  # Reading config file
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'config.json')
with open(filename, 'r') as file:
    config = json.load(file)
from nano.rpc import Client
rpc = Client(config["rpc.client"])




if __name__ == "__main__":
    print(rpc.receive_minimum_set(1 * 10 ** 36))
    db.connect()
    # First, check if current lottery is  duedate
    for lottery in Lottery.select().order_by(Lottery.endblock.desc()):
        lottery = lottery
        break
    current_block = fair.last_blockchain()
    if current_block + 6 >= lottery.endblock:
        # Getting date for next friday
        today = date.today()
        # Getting time on friday
        friday = today + timedelta((4 - today.weekday()) % 7)
        # Getting time on friday, 20:00
        target = datetime.combine(friday, time(hour=20))
        # Getting difference between today and friday, 20:00
        delta = target - datetime.now()
        # Getting difference in minutes
        minutes = delta.total_seconds()/60
        # Getting number of blocks, by using an estimated of 9.5 minutes between blocks.
        blocks = round(minutes/9.5)

        # Create new lottery
        new_lottery = Lottery.create(id=lottery.id+1, time=datetime.now(), endblock=current_block+blocks)
        new_lottery.save()

        # New lottery created. Last lottery should be fixed:
        block_hash = fair.blockchain_api(lottery.endblock)
        print(block_hash)
        float_roll = fair.roll(block_hash)
        print(float_roll)

        # Needs to get number of tickets sold
        tickets_sold = 0
        for ticket_sold in Ticket.select().join(Lottery).where(Lottery.id == lottery.id):
            tickets_sold += 1
        final_roll = fair.roll_between(tickets_sold, float_roll)

        # Inserting roll
        lottery.roll = final_roll

        # Finding winner
        winner_ticket = Ticket.select().where(Ticket.ticket == lottery.roll)

        # Sending to winner and dev funds.
        pot_amount = tickets_sold * 0.01
        pot_win = pot_amount * config["dev_fee"]
        pot_dev = pot_amount - pot_win
        # Make sure the win amount is sent
        id = round(timenow())
        while True:
            try:
                if rpc.send(wallet=config["wallet"], source=config["address"],
                            destination=winner_ticket.address, amount=pot_win*10**30, id=id):
                    break
            except:
                pass
        sleep(1)
        id = round(timenow())
        while True:
            try:
                if rpc.send(wallet=config["wallet"], source=config["address"],
                            destination=winner_ticket.address, amount=pot_dev * 10 ** 30, id=id):
                    break
            except:
                pass
        # Things should be sent now.

        lottery.save()

    # Create tickets

    # Get pending transactions
    pending = rpc.pending(config["address"])
    if pending:
        for block in pending:
            print(f'{block} is pending')
            rpc_block = rpc.blocks_info(block)[block]
            rpc_account = rpc_block["block_account"]
            rpc_amount = rpc_block["amount"]
            # Number of tickets
            price = config["ticket_price"]
            tickets_bought = round(rpc_amount/(price*10**30)-0.5)
            if tickets_bought > 0:
                print(f'{rpc_account} wants to buy')
                # Find last ticket
                sold_tickets = []
                for ticket in Ticket.select().order_by(Ticket.ticket.desc()).join(Lottery).where(Lottery.id = lottery.id):
                    sold_tickets.append(ticket.ticket)

                # Give new guy his tickets.
                for i in range(tickets_bought):
                    ticket_number = max(sold_tickets) + 1 + i
                    print(f'Sold: {ticket_number}')
                    ticket = Ticket.create(ticket=ticket_number, lottery=lottery,
                                           time=datetime.now(), address=rpc_account)
                    ticket.save()


