
from features.esp_easy.esp_easy_model import Controller
from features.esp_easy.html_parser import HtmlParser
from tests.conftest import read_file

   

def test_controllers():
    # Given: Html file
    html = read_file("controllers.html")
    hp = HtmlParser(html)
    # When: Html is parsed
    ret = hp.parse_controllers()
    # Then: Controllers are parsed
    print (ret)
    assert isinstance(ret, list)
    assert len(ret) == 3
    assert all(isinstance(c, Controller) for c in ret)
