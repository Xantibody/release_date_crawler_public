import os
import csv
import boto3
import datetime
from chalicelib.logger import MyLogger
from chalicelib.services.util_service import UtilService
from chalicelib.data.release_date import ReleaseDateData


logger = MyLogger.setup(__name__)

class UniqueDatesService:
    def get_unique_dates(self, release_dates:list[ReleaseDateData]):
        try:
            logger.info('登録済み販売日削除処理 開始')
            conf = UtilService.create_conf()
            current_date_list = self._convert_release_dates_to_list(release_dates)
            client = self._create_s3_client(
                conf.get('S3', 'AWS_ACCESS_KEY_ID'), 
                conf.get('S3', 'AWS_SECRET_ACCESS_KEY'), 
                conf.get('S3','AWS_DEFAULT_REGION')
                )
            self._fetch_old_dates_csv(
                client, 
                conf.get('S3','BUCKET_NAME'), 
                conf.get('S3','OLD_CSV_PATH'), 
                conf.get('local','OLD_CSV_PATH')
                )
            old_date_list = self._read_old_dates_csv(conf.get('local','OLD_CSV_PATH'))
            result_date_list = self._create_unique_date_list(current_date_list, old_date_list)
            self._create_old_date_csv(result_date_list, old_date_list, conf.get('local','OLD_CSV_PATH'))
            self._put_old_date_list_csv(
                client,
                conf.get('local','OLD_CSV_PATH'), 
                conf.get('S3','BUCKET_NAME'), 
                conf.get('S3','OLD_CSV_PATH')
                )
            self._delete_old_dates_csv(conf.get('local','OLD_CSV_PATH'))
            release_date_datas = self._convert_list_to_release_date_datas(result_date_list)
            logger.info('登録済み販売日削除処理 終了')
            return  release_date_datas
        
        except Exception as e:
            logger.exception('exception:%s', e)
            raise


    def _convert_release_dates_to_list(self, release_dates:list[ReleaseDateData])->list[list]:
        date_list = []
        for date in release_dates:
            date_list.append([date.title, date.release_date.strftime('%Y-%m-%d')])
        logger.debug('current_date_list=%s', date_list)
        return date_list


    def _create_s3_client(self, aws_access_key_id:str, aws_secret_access_key:str, region_name:str):
        client = boto3.client('s3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        return client


    def _fetch_old_dates_csv(self,client, bucket_name:str, s3_path:str, local_path:str):
            client.download_file(
                bucket_name, 
                s3_path, 
                local_path
            )


    def _read_old_dates_csv(self, local_path:str):
            old_dates = []
            with open(local_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                old_dates = [row for row in reader]
            logger.debug('old_date_list=%s', old_dates)
            return old_dates


    def _create_unique_date_list(self, current_dates:list[list], old_dates:list[list]):
        if len(old_dates) == 0:
            logger.debug('result_dates=%s', current_dates)
            return current_dates
        
        result_dates = []
        for current_date in current_dates:
            for i, old_date in enumerate(old_dates):
                if (old_date[0] == current_date[0]) & (old_date[1] == current_date[1]):
                    break
                else:
                    if(i == len(old_dates) -1):
                        result_dates.append(current_date)
                    else:
                        continue
        logger.debug('result_dates=%s', result_dates)           
        return result_dates

    
    def _create_old_date_csv(self, result_dates:list[list], old_dates:list[list], local_path:str):
        
        with open(local_path, "w", encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(old_dates + result_dates)


    def _put_old_date_list_csv(self, client, local_path:str, bucket_name:str, s3_path:str):
        client.upload_file(
                local_path,
                bucket_name, 
                s3_path
        )


    def _delete_old_dates_csv(self, local_path:str):
        os.remove(local_path)

    
    def _convert_list_to_release_date_datas (self, release_date_list:list[list])->list[ReleaseDateData]:
        release_dates = []
        for date in release_date_list:
            title = date[0]
            release_date = datetime.datetime.strptime(date[1] ,"%Y-%m-%d").date()
            release_dates.append(ReleaseDateData(title=title, release_date=release_date))
        logger.debug('release_dates=%s', release_dates)
        return release_dates