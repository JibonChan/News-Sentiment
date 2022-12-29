import sys
import requests
import re
import json
from parsel import Selector

path = 'storage/'

def extractSourceLink(text='') -> str:
    link_p = r'href=[\'"]?([^\'" >]+)'
    link = re.search(link_p, text)
    return link[0]

def extractSourceName(text="") -> str:
    pat = r'<span>(.*?)</span>'
    out = re.findall(pat, text)
    return out[0]


def extractPostedDate(text="") -> str:
    pat = r'<span>(.*?)</span>'
    out = re.findall(pat, text)
    return out[1]


def extractImages(text="") -> str:
    pat = r'src="(.*?)"'
    out = re.findall(pat, text)
    return out


def extractHeading(text="") -> str:
    selector = Selector(text=text)
    data = selector.css('div').getall()

    return data


def extractElements(text="") -> str:
    selector = Selector(text=text)
    data = selector.css('div').getall()

    return data


def getData(q='') -> requests:
    q = q.strip()
    q = re.sub(' ', '+', q)
    no = 100

    url = 'https://www.google.com/search'

    params = {
        'q': q,
        'num': no,
        'biw': '1536',
        'bih': '121',
        'tbm': 'nws',
        'ei': 'STGrY9zDFNmYseMP0raj2AY',
        'oq': q,
        'gs_lcp': 'Cgxnd3Mtd2l6LW5ld3MQARgAMgoIABCxAxCDARBDMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEUABYAGCNHWgAcAB4AIABrgiIAa4IkgEDNy0xmAEAwAEB',
        'sclient': 'gws-wiz-news'
    }

    headers = {
        'Host': 'www.google.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'utf8',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive',
        # 'Cookie': 'NID=511=X_24SA9gtDAP3481faD13f1KsDM60Wmt6lEK2E8MiuQK2Pl2fBzyM2uCy86EUEynUqLQRA7yGtflgH1mijBCIIhE0pQzz3q4rbv9xe-KX0qO1ku3mGgQNB2qcVstIsls2Zw1Y8P8J6x2MDyv9Cc6I2Jz7ENYAtbUhEAHQBR8f7E9mVAsM_Ax2NzA3Q_ifecKIZ9DbC0FvCZ8PuiVsI2hTAxdRUaF038x9DM5A2n-9aWSQtSaW7obW0fusI2R4QtphXo; SID=RwhRnC_3hsPLeQV7wvIagXLfCVhvRR8KWXz-576ZII4Fjw5zsdtJaoqyxVsHh9U5kkLyOA.; __Secure-1PSID=RwhRnC_3hsPLeQV7wvIagXLfCVhvRR8KWXz-576ZII4Fjw5z4sFEaiJjcKKSiXiZW55CcQ.; __Secure-3PSID=RwhRnC_3hsPLeQV7wvIagXLfCVhvRR8KWXz-576ZII4Fjw5zr0NyQwZGYfXzJrS2uKuwUQ.; HSID=AV_ca_bJZJk54P7Wm; SSID=A7lkpy1CQPynNiMC3; APISID=ThOXaKTC62yrtCAY/AMPIqO2g9imM5j5e-; SAPISID=YPtwFzMF_urMWo12/AAcG-SRo4KVBUPnP2; __Secure-1PAPISID=YPtwFzMF_urMWo12/AAcG-SRo4KVBUPnP2; __Secure-3PAPISID=YPtwFzMF_urMWo12/AAcG-SRo4KVBUPnP2; SIDCC=AIKkIs1ooXpmyFMWDJbX8xSPgHvjP9qN8v4a5bEnrVB3uNEGLZz9mg4n99pS1-zvCrdznHdkMptV; __Secure-1PSIDCC=AIKkIs0lgux0PRniZSbIDN0N0PAWpDoLp8AXB4wbe1pWffmGQq8CvOqI-hAz-0CYWXoJoQx38Ns; __Secure-3PSIDCC=AIKkIs3n-C5sMh31acsjQlHFdhq3OcIWnCEhyVvUUt157aFvb1MK3YcT7bdpM_Fbdt0rdswloWg; 1P_JAR=2022-12-27-17; AEC=AakniGMmjdiVTVuxI-bv0bM5xzctBIw-XM7hX-ImfVoqD5Nbd2JwNup12A; OGPC=19027681-1:; DV=ozYdU8G8CGsq8M_bUqimj4g16gRLVdhh6_XJcm-gWwEAAAA',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
    }

    data = requests.get(url=url, headers=headers, params=params)
    
    with open(f'{path}{q}.html','w') as f:
        f.write(data.text)

    return data.text


def parseData(html, query):
    selector = Selector(text=html)
    data = selector.css('#search div div div div a').getall()

    count = 0
    output = []

    for div in data:
        extracted = extractHeading(div)

        temp = {}
        temp['link'] = extractSourceLink(div)
        try:
            temp['createdAt'] = extractPostedDate(div)
            temp['sourceName'] = extractSourceName(div)
            temp['title'] = re.findall(r'role="heading">(.*?)</div>', re.sub('<br>|\n', '', extracted[6]))[0]
            temp['thumbnail'] = ''
            temp['description'] = re.findall(r'>(.*?)</div>', re.sub('<br>|\n', '', extracted[7]))[0]
        except:
            # print("oops")
            pass
        output.append(temp)

    with open(f'{path}{query}.json','w') as f:
        f.write(json.dumps(output, indent=4, ensure_ascii=False))
    
    return json.dumps(output, indent=4, ensure_ascii=False)



# getData()
# with open('outp.html','r') as f:
#     data = f.read()
#     parseData(data)

def main():
    n = len(sys.argv)
    query = ""
    for i in range(1,n):
        query += f'{sys.argv[i]} '
    html = getData(query)
    data = parseData(html, query)
    print(data)

    exit(0)

main()