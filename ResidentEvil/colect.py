#%%

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://www.residentevildatabase.com/personagens/',
    'Connection': 'keep-alive',
    # 'Cookie': '_ga_DJLCSW50SC=GS2.1.s1761040754$o1$g1$t1761042329$j59$l0$h0; _ga=GA1.1.1167708344.1761040755; _ga_D6NF5QC4QT=GS2.1.s1761040754$o1$g1$t1761042329$j59$l0$h0; FCNEC=%5B%5B%22AKsRol9FlzjDj3Dl80s7PjxIHozLmaUE_REw12s8i7C3G6gG0z3i6kpQS3Ukuj4lA01rsA_hH2Iz5frealG9bKhsGjn0bijrW0N6cTY-rlkecCfhD9-Ld96K3E-OyxFxT_YKQXAna2WpDu0R0mz9EqSC2hS3l5uuoQ%3D%3D%22%5D%5D',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

url = "https://www.residentevildatabase.com/personagens/leon-s-kennedy/"

resp = requests.get(url, headers=headers)

#%%

resp.status_code

#%%

soup = BeautifulSoup(resp.text)
soup

#%%

soup.find("div", class_ = "td-page-content")