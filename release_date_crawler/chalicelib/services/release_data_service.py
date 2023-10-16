from chalicelib.data.release_date import ReleaseDateData
from bs4 import BeautifulSoup
import datetime
import re
from chalicelib.logger import MyLogger


logger = MyLogger.setup(__name__)

class ReleaseDataService:
    def create_release_datas(self, html: str)->list[ReleaseDateData]:
        try:
            logger.info('発売日リスト作成 開始')
            soup = BeautifulSoup(html, 'html.parser')
            elems = soup.select('#latest-products .latest-info')
            release_Dates = []
            
            for elem in elems:
                date = self._parse_date(elem)
                title = self._parse_title(elem)
                logger.debug('title=%s',title)
                logger.debug('date=%s',date)
                release_Dates.append(self._create_release_data(date, title))
            logger.info('発売日リスト作成 終了')
            return release_Dates

        except Exception as e:
            logger.exception('exception:%s', e)
            raise


    def _parse_date(self, elem)->datetime.date:
        str = elem.select('.date')[0].string
        str_sub = re.sub('\(\S*\)$','',str)
        date = datetime.datetime.strptime(str_sub ,'%Y年%m月%d日').date()
        return date

    
    def _parse_title(self,elem)->str:
        title = ''
        spans = elem.select('strong span')
        i = 1
        for span in spans:
            str = span.string            
            if i == 1 or not str:
                i += 1
                continue
            
            if i == len(spans):
                title += str

            else:
                title += str + ' '
            
            i += 1
        return title
    

    def _create_release_data(self, date :datetime, title: str)-> ReleaseDateData: 
        return ReleaseDateData(
            release_date=date,
            title=title
        )
