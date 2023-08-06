from configparser import ConfigParser
from pathlib import Path


class ConfigurableObject:
    basedir = None
    exception = None

    def __init__(self, name):
        commonconf = Path(__file__).parent / self.basedir / "common.ini"
        conffile = Path(__file__).parent / self.basedir / f"{name}.ini"
        if not conffile.exists():
            raise self.exception(name)
        self.name = name
        self.config = ConfigParser()
        self.config.optionxform = str
        self.config.read(commonconf)
        self.config.read(conffile)
        self.__init_config__()

    def __init_config__(self):
        raise NotImplementedError
