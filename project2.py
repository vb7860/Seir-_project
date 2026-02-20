import sys
import requests
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) != 2:
        print("put correct url")
        sys.exit(1)

    url = sys.argv[1]
    response = requests.get(url)
    if response.status_code == 200:
        raw_html = response.text
        soup = BeautifulSoup(raw_html, 'html.parser')
        print(soup.title.get_text())
        body_text = soup.body.get_text(separator=' ', strip=True)
        print(body_text)
        for link in soup.find_all('a'):
            address = link.get('href')
            if address:
                print(address)
    else:
        print("i Can not fetch page")
        sys.exit()
main()
