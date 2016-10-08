import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor

# if any suggestions or corrections please msg me <kanna.dharahas@gmail.com>

# Change only these three inputs , customise the functions if need be
# Input main keyword for searching
search = 'new york'
# Input if any keywords neccessary before the main keyword as ['a', 'b']
preKeywords = []
# Input if any keywords neccessary after the main keyword as ['a', 'b']
postKeywords = []


# Downloads images with respective name in the same folder
def download(link):
    img = link.rsplit('/', 1)[1]
    urllib.request.urlretrieve(link, img+".jpg")
    # print('Link-->'+link+' Done!!!')


# Creates multiple threads to download Images faster
def pool_threads(urls):
    # Using Async Concurrent Futures with 5threads downloading all images links
    pool = ThreadPoolExecutor(8)
    for link in urls:
        pool.submit(download, link)


#  Parses and generates url links from google image search
def get_links_download(string, l):
    try:
        print('Starting download for links related to---->'+string)
        if l is True:
            url = 'https://www.google.co.in/search?q='+string+'&tbm=isch&tbs=isz:l'
        else:
            url = 'https://www.google.co.in/search?q='+string+'&tbm=isch'
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        soup = BeautifulSoup(respData, 'html.parser')
        links = soup.find_all('div', 'rg_meta')

        # Saving links in the output file links.txt
        saveFile = open('links.txt', 'w')

        urls = []
        for link in links:
            obj = link.string
            obj = json.loads(obj)
            print(obj['ou'])
            urls.append(obj['ou'])
            saveFile.write(obj['ou']+'\n')

        # print(len(links))
        saveFile.close()
        # download(urls[0])
        pool_threads(urls)
        print('<--------------------Done!!! links related to-------->'+string+'\n\n')

    except Exception as e:
        print(str(e))


# Tries different combinations of the three input keywords to get maximum result
def urls_generate(search, preKeywords, postKeywords, l):
    print("=============Download Starting for Search " + search + " =======================")
    search = search.replace(' ', '+')
    string = search
    get_links_download(string, l)
    if len(preKeywords) > 0:
        for i in preKeywords:
            string = search
            string = i+'+'+string
            get_links_download(string, l)
            if len(postKeywords) > 0:
                for j in postKeywords:
                    string = string+'+'+j
                    get_links_download(string, l)

    else:
        if len(postKeywords) > 0:
            for j in postKeywords:
                string = string+'+'+j
                get_links_download(string)


# Used for calling the above process (Main function)
urls_generate(search, preKeywords=preKeywords, postKeywords=postKeywords, l=False)


# If you need larger image sizes change l = True like the below comment
# urls_generate(search, preKeywords=preKeywords, postKeywords=postKeywords, l=True)
