from lib import requests, BeautifulSoup


def get_html_content(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")

    return soup


















