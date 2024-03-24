from peewee import *
import psycopg2

database = PostgresqlDatabase('defaultdb', **{'host': 'pstdbdedi-do-user-11106940-0.c.db.ondigitalocean.com', 'port': 25060, 'user': 'doadmin', 'password': 'AVNS_4qIXT_v6ZdvCnbulAS_'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Dblk(BaseModel):
    package = CharField(null=True)
    subdeps = AnyField(null=True)
    # TODO: Create version itemary and enter it in

    class Meta:
        table_name = 'dblk'
        primary_key = False