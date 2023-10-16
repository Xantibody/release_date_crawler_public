import googleapiclient.discovery
import google.auth
from chalicelib.logger import MyLogger
from chalicelib.data.release_date import ReleaseDateData
from chalicelib.services.util_service import UtilService

logger = MyLogger.setup(__name__)

class CalendarRegisterService:
    def register_calender(self, release_dates:list[ReleaseDateData]):
        try:
            logger.info('カレンダー登録 開始')
            if len(release_dates) == 0:
                logger.info('カレンダー登録データなし')

            else:
                service = self._create_calendar_service()
                events = self._create_events(release_dates)
                conf = UtilService.create_conf()
                for event in events:
                    service.events().insert(calendarId=conf.get('google', 'calendar_id'), body=event).execute()

        except Exception as e:
             logger.exception('exception:%s', e)
             raise
        
        else:    
            logger.info('カレンダー登録 終了')


    def _create_calendar_service(self):
            SCOPES = ['https://www.googleapis.com/auth/calendar']
            creds = google.auth.load_credentials_from_file('chalicelib/config/credentials.json', SCOPES)[0]
            service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
            return service


    def _create_events(self, release_dates:list[ReleaseDateData]):
        events = []
        for release_data in release_dates:
            event = {
                'summary': release_data.title,
                'start': {
                    'date': release_data.release_date.isoformat(),
                },
                'end': {
                   'date': release_data.release_date.isoformat(),
                },
            }
            events.append(event)
        return events