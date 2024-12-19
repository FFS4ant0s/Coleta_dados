# import requests
# import pandas as pd
# from datetime import datetime, timedelta

# # Substitua pela sua chave da API
# API_KEY = "cedd6f5dc7f9f4beb07ba20f5263134dd7808b8808f712580ac9f5d45fd7b8a72f951fa7c426e3d7e3119ce0b1b154634704a6a615696b870d9a1f59c45af1f6"  # noqa: E501
# API_URL = "https://api.casadosdados.com.br/v5/cnpj/pesquisa"

# # Função para buscar CNPJs ativos com telefone celular


# def buscar_cnpjs_ativos_com_celular(data_inicial, data_final, limite=5, pagina=1):  # noqa: E501
#     headers = {
#         "api-key": API_KEY,  # Passando a chave de API no cabeçalho
#         "Content-Type": "application/json"
#     }

#     # Parâmetros da pesquisa
#     data = {
#         "filters": {
#             "situacao_atual": ['ATIVA'],  # Filtra para empresas ativas
#             "mais_filtros": {
#                 "com_telefone": True,  # Garantir que a empresa tem um telefone # noqa: E501
#                 "somente_celular": True  # Garantir que o telefone é celular
#             },
#             "data_abertura": {
#                 "inicio": data_inicial,  # Usando a variável 'data_inicial'
#                 "fim": data_final,  # Usando a variável 'data_final'
#             },
#         },
#         # Limite de 5 CNPJs por página (ajustar conforme necessário)
#         "limite": limite,
#         "pagina": pagina  # Página de resultados
#     }

#     # Requisição POST para a API
#     response = requests.post(API_URL, headers=headers, json=data)

#     # Verifica se a requisição foi bem-sucedida
#     if response.status_code == 200:
#         dados = response.json()

#         # Exibe a resposta completa da API para verificar a estrutura dos dados # noqa: E501
#         print("Resposta da API:", dados)

#         # Estrutura para armazenar os dados
#         cnpjs_data = []

#         # Extrai os dados do retorno da API
#         for item in dados.get("cnpjs", []):
#             razao_social = item.get("razao_social", "Não Disponível")
#             cnpj = item.get("cnpj", "Não Disponível")
#             situacao_atual = item.get("situacao_cadastral", {}).get(
#                 "situacao_atual", "Desconhecida")

#             # Tentando obter o telefone de diferentes campos
#             # Tentando o campo "numero"
#             telefone_celular = item.get("numero", None)
#             if telefone_celular is None:
#                 # Tentando "telefone_celular"
#                 telefone_celular = item.get("telefone_celular", None)
#             if telefone_celular is None and "contatos" in item:  # Tentando buscar no campo "contatos" # noqa: E501
#                 for contato in item["contatos"]:
#                     telefone_celular = contato.get("numero", None)
#                     if telefone_celular:
#                         break

#             # Se não encontrar telefone, marcar como "Não informado"
#             if telefone_celular is None:
#                 telefone_celular = "Não informado"

#             # Adiciona os dados ao array
#             cnpjs_data.append({
#                 "Razão Social": razao_social,
#                 "CNPJ": cnpj,
#                 "Situação Atual": situacao_atual,
#                 "Número de Telefone": telefone_celular
#             })

#         # Criar DataFrame do Pandas
#         df = pd.DataFrame(cnpjs_data)
#         return df
#     else:
#         print(f"Erro na requisição: {response.status_code}")
#         print(response.text)  # Para verificar o erro detalhado
#         return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro


# # Definir o intervalo da última semana (calculando as datas corretamente)
# hoje = datetime.today()
# sete_dias_antes = hoje - timedelta(days=7)
# data_inicial = sete_dias_antes.strftime("%Y-%m-%d")
# data_final = hoje.strftime("%Y-%m-%d")

# # Buscar dados para várias páginas
# df_cnpjs_total = pd.DataFrame()  # DataFrame para armazenar todos os resultados # noqa: E501

# # Definindo número de páginas
# # Número de páginas a consultar (ajustar conforme necessário)
# num_paginacoes = 3

# # Buscar dados de várias páginas
# for pagina in range(1, num_paginacoes + 1):
#     df_cnpjs = buscar_cnpjs_ativos_com_celular(
#         data_inicial=data_inicial, data_final=data_final, limite=5, pagina=pagina)  # noqa: E501
#     df_cnpjs_total = pd.concat([df_cnpjs_total, df_cnpjs], ignore_index=True)

# # Verificar se há dados
# if not df_cnpjs_total.empty:
#     # Salvar em uma planilha Excel
#     df_cnpjs_total.to_excel(
#         "CNPJs_ativos_com_telefone_celular.xlsx", index=False)
#     print("Planilha gerada com sucesso!")
# else:
#     print("Nenhum dado encontrado ou erro na requisição.")
