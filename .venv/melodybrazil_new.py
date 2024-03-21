import requests
import pandas as pd
from bs4 import BeautifulSoup


def conexao(): ## Define a conexão com o site (Parametro reutizável) ##
    link = "https://www.cdsdeaparelhagens.com/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        print(f"Conexão exitosa: {response}\n")
    else:
        print(f"Error: {response.status_code} ao realizar a tentativa de conexão\n")
    return response

def extrair_info(): ## Está funcional: trás [title, data, autor, url publicação e url download] ##
    
    soup = BeautifulSoup(conexao().text, 'html.parser')

    #localiza composição principal da div (onde tem todas infos):
    cd_temp = soup.find_all("div", attrs={"class" : "post-info"})
    data = []
    for datas in cd_temp:
        data_value = []

        #Obtendo informações
        data_title = datas.find("h2", class_="post-title").find('a').text
        data_value.append(data_title)

        #obtendo datas 
        data_date = datas.find('time', class_='post-datepublished')
        if data_date:
            data_date = data_date.text.strip()
            data_value.append(data_date)
        else:
            data_value.append("Data não disponível")

        # Obtendo autor da publicação se existir 
        data_authorpb = datas.find('span', class_='post-author')
        if data_authorpb and data_authorpb.find('a'):
            data_authorpb = data_authorpb.find('a').text
        else:
            data_authorpb = "Autor não disponível"
        data_value.append(data_authorpb)

        # obtendo URL de publicação
        data_urlpb = datas.find('a')['href']
        data_value.append(data_urlpb)

        # obtendo link de download a partir de URL de publicação
        data_linkdw = download_link(data_urlpb)
        data_value.append(data_linkdw)

        # Adicionando os dados extraídos à lista de dados       
        data.append(data_value)

        #Remove listas fora da div principal:
        data = [item for item in data if 'Data não disponível' not in item and 'Autor não disponível' not in item]

    if not data:  # Verifica se a lista de dados está vazia
        print("Nenhuma informação encontrada na página.")
    else:
        print(data)
    return data

def download_link(data_urlpb): ## Funcional, está trazendo o link do download do arquivo (Está função apoia a extrair_info)##
    
    response = requests.get(data_urlpb)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Aqui você precisa encontrar o botão de download e extrair o link
        download_button = soup.find('a', {'data-download-count': True})
        if download_button:
            download_link = download_button.get('onclick').split("'")[1]
            return download_link
        else:
            return "Link de download não encontrado"
    else:
        return "Não foi possível acessar a URL de publicação"

def save_to_excel(data):
    df = pd.DataFrame(data, columns=["Título da Publicação", "Data da Publicação", "Publicado por", "URL da Publicação", "URL do Download"])
    df.to_excel("dados_publicacoes.xlsx", index=False)
    print("Arquivo Excel criado com sucesso.")
    
data = extrair_info()
save_to_excel(data)