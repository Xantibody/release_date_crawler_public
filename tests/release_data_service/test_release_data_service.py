from release_date_crawler.services.release_data_service import ReleaseDataService

def test_create_release_datas():
    html = ''
    with open('tests/release_data_service/test.html', 'r') as f:
        html = f.read()
    ReleaseDataService.create_release_datas(ReleaseDataService, html)