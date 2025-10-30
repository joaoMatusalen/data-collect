#%%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

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

def get_content(url):
    resp = requests.get(url, headers=headers)
    return resp

def get_basic_infos(soup):
    div_page = soup.find("div", class_ ="td-page-content")
    paragrafo = div_page.find_all("p")[1]
    ems = paragrafo.find_all("em")
    data = {}
    for i in ems:
        chave, valor, *_ = i.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")

    return data

def get_aparicoes(soup):

    lis = (soup.find("div", class_ = "td-page-content")
            .find("h4")
            .find_next()
            .find_all("li")
            )

    aparicoes = [i.text for i in lis]

    return aparicoes

def get_personagens_info(url):
    resp = get_content(url)

    if resp.status_code != 200:
        print("não foi possível encontrar os dados.")
        return {}
    else:
        soup = BeautifulSoup(resp.text, features="html.parser")
        data = get_basic_infos(soup)
        data["Aparições"] = get_aparicoes(soup)
        return data
    
def get_links():
    url = "https://www.residentevildatabase.com/personagens/"
    resp = requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(resp.text)
    ancoras = (soup_personagens.find("div", class_="td-page-content")
                               .find_all("a"))

    links = [i["href"] for i in ancoras]
    return links


#%%

url = "https://www.residentevildatabase.com/personagens/alex-wesker/"

links = get_links()
data = []
for i in tqdm(links):
    d = get_personagens_info(i)
    d["Link"] = i
    nome = i.strip("/").split("/")[-1].replace("-", " ").title()
    d["Nome"] = nome
    data.append(d)

#%%

df = pd.DataFrame(data)

#%%


df.to_parquet("dados_re.parquet", index=False)