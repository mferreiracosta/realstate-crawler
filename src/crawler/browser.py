import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from typing import Dict, List
import re


class BrowserRealState:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--hadless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable--web-security")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--memmory_pressure-off")
        self.chrome_options.add_argument("--ignore-certicate-errors")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("user-ageeent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'")
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        self.driver = webdriver.Chrome(options=self.chrome_options)

    def execute_command(self):
        htmls = []
        html = self.get_html(page_number=1)
        last_page_number = self.get_last_page_number(html)
        print(last_page_number)

        htmls.append(html)
        for page_number in range(2, last_page_number + 1):
            html = self.get_html(page_number=page_number)
            htmls.append(html)
        self.driver.quit()

        print(len(htmls))
        soup = BeautifulSoup(htmls[0], "html.parser")

        results: List[BeautifulSoup] = soup.find_all("div", class_="card-body")

        data = []
        result = results[0]

        # Extrair o link do anúncio
        link = result.find("a")["href"]

        # Extrair o código do imóvel
        codigo = link.split("/")[-1]

        # Extrair o endereço, bairro e tipo
        cidade = "Divinopolis"
        endereco = result.find("p", class_="endereco-rua").text
        bairro = result.find("p", class_="card-text text-center").text
        tipo = result.find("h6", class_="card-title").text

        # Extrair os atributos característicos (area, quartos, garagem) e quantitativos (preco, IPTU e condomínio)
        atributos_tag: BeautifulSoup = result.find("div", class_="col-15")
        caracteristicas = [item.text.strip() for item in atributos_tag.find_all("h6", class_="item-caracteristica")]
        area, dormitorios, garagem = caracteristicas[:3]
        valor = atributos_tag.find('h5', class_='card-text').text
        iptu = atributos_tag.find('p', text=lambda text: 'IPTU' in text).text
        condominio = atributos_tag.find('p', text=lambda text: 'Condomínio' in text).text.strip()

        data.append({"codigo": codigo, "tipo_imovel": tipo, "cidade": cidade, "bairro": bairro, "endereco": endereco, "area": area, "dormitorios": dormitorios, "garagem": garagem, "disponibilidade": "aluguel", "valor": valor, "valor_iptu": iptu, "valor_condominio": condominio, "link": link})

        print("Código:", codigo)
        print("Link:", link)
        print("Cidade:", cidade)
        print("Bairro:", bairro)
        print("Endereço:", endereco)
        print("Tipo do Imóvel:", tipo)
        print("Área:", area)
        print("Dormitórios:", dormitorios)
        print("Garagem:", garagem)
        print("Preço:", valor)
        print("IPTU:", iptu)
        print("Condomínio:", condominio)
        print("Disponibilidade:", "aluguel")


        print(data)

    def get_html(self, page_number: str):
        url = f"https://www.franciscoimoveis.com.br/aluguel/imoveis/todas-as-cidades/todos-os-bairros/0-quartos/0-suite-ou-mais/0-vaga-ou-mais/0-banheiro-ou-mais/sem-portaria-24horas/sem-area-lazer/sem-dce/sem-mobilia/sem-area-privativa/sem-area-servico/sem-box-despejo/sem-circuito-tv/?valorminimo=0&valormaximo=0&pagina={str(page_number)}"
        self.driver.get(url)
        time.sleep(5)
        html = self.driver.page_source

        return html

    def get_last_page_number(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        pagination = soup.find("div", class_="pagination d-flex justify-content-around align-items-center")
        onclick_attr = pagination.find_all("button")[-1]["onclick"]
        last_page_number = re.search(r'\((\d+)\)', onclick_attr).group(1)

        return int(last_page_number)

    

    def transform_df(self):
        pass