from chalice import Chalice
import logging
from chalicelib.services.request_service import RequestService
from chalicelib.services.release_data_service import ReleaseDataService
from chalicelib.services.calendar_register_service import CalendarRegisterService
from chalicelib.services.unique_dates_service import UniqueDatesService
from chalicelib.logger import MyLogger


logger = MyLogger.setup(__name__)
app = Chalice(app_name='release_date_crawler')

@app.route('/')
def main(event, context):
    try:
        request_service = RequestService()
        html = request_service.fetch_html()
        
        release_data_service = ReleaseDataService()
        release_datas = release_data_service.create_release_datas(html)
        
        unique_dates_service = UniqueDatesService()
        unique_dates = unique_dates_service.get_unique_dates(release_datas)
        
        calendar_register_service = CalendarRegisterService()
        calendar_register_service.register_calender(unique_dates)
        return 'OK'

    except Exception as e:
        logger.exception('exception:%s', e)
        return 'NG'