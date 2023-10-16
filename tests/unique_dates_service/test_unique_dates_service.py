import pytest
import pytest_mock
from release_date_crawler.data.release_date import ReleaseDateData
from release_date_crawler.services.unique_dates_service import UniqueDatesService
import datetime
import csv


today = datetime.date.today()
tomorrow =  datetime.datetime.now() + datetime.timedelta(days = 1)
tomorrow = tomorrow.date()

class TestUniqueDatesService:
    @pytest.fixture
    def release_dates(self):
        test1 = "テスト1"
        test2 = "テスト2"
        release_dates = [ReleaseDateData(title=test1, release_date=today), ReleaseDateData(title=test2, release_date=tomorrow)]
        date_list = [[test1, today],[test2, tomorrow]]
        with open("tests/unique_dates_service/test.csv", "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(date_list)
        return release_dates
        # yield

    # def test_get_unique_dates(self, release_dates, mocker):
    #     result = UniqueDatesService.get_unique_dates(UniqueDatesService, release_dates)
    #     print(result)
    #     assert result, 'successful'
    
    def test_create_unique_date_list(self):
        old_dates = [] 
        with open("tests/unique_dates_service/test.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            old_dates = [row for row in reader]
        current_dates = [['テスト1', today.strftime('%Y-%m-%d')], ['テスト2', tomorrow.strftime('%Y-%m-%d')], ['テスト3', '2022-01-01'], ['テスト4', '2023-01-01']]
        l = UniqueDatesService._create_unique_date_list(current_dates, old_dates)
        print(l)
        assert len(l) == 2 , 'successful' 