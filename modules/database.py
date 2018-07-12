from datetime import datetime
from peewee import *
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../database.db')

db = SqliteDatabase(filename)


class BaseModel(Model):
    class Meta:
        database = db


#
# Tables
#

class Lottery(BaseModel):
    id = IntegerField()
    time = DateTimeField(default=datetime.now())
    endblock = IntegerField()
    nano = DecimalField(null=True)
    roll = IntegerField(null=True)
    winner = CharField(null=True)
    due = BooleanField(default=False)


class Ticket(BaseModel):
    id = IntegerField(null=True)
    ticket = IntegerField()
    lottery = ForeignKeyField(Lottery, backref='tickets')
    time = DateTimeField(default=datetime.now())
    account = CharField()
    hash = CharField(null=True)


tables = [Lottery, Ticket]


if __name__ == "__main__":
    db.create_tables(tables)
    # lottery = Lottery.create(id=0, endblock=1)
