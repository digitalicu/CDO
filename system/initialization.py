import importlib
from system import CdoApp
from model import *

class Initializer(object):
    def preapre_app(self):
        self.init_db()
        self.load_plugins()

    def init_db(self):
        db = CdoApp.get_db()

        if len(db.get_tables()) == 0:
            db.create_tables([Collection, PluginType, Plugin, 
                              CollectionField, CollectionDataRow, CollectionFieldValue,
                              Settings])

            field_plugin_type = PluginType.create(code="FIELD_PLUGIN")
            field_plugin_type.save()
            field_param_plugin_type = PluginType.create(code="FIELD_PARAM_PLUGIN")
            field_param_plugin_type.save()

            Plugin.create(package="plugin.field.int_field.IntField", type=field_plugin_type, initialized=True).save()
            Plugin.create(package="plugin.field.float_field.FloatField", type=field_plugin_type, initialized=False).save()
            Plugin.create(package="plugin.field.string_field.StringField", type=field_plugin_type, initialized=True).save()
            Plugin.create(package="plugin.field.bool_field.BooleanField", type=field_plugin_type, initialized=True).save()
            Plugin.create(package="plugin.field.select_field.SelectField", type=field_plugin_type, initialized=False).save()
            Plugin.create(package="plugin.field.datetime_field.DateTimeField", type=field_plugin_type, initialized=False).save()

            Plugin.create(package="plugin.field_param.general.GeneralFieldParam", type=field_param_plugin_type).save()
            Plugin.create(package="plugin.field.select_field.SelectOptionsFieldParam", type=field_param_plugin_type).save()
            Plugin.create(package="plugin.field.datetime_field.DateTimeSettingsFieldParam", type=field_param_plugin_type).save()

    def load_plugins(self):
        plugins = {}
        for p in Plugin.select():
            if p.active:
                if p.type.code not in plugins.keys():
                    plugins[p.type.code] = {}

                package, class_name = p.package.rsplit(".", 1)
                mod = importlib.import_module(package)
                plugins[p.type.code][p.package] = getattr(mod, class_name)()

                if not p.initialized:
                    plugins[p.type.code][p.package].initialize()
                    query = Plugin.update({Plugin.initialized: True}).where(Plugin.package==p.package)
                    query.execute()

        CdoApp.set_loaded_plugins(plugins)