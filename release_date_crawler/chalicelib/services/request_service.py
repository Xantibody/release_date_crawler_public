import requests
from ..logger import MyLogger
from .util_service import UtilService


logger = MyLogger.setup(__name__)

class RequestService:
    def fetch_html(self):
        logger.info('販売日html取得 開始')
        try:
            conf = UtilService.create_conf()
            url = conf.get('request','URL')
            html = requests.get(url).text
            logger.info('販売日html取得 終了')
            return html

        except Exception as e:
            logger.exception('exception:%s', e)
            raise