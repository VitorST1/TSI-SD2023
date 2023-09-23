import requests
from requests import exceptions
from bs4 import BeautifulSoup

def get_links(url): #
    '''
    Obtém todos os links da página indicada pela url.
    Retorna None caso a url seja inválida ou a página não exista,
    ou uma lista com os links da página.
    '''
    # Padroniza a URL.
    url = standardize_url(url)

    # Cria a requisição.
    response = create_request(url)

    if not response: 
        return None

    # Extrai os links da página.
    links = create_links_list(url, BeautifulSoup(response.content, 'html.parser'))

    if not links: 
        return None

    return links
# get_links()

## Padroniza a URL recebida pela API.
def standardize_url(url: str): #
    if not url.startswith("https://") and not url.startswith("http://"):
        url = "https://" + url  # Adiciona "https://" por padrão

    parsed_url = url.split("//")
    domain = parsed_url[1] if len(parsed_url) > 1 else parsed_url[0]

    if not domain.startswith("www."):
        url = url.replace(domain, "www." + domain)

    return url
#


def create_request(url, ssl_cert = True): #
    """
    Cria uma requisição e retorna a resposta.
    Tenta criar uma requisição efetuando a verificação dos certificados SSL, 
    caso não consiga cria ignorando a verificação.
    """
    try:
        return requests.get(url)
    except (exceptions.SSLError):
        return requests.get(url, verify=False)
    except (exceptions.ConnectionError, exceptions.MissingSchema, 
            exceptions.InvalidSchema, exceptions.InvalidURL):
        return None
    except Exception:
        return None
#

# Extrai os links da página.
def create_links_list(url: str, soup: BeautifulSoup): #
    links = []
    for link_tag in soup.find_all('a', class_='summary url'):
        # print(link_tag)
        link_href = link_tag.get('href')
        
        if(link_href):
            treated_link = treatLink(url,link_href)
       
            if link_href:
                links.append(
                   link_tag.text
                )
      
    return links
#


## Trata o link de referência local da página. (ex.: '/favoritos')
# Retorna um link válido. (ex.: 'https://seusite.com/favoritos')
def treatLink(url_page: str, link: str): #
    if link.startswith("/"):
        return f"{url_page}{link}"
    if link.startswith("#"):
        return url_page
    
    return link
#