from modules import fair
from modules.database import Ticket, Lottery, db
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
    while True:
        # First, check if current lottery is  duedate
        for lottery in Lottery.select().order_by(Lottery.endblock.desc()):
            lottery = lottery
            break
        current_block = fair.last_blockchain()
        if current_block + config["block_limit"] >= lottery.endblock:
            print("Lottery is due")
            # Getting date for next friday
            today = datetime.now()
            # # Getting time on friday
            # friday = today + timedelta((4 - today.weekday()) % 7)
            # # Getting time on friday, 20:00
            # target = datetime.combine(friday, time(hour=20))

            # Getting time for tomorrow # Only for testing
            target = today + timedelta(hours=4)

            # Getting difference between today and friday, 20:00
            delta = target - datetime.now()
            # Getting difference in minutes
            minutes = delta.total_seconds()/60
            # Getting number of blocks, by using an estimated of 9.5 minutes between blocks.
            blocks = round(minutes/9.5)

            # Create new lottery
            new_lottery = Lottery.create(id=lottery.id+1, time=datetime.now(), endblock=current_block+blocks)
            new_lottery.save()
            print(f'New lottery created. Endblock {new_lottery.endblock}')
            lottery.due = True
            lottery.save()

        # Fix due lotteries
        # Check if any lotteries can be fixed:
        lotteries_due = []
        for lottery in Lottery.select().where(Lottery.due == True):
            lotteries_due.append(lottery)
        for lottery in lotteries_due:
            # Possible to continue?
            if current_block >= lottery.endblock:
                # Needs to get number of tickets sold
                tickets_sold = 0
                for ticket_sold in Ticket.select().join(Lottery).where(Lottery.id == lottery.id):
                    tickets_sold += 1
                print(f'{tickets_sold} tickets sold')
                block_hash = fair.blockchain_api(lottery.endblock)
                print(block_hash)
                float_roll = fair.roll(block_hash)
                print(float_roll)

                if tickets_sold != 0:
                    final_roll = fair.roll_between(tickets_sold, float_roll)

                    print(f'Ticket with number {final_roll} won!')
                    # Inserting roll
                    lottery.roll = final_roll
                    # Finding winner
                    winner_ticket = Ticket.get(Ticket.ticket == lottery.roll)

                    # Sending to winner and dev funds.
                    pot_amount = tickets_sold * Decimal("0.01")
                    pot_dev = pot_amount * Decimal(str(config["dev_fee"])) # Hurray for float precision! :D
                    pot_win = pot_amount - pot_dev

                    print(f'Winner account is: {winner_ticket.account}. He gets {pot_win}')
                    # Make sure the win amount is sent
                    id = round(timenow())
                    while True:
                        try:
                            send_block = rpc.send(wallet=config["wallet"], source=config["account"],
                                                  destination=winner_ticket.account, amount=int(pot_win * 10 ** 30), id=id)
                            if send_block:
                                print(send_block)
                                break
                        except Exception as er:
                            print(er)
                            pass
                    # sleep(0.01)
                    id = round(timenow())
                    if config["dev_fee"] != 0:
                        while True:
                            try:
                                send_block = rpc.send(wallet=config["wallet"], source=config["account"],
                                                      destination=config["dev_account"], amount=int(pot_dev * 10 ** 30),
                                                      id=id)
                                if send_block:
                                    print(send_block)
                                    break
                            except Exception as er:
                                print(er)
                                pass
                        # Things should be sent now.
                    lottery.winner = winner_ticket.account
                    lottery.due = False
                    lottery.save()
                    print("Lottery out!")
                else:
                    print("Poor you, no one bought any tickets")
                    lottery.due = False
                    lottery.save()
        for lottery in Lottery.select().order_by(Lottery.endblock.desc()):
            lottery = lottery
            break
        # Get pending transactions
        pending = rpc.pending(config["account"])
        if pending:
            for block in pending:
                print(f'{block} is pending')
                rpc_block = rpc.blocks_info([block])[block]
                rpc_account = rpc_block["block_account"]
                rpc_amount = rpc_block["amount"]
                # Number of tickets
                price = config["ticket_price"]
                tickets_bought = int(rpc_amount/10**30/price)
                print(tickets_bought)
                if tickets_bought > 0:
                    print(f'{rpc_account} wants to buy')
                    # Find last ticket
                    sold_tickets = []
                    for ticket in lottery.tickets:
                        sold_tickets.append(ticket.ticket)
                    if not sold_tickets:
                        sold_tickets.append(0)
                    # Give new guy his tickets.
                    print(sold_tickets)
                    for i in range(tickets_bought):
                        ticket_number = max(sold_tickets) + 1 + i
                        print(f'Sold: {ticket_number} to endblock {lottery.endblock}')
                        ticket = Ticket.create(ticket=ticket_number, lottery=lottery,
                                               time=datetime.now(), account=rpc_account, hash=block)
                        ticket.save()
                    rpc.receive(config["wallet"], config["account"], block)
        sleep(1)
