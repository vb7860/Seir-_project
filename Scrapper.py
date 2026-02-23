import sys
import requests
from bs4 import BeautifulSoup

def detailoffirst(link1):
        response = requests.get(link1)
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

            body_text=body_text.lower()            
            words=[]
            newword=""
            for i in body_text:
                if i.isalnum():
                    newword+=i
                    
                else:
                    if len(newword)>0:
                        words.append(newword)
                        newword=""
            print(words)

            countofwords={}
            for i in words:
                if i in countofwords:
                    countofwords[i]+=1
                else:
                    countofwords[i]=1 

            def polynomial_hash(newword):
                p = 53
                m = 2**64
                h = 0
                power = 1
                for char in newword:
                    h = (h + ord(char) * power) % m
                    power = (power * p) % m
                return h
            
            def simhash(countofwords):
                
                bitarr = [0]*64
                for newword in countofwords:
                    calchash=polynomial_hash(newword)
                    calcfrq=countofwords[newword]
                    for i in range(64):
                        if (calchash>>i) & 1:
                            bitarr[i]+=calcfrq
                        else:
                            bitarr[i]-=calcfrq
                            
                output=0
                for i in range(64):
                    if bitarr[i]>0:
                        output = output | (1<<i)
                        
                return output
            print("simhash value is :")
            print(simhash(countofwords))



        else:
            print("i Can not fetch page for the link")
            print(link1)
            sys.exit() 
        return simhash(countofwords)
def detailofsecond(link2):
        response = requests.get(link2)
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

            body_text=body_text.lower()            
            words=[]
            newword=""
            for i in body_text:
                if i.isalnum():
                    newword+=i
                    
                else:
                    if len(newword)>0:
                        words.append(newword)
                        newword=""
            print(words)

            countofwords={}
            for i in words:
                if i in countofwords:
                    countofwords[i]+=1
                else:
                    countofwords[i]=1 

            def polynomial_hash(newword):
                p = 53
                m = 2**64
                h = 0
                power = 1
                for char in newword:
                    h = (h + ord(char) * power) % m
                    power = (power * p) % m
                return h
            
            def simhash(countofwords):
                
                bitarr = [0]*64
                for newword in countofwords:
                    calchash=polynomial_hash(newword)
                    calcfrq=countofwords[newword]
                    for i in range(64):
                        if (calchash>>i) & 1:
                            bitarr[i]+=calcfrq
                        else:
                            bitarr[i]-=calcfrq
                            
                output=0
                for i in range(64):
                    if bitarr[i]>0:
                        output = output | (1<<i)
                        
                return output
            print("simhash value is :")
            print(simhash(countofwords))



        else:
            print("i Can not fetch page for the link")
            print(link2)
            sys.exit() 
        return simhash(countofwords) 



def main():
    if len(sys.argv) == 1:
        print("put correct url")
        sys.exit(1)

    elif len(sys.argv)==2:
        detailoffirst(sys.argv[1])

    elif len(sys.argv)==3:
        simhashfirst=detailoffirst(sys.argv[1])
        simhashsecond=detailoffirst(sys.argv[2])
        xor = simhashfirst^simhashsecond
        difference=bin(xor).count("1")
        common=64-difference
        print("common hash value bits is :")
        print(common)

    

main()


