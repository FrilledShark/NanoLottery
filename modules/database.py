from datetime import datetime
from peewee import *
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../database.db')

db = SqliteDatabase(filename, pragmas=(('foreign_keys', 'on'),))


#
# Tables
#

class Lottery(Model):
    id = IntegerField()
    time = DateTimeField(default=datetime.now())
    endblock = IntegerField()
    nano = DecimalField()
    roll = IntegerField(null=True)
    winner = CharField(null=True)

    class Meta:
        database = db


class Ticket(Model):
    id = IntegerField(null=True)
    ticket = IntegerField()
    lottery = ForeignKeyField(Lottery, backref='tickets')
    time = DateTimeField(default=datetime.now())
    address = CharField()

    class Meta:
        database = db



tables = [Lottery, Ticket]


if __name__ == "__main__":
    db.create_tables(tables)