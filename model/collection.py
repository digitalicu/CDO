from peewee import *
from system import CdoApp
from model import Plugin

class Collection(Model):
    name = CharField()

    class Meta:
        database = CdoApp.get_db()

class CollectionField(Model):
    collection = ForeignKeyField(Collection, backref="fields")
    type = ForeignKeyField(Plugin)
    name = CharField()
    order = IntegerField(default=0)

    class Meta:
        database = CdoApp.get_db()

class CollectionDataRow(Model):
    collection = ForeignKeyField(Collection, backref="rows")
    order = IntegerField(default=0)

    class Meta:
        database = CdoApp.get_db()

class CollectionFieldValue(Model):
    field = ForeignKeyField(CollectionField)
    value = CharField()
    row = ForeignKeyField(CollectionDataRow, backref="fields")

    class Meta:
        database = CdoApp.get_db()

def create_collection_by_name(name) -> Collection:
    new_object = Collection.create(name=name)
    new_object.save()
    return new_object