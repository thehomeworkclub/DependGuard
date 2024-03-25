from peewee import *
import psycopg2


# Connect to the PostgreSQL database
database = PostgresqlDatabase('defaultdb', **{
    'host': 'pstdbdedi-do-user-11106940-0.c.db.ondigitalocean.com',
    'port': 25060,
    'user': 'doadmin',
    'password': 'AVNS_4qIXT_v6ZdvCnbulAS_'
})


class UnknownField(object):
    """
    Placeholder class for unknown fields in the database model.
    """

    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    """
    Base model class for all database models.
    Sets the database connection.
    """

    class Meta:
        database = database


class Dblk(BaseModel):
    """
    Database model for storing dependency information.
    """

    package = CharField(null=True)  # Name of the package
    subdeps = AnyField(null=True)  # List of sub-dependencies (can be nested)
    version = TextField(null=True)  # Version of the package
    v_behind = TextField(null=True)  # Number of versions behind the latest

    class Meta:
        table_name = 'dblk'
        primary_key = False  # No primary key is defined for this model