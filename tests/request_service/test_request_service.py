from release_date_crawler.chalicelib.services.request_service import RequestService

def test_fetch_html():
    html = RequestService.fetch_html(RequestService)
    with open('tests/release_data_service/test.html', mode='w') as f:
        f.write(html)
    assert html, 'successful'