import configparser

class UtilService:
    def create_conf():
        conf = configparser.ConfigParser()
        conf.read('chalicelib/config/config.ini')
        return conf