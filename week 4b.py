import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE



url = input('Enter URL: ')
if len(url)<1 :
    url = "http://py4e-data.dr-chuck.net/known_by_Ruaraidh.html"
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

count = int(input("Enter Count: "))
position = int(input("Enter Position: "))

people = list()

while count > 0:
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    anchors = soup('a')
    print(anchors)
    people.append(anchors[position-1].string)
    count = count - 1
    url = anchors[position-1].get("href", None)

print(people)



