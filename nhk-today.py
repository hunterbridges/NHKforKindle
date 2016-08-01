import requests
import sys
import json
import codecs
import os
import re
from bs4 import BeautifulSoup
from datetime import date

def main():

    r = requests.get('http://www3.nhk.or.jp/news/easy/news-list.json')
    r.encoding = 'utf-8-sig'
    o = json.loads(r.text)
    parse(o)

def parse(o):
    for k, v in o[0].items():
        if k == date.today().strftime("%Y-%m-%d"):
            parseDate(k, v)

def parseDate(date, news):
    output = date + '.html'
    folder = 'data/' + date

 #   if os.path.isdir(folder) == False:
 #       os.makedirs(folder)
 #       print("Directory \"" + folder + "/\" created")
 #   elif os.listdir(folder):
 #       print("Directory \"" + folder + "/\" exists!\n\nAbort.\n")
 #       return

    items = []
    content = []
    for i in news:
        item = parseNews(i);
        items.append(item)
        content.append(item["content"])

    with open(output, "w") as f:
        print('<?xml version="1.0" encoding="UTF-8" ?>', file=f)
        print("<!DOCTYPE html>", file=f)
        print("<html lang='ja'>", file=f)
        print('<head><meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" >', file=f)
        print('<style type="text/css">body { margin-left: 1em; margin-right: 1em; writing-mode:tb-rl; -epub-writing-mode: vertical-rl; -webkit-writing-mode: vertical-rl; line-break: normal; -epub-line-break: normal; -webkit-line-break: normal;} {font-family: serif;} p { text-indent: 1em;} h2{ font-size: large; font-weight: bold;}</style>', file=f)
        print("</head>", file=f)
        print("<body>", file=f)
        print("<br />".join(content), file=f)
        print("</body>", file=f)
        print("</html>", file=f)
        print("File \"" + output + "\" created")
        
        file = open(date + '.opf', "w")
        file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><package version=\"3.0\" xmlns=\"http://www.idpf.org/2007/opf\"         unique-identifier=\"BookId\"> <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\"           xmlns:dcterms=\"http://purl.org/dc/terms/\">   <dc:title>NHK ニュース・読み物・" + date + "</dc:title>    <dc:contributor>NHK</dc:contributor>   <dc:language>ja</dc:language>   <dc:publisher>NHK</dc:publisher> </metadata> <manifest>  <item id=\"titlepage\" href=\"" + output + "\" media-type=\"application/xhtml+xml\" /> </manifest> <spine toc=\"tocncx\" page-progression-direction=\"rtl\">  <itemref idref=\"titlepage\" /> </spine></package>")
        file.close()
        
    for i in items:
        if not "voice" in i or not "uri" in i["voice"]:
            continue

        r = requests.get(i["voice"]["uri"])
        with open(folder + '/' + i["voice"]["file"], "wb") as f:
            f.write(r.content)
            print("File \"" + i["voice"]["file"] + "\" downloaded")

    print("Today news were downloaded from NHK.")

def parseNews(news):
    news_id = news['news_id']
    news_time = news['news_prearranged_time'].replace(':', '-')
    title = news['title']
    title_ruby = news['title_with_ruby']
    news_uri = 'http://www3.nhk.or.jp/news/easy/' + str(news_id) + '/' + str(news_id) + '.html'

    r = requests.get(news_uri)
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, 'html.parser')
    date = soup.find('p', attrs={'id':'newsDate'}).contents[0]
    title = soup.find('div', attrs={'id':'newstitle'})#.find('h2')
    article = soup.find('div', attrs={'id':'newsarticle'})

    for a in article.findAll('a'):
        a.unwrap()

 #   if news['has_news_easy_voice'] == True:
 #       voice_file = re.sub(r"[^\da-z\.]i", "", news['news_easy_voice_uri'])
 #       voice = {
 #           "uri": 'http://www3.nhk.or.jp/news/easy/' + str(news_id) + '/' + str(voice_file),
 #           "file": voice_file
 #       }
 #       # add audio tag to mp3 file
 #       link = """<audio preload="metadata" controls="controls">
 #               <source src="{src}" type="audio/mpeg; codecs=mp3" />
 #               <a href="{src}" target="_blank">Download voice file</a>
 #               </audio>""".replace("{src}", voice_file)
 #       article.append(BeautifulSoup(link, 'html.parser'))
 #
 #   else:
        voice = {}

    return {
        "content": str(title) + str(article),
        "voice": voice
    }

main()
