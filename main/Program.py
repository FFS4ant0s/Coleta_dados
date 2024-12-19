import requests
import pandas as pd

# Substitua pela sua chave de API
API_KEY = "cedd6f5dc7f9f4beb07ba20f5263134dd7808b8808f712580ac9f5d45fd7b8a72f951fa7c426e3d7e3119ce0b1b154634704a6a615696b870d9a1f59c45af1f6"  # noqa: E501
API_URL = "https://api.casadosdados.com.br/v5/cnpj/pesquisa"


def buscar_cnpjs_com_telefone(data_inicial, data_final, limite=100, pagina=1):
    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "situacao_cadastral": ["ATIVA"],
        "mais_filtros": {"com_telefone": True},
        "uf": ["df"],  # Alterar conforme necessário
        "data_abertura": {"inicio": data_inicial, "fim": data_final},
        "limite": limite,
        "pagina": pagina
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None


# Definir intervalo de datas
hoje = "2024-12-18"
sete_dias_antes = "2024-12-18"

# Criar uma lista para armazenar os dados de CNPJ
dados_para_planilha = []

# Ajuste para pegar várias páginas
for pagina in range(1, 6):  # Limite de 5 páginas (ajuste conforme necessário)
    dados_cnpjs = buscar_cnpjs_com_telefone(
        data_inicial=sete_dias_antes, data_final=hoje, limite=100, pagina=pagina  # noqa: E501
    )

    if dados_cnpjs:
        for item in dados_cnpjs.get('cnpjs', []):
            cnpj = item.get('cnpj', 'Não informado')
            razao_social = item.get('razao_social', 'Não disponível')
            nome_fantasia = item.get('nome_fantasia', 'Não disponível')

            # Extrair números de telefone dos contatos
            contatos = item.get('contatos', [])
            telefones = []
            if contatos:
                for contato in contatos:
                    tipo = contato.get('tipo', 'Desconhecido')
                    numero = contato.get('numero', 'Não informado')
                    telefones.append(f"{tipo}: {numero}")
            else:
                telefones.append("Nenhum telefone encontrado.")

            # Situação cadastral
            situacao = item.get('situacao_cadastral', {}).get(
                'situacao_atual', 'Desconhecida')

            # Adicionar os dados na lista para a planilha
            dados_para_planilha.append({
                "CNPJ": cnpj,
                "Razão Social": razao_social,
                "Nome Fantasia": nome_fantasia,
                "Telefones": ', '.join(telefones),
                "Situação Cadastral": situacao
            })

# Criar um DataFrame do pandas com os dados coletados
df = pd.DataFrame(dados_para_planilha)

# Salvar o DataFrame em um arquivo Excel
arquivo_excel = "dados_cnpjs.xlsx"
df.to_excel(arquivo_excel, index=False)

print(f"Dados salvos em {arquivo_excel}")
