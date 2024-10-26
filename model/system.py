from peewee import *
from system import CdoApp

class PluginType(Model):
    code = CharField()
    description = CharField(null=True, default=None)

    class Meta:
        database = CdoApp.get_db()

class Plugin(Model):
    package = CharField()
    active = BooleanField(default=True)
    initialized = BooleanField(default=False)
    type = ForeignKeyField(PluginType, backref='plugins')

    class Meta:
        database = CdoApp.get_db()