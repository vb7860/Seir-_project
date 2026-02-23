import sys
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
def main():
    if len(sys.argv) != 2:
        print("put correct url")
        sys.exit(1)
    url = sys.argv[1]
    response = requests.get(url)
    if response.status_code == 200:
        raw_html = response.text
        soup = BeautifulSoup(raw_html, 'html.parser')
        if soup.title:
            print(soup.title.get_text())
        if soup.body:
            body_text = soup.body.get_text(separator=' ', strip=True)
            print(body_text)
            for link in soup.find_all('a'):
                address = link.get('href')
                if address:
                    print(address)
            word_counts = get_word_frequencies(body_text)
            for word, count in word_counts.items():
                h_val = polynomial_hash(word)
                print(f"Word: {word} | Count: {count} | Hash: {h_val}")
    else:
        print("i Can not fetch page")
        sys.exit()
def get_word_frequencies(text):
    words = re.findall(r'\w+', text.lower())
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    return word_counts
def polynomial_hash(word):
    p = 53
    m = 2**64
    h = 0
    power = 1
    for char in word:
        h = (h + ord(char) * power) % m
        power = (power * p) % m
    return h


    
main()