class HemRouter(object):
    """
    A router to control all database operations on models in the
    hem application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read hem models go to hem_db.
        """
        if model._meta.app_label == 'hem_app':
            return 'hem_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to hem_db.
        """
        if model._meta.app_label == 'hem_app':
            return 'hem_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the hem app is involved.
        """
        if obj1._meta.app_label == 'hem_app' or \
           obj2._meta.app_label == 'hem_app':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the hem app only appears in the 'hem_db'
        database.
        """
        if app_label == 'hem_app':
            return db == 'hem_db'
        return None


#Class for hwbi_db routing
class HwbiRouter(object):
    """
    A router to control all database operations on models in the
    hwbi application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read hem models go to hwbi_db.
        """
        if model._meta.app_label == 'hwbi_app':
            return 'hwbi_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to hwbi_db.
        """
        if model._meta.app_label == 'hwbi_app':
            return 'hwbi_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the hwbi app is involved.
        """
        if obj1._meta.app_label == 'hwbi_app' or \
                        obj2._meta.app_label == 'hwbi_app':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the hem app only appears in the 'hwbi_db'
        database.
        """
        if app_label == 'hwbi_app':
            return db == 'hwbi_db'
        return None
