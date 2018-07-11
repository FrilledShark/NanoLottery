from datetime import datetime
from peewee import *
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../database.db')

db = SqliteDatabase(filename)

#
# Tables
#

class Ticket(Model):
    id = CharField(null=True)
    time = CharField(default=datetime.now())
    address = DateTimeField()
    nano = DecimalField()

    class Meta:
        database = db

class Lottery(Model):
    id = CharField(null=True)
    time = CharField(default=datetime.now())
    roll = DateTimeField()
    winner = DecimalField()

    class Meta:
        database = db

tables = [Ticket, Lottery]


if __name__ == "__main__":
    db.create_tables(tables)