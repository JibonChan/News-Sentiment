import requests
import sys
import json
from datetime import datetime

path = 'storage/'

def getNewsResult(query):
    url_top = ('https://newsapi.org/v2/top-headlines?'
        'country=us&'
        'apiKey=1b80b28b0cbb41878ca732767e68a87a')

    url_search ='https://newsapi.org/v2/everything?'

    params = {
        'q': f'{query}',
        'from': datetime.today().strftime('%Y-%m-%d'),
        'sortBy': 'publishedAt',
        'apiKey': '1b80b28b0cbb41878ca732767e68a87a'
    }

    response = requests.get(url_search, params=params)

    return response.json()

def saveNews(data, filename):
    with open(f'{path + filename}.json', 'w') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


def main():
    n = len(sys.argv)
    query = ""
    for i in range(1,n):
        query += f'{sys.argv[i]} '

    # return
    data = getNewsResult(query)
    print(data)
    saveNews(data, query)

    exit(0)

main()