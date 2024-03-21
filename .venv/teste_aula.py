import requests
from bs4 import BeautifulSoup

def exemplo_google():
    #Usamos o link abaixo, para encontrar o site para realizarmos a raspagem dos dados:
    link = "https://www.google.com/search?q=cotacao+do+dolar"
    #link = "https://www.google.com/search?q=Furry+fandom"
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}

    requisicao = requests.get(link, headers=headers)
    print(f"{requisicao}\n")
    #print(request.text)

    site = BeautifulSoup(requisicao.text, "html.parser")
    #print(site.prettify())

    #titulo = site.find("title")
    pesquisa = site.find_all("input")
    pesquisa2 = site.find("textarea", class_="gLFyf")
    print(pesquisa2)

#def cotacao_dolar():
def cotacao_dolar():
    link = "https://www.google.com/search?q=cotacao+do+dolar"
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    request = requests.get(link, headers=headers)
    print(f"{request}\n")

    site = BeautifulSoup(request.text, "html.parser")
    cotacao_dolar = site.find("span", class_="SwHCTb")
    print(cotacao_dolar.get_text())
    print(cotacao_dolar["data-value"])

cotacao_dolar()