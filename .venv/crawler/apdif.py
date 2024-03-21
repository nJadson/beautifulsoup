import requests
import pandas as pd
from bs4 import BeautifulSoup


def conexao(): ## Define a conexão com o site (Parametro reutizável) ##
    link = input("Digite o URL para coleta dos dados: ")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    
    # Decidi colocar o Try-except | Pois houveram alguns erros de conexão e como uma forma de previnir, adicionei para tratar adequatamente esses erros. 
    # Também evita várias chamadas durante a request (Evitando que o site me derrube e melhora também a eficiência)
    try: 
        response = requests.get(link, headers=headers, timeout=30)
        response.raise_for_status()
        print(f"\nConexão bem-sucedida: {response}\n")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Erro ao tentar conectar: {e}\n")
        return None

def extracao(): ## Chama conexão e Extrair os dados contidos na página ##
    response = conexao() # Guarda em response o que à request devolveu em conexao()

    if response: # Caso a conexão seja vem sucedida (code: 200) - Ele constinua e excuta o bloco if abaixo.
 
        soup = BeautifulSoup(response.text, 'html.parser')   # Usa soup para adequar o html e torná-lo legível. Resgata o txt gerado durante a conexão para isto.
        grids = soup.find_all("div", attrs={"class" : "grid-posts"}) #Identifiquei que as informações dos CDS são contidos na div "gri-post" - Então à referencio para as chamadas abaixo
        data = [] # Crio a lista Data, que armazenará todas as informações ao final do processo

        for grid in grids: # Laço para criar a iteração e buscar todas as informações que preciso na pagina.
            grid = soup.find_all("div", attrs={"class" : "post-info"}) # Salvou na variável grid minha segunda referência para busca.

            for info in grid: # Inicio uma iteração do resultado de outra (Basicamente ele começará a verificar todos os post-info que estão apenas em grid-posts) Assim, evito consumir lixo.
                data_value = [] #  Define-se uma lista para organizar e armazena os dados em appends.
                
                # Obtendo informações para composição do XLS #

                # Coleta o Title e armazena em data_title #
                data_title = info.find("h2", class_="post-title").find('a').text
                data_value.append(data_title)

                # Coleta a Data da postagem e armazena em data_date #
                data_date = info.find('time', class_='post-datepublished')
                if data_date:
                    data_date = data_date.text.strip()
                    data_value.append(data_date)
                else:
                    data_value.append("Data não disponível")

                # Coleta a nome do autor da publicação e armazena em data_authorpb #
                data_authorpb = info.find('span', class_='post-author')
                if data_authorpb and data_authorpb.find('a'): # Controle if para tratar publicações em autores, pois existiam mais 'a' sem informações ou blocos onde não tinham 'a'.
                    data_authorpb = data_authorpb.find('a').text
                else:
                    data_authorpb = "Autor não disponível"
                data_value.append(data_authorpb)

                # Coleta o URL da publicação e armazena em data_urlpb #
                data_urlpb = info.find('a')['href']
                data_value.append(data_urlpb)

                # Coleta o URL que permite o download e armazena em data_urlpb #
                data_linkdw = refdownload(data_urlpb)
                data_value.append(data_linkdw)

                # Adicionando os dados extraídos à lista de dados       
                data.append(data_value)
                
                # Controle de lixo = Removerá listas do grid "Top Musicas e outros" que não possuem todas informações e vem duplicados às vezes.
                data = [item for item in data if 'Data não disponível' not in item and 'Autor não disponível' not in item]

            if not data:  # Verifica se a lista de dados está vazia
                print("Nenhuma informação encontrada na página.")
            else:
                print("Informação encontrada e adicionada ao XLSX\n")
            return data # Devolve o valor dos dados

def refdownload(data_urlpb): ## Função apra acessar à página da URL da publicação e resgatar o link de download ##
    try: # Aqui resolvi deixar mais simples porém com o try para evitar erros #
        response = requests.get(data_urlpb, timeout=30)
        response.raise_for_status()
            
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            download_button = soup.find('a', {'data-download-count': True}) # Aqui encontramos o botão do download e extraímos o link

            if download_button: # Verificação do botão - Caso positivo ele vai retornar o Link que encontro no botão pela função refdownload.
                refdownload = download_button.get('onclick').split("'")[1]
                return refdownload
            else:
                return "Link de download não encontrado"

    except requests.exceptions.RequestException as e: # Trativa para erro, devolve "" e imprime o erro.
        print(f"Erro ao tentar conectar: {e}\n")
        return None

def xlsx_convert(data): # Conversão para arquivo XLSX #
    try: #Bloco que verifica se a planilha já existe. Caso positivo ela concatena e adiciona ao final
        verifica_arquivo = pd.read_excel("dados_publicacoes.xlsx")
        concatena_dados = pd.concat([verifica_arquivo, pd.DataFrame(data, columns=["Título da Publicação", "Data da Publicação", "Publicado por", "URL da Publicação", "URL do Download"])], ignore_index=True)
        concatena_dados.to_excel("dados_publicacoes.xlsx", index=False)
        print("\nOs dados foram adicionados à planilha existente com sucesso.")

    except FileNotFoundError: # Primeira exceção, caso não exista planilha ele cria e adiciona os primeiros valores.
        df = pd.DataFrame(data, columns=["Título da Publicação", "Data da Publicação", "Publicado por", "URL da Publicação", "URL do Download"])
        df.to_excel("dados_publicacoes.xlsx", index=False)
        print("\nArquivo XLSX(Excel) criado com sucesso.")

    except Exception as e: # Segunda exceção, casso venha a dar problema ele devovlerá um print com erro
        print(f"Ocorreu um erro ao tentar adicionar os dados à planilha existente: {e}")


def inicializacao(): # Bloco de inicialização com interação c/ usuário
    print("\n O processo finalizou e pagina foi convertida com sucesso. Deseja continuar?")
    opcao = input("Digite 1 para continuar ou 2 para interromper:  ")
    while (opcao != "2"):
        if opcao == "1":
            data = extracao()
            xlsx_convert(data)
            opcao = input("Digite 1 para continuar ou 2 para interromper:  ")
        elif opcao == "2":
            print("Obrigado! Programa encerrado")
        else:
            print("Opcao invalida. Programa encerrado!")

inicializacao() # Chamada para execução do código em forma monolítica