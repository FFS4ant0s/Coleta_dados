import requests
from bs4 import BeautifulSoup


def buscar_telefone_apontador(cnpj):
    # URL de busca no Apontador
    url = f'https://www.apontador.com.br/busca?q={cnpj}'

    # Requisição HTTP
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Aqui você inspeciona a estrutura da página para encontrar o telefone
        # Modifique conforme o site
        telefone = soup.find('span', {'class': 'phone'})
        if telefone:
            return telefone.text.strip()
        else:
            return "Telefone não encontrado."
    else:
        return "Erro ao acessar o Apontador."


# Substitua pelo CNPJ desejado
cnpj = '12345678000195'
telefone = buscar_telefone_apontador(cnpj)

print(f'Telefone encontrado: {telefone}')
