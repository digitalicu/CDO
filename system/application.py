from peewee import SqliteDatabase

DB = SqliteDatabase('cdo.db')
DB.connect()

PLUGINS = {}

class CdoApp(object):
    @staticmethod
    def get_db():
        global DB
        return DB
    
    @staticmethod
    def close_db():
        global DB
        DB.close()
    
    @staticmethod
    def set_loaded_plugins(plugins):
        global PLUGINS
        PLUGINS = plugins

    @staticmethod
    def get_plugins():
        global PLUGINS
        return PLUGINS
    
    @staticmethod
    def get_applicable_plugins(field_package):
        plugins = {}
        for package, param_plugin in CdoApp.get_plugins()["FIELD_PARAM_PLUGIN"].items():
            if param_plugin.field_applicable(field_package):
                plugins[package] = param_plugin
        return plugins