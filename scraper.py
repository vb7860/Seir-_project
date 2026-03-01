import sys
import requests
from bs4 import BeautifulSoup
import re

def fetch_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Cannot fetch page:", url)
        sys.exit()

    soup = BeautifulSoup(response.text, "html.parser")

    print("URL:", url)

    if soup.title:
        print("Page Title:")
        print(soup.title.get_text(strip=True))
    else:
        print("Page Title: Not Found")

    body_text = ""
    if soup.body:
        body_text = soup.body.get_text(separator=" ", strip=True)
        print("Page Body:")
        print(body_text)

    print("Links:")
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            print(href)

    return body_text


def polynomial_hash(word):
    p = 53
    m = 2**64
    h = 0
    power = 1
    for char in word:
        h = (h + ord(char) * power) % m
        power = (power * p) % m
    return h


def simhash(text):
    words = re.findall(r'\w+', text.lower())
    count = {}
    for word in words:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1

    bitarr = [0] * 64

    for word in count:
        hashvalue = polynomial_hash(word)
        frequency = count[word]
        for i in range(64):
            if (hashvalue >> i) & 1:
                bitarr[i] += frequency
            else:
                bitarr[i] -= frequency

    output = 0
    for i in range(64):
        if bitarr[i] > 0:
            output |= (1 << i)

    return output


def main():
    if len(sys.argv) < 2:
        print("Provide at least one URL")
        sys.exit()

    if len(sys.argv) == 2:
        text = fetch_page(sys.argv[1])
        print("Simhash:", simhash(text))

    elif len(sys.argv) == 3:
        text1 = fetch_page(sys.argv[1])
        text2 = fetch_page(sys.argv[2])
        hash1 = simhash(text1)
        hash2 = simhash(text2)
        xor = hash1 ^ hash2
        difference = bin(xor).count("1")
        similarity = 64 - difference
        print("Common hash bits:", similarity)


if __name__ == "__main__":
    main()
