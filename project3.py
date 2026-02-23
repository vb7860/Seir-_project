import sys
import requests
from bs4 import BeautifulSoup
import re

def get_simhash(url):
    response = requests.get(url)
    if response.status_code != 200:
        return 0
    
    soup = BeautifulSoup(response.text, 'html.parser')
    body_text = soup.body.get_text(separator=' ', strip=True).lower() if soup.body else ""
    words = re.findall(r'[a-z0-9]+', body_text)
    
    freqs = {}
    for w in words:
        freqs[w] = freqs.get(w, 0) + 1
        
    v = [0] * 64
    for word, weight in freqs.items():
        word_hash = 0
        for i, char in enumerate(word):
            word_hash = (word_hash + ord(char) * (53**i)) % (2**64)
        
        for i in range(64):
            if (word_hash >> i) & 1:
                v[i] += weight
            else:
                v[i] -= weight
                
    fingerprint = 0
    for i in range(64):
        if v[i] > 0:
            fingerprint |= (1 << i)
    return fingerprint

def main():
    if len(sys.argv) != 3:
        sys.exit(1)
        
    h1 = get_simhash(sys.argv[1])
    h2 = get_simhash(sys.argv[2])
    
    common = bin(~(h1 ^ h2) & 0xFFFFFFFFFFFFFFFF).count('1')
    print(common)

main()