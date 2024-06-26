import os

g = None


def init_config():
    global g
    g = Config()


class ConfigEnvError(Exception):
    pass


class Config(object):
    # the host / credentials to access the database
    ARANGO_USERNAME = ""
    ARANGO_PASSWORD = ""
    DB_HOST = ""
    DB_NAME = ""

    # the versioning infos
    VERSION = ""
    COMMIT_SHA = ""
    JOB_URL = ""

    # misc config
    JWT_SECRET_KEY = ""
    TIMEZONE = ""
    DEBUG = ""

    @staticmethod
    def get_env_value(env_name):
        if env_name not in os.environ.keys():
            raise ConfigEnvError(f"Missing environment variable: {env_name}")

        env_value = os.environ.get(env_name)
        return env_value

    def __init__(self):
        self.ARANGO_USERNAME = self.get_env_value("ARANGO_USERNAME")
        self.ARANGO_PASSWORD = self.get_env_value("ARANGO_PASSWORD")
        self.DB_HOST = self.get_env_value("DB_HOST")
        self.DB_NAME = self.get_env_value("DB_NAME")
        if "VERSION" in os.environ.keys():
            self.VERSION = self.get_env_value("VERSION")
        if "COMMIT_SHA" in os.environ.keys():
            self.COMMIT_SHA = self.get_env_value("COMMIT_SHA")
        if "JOB_URL" in os.environ.keys():
            self.JOB_URL = self.get_env_value("JOB_URL")
        self.JWT_SECRET_KEY = self.get_env_value("JWT_SECRET_KEY")
        self.TIMEZONE = self.get_env_value("TIMEZONE")
        if "DEBUG" in os.environ.keys():
            self.DEBUG = self.get_env_value("DEBUG")
        self.ALGORITHM = self.get_env_value("ALGORITHM")
