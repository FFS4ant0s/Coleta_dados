import requests

API_KEY = "cedd6f5dc7f9f4beb07ba20f5263134dd7808b8808f712580ac9f5d45fd7b8a72f951fa7c426e3d7e3119ce0b1b154634704a6a615696b870d9a1f59c45af1f6"  # noqa: E501
API_URL = "https://api.casadosdados.com.br/v4/plano/saldo"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.get(API_URL, headers=headers)

if response.status_code == 200:
    print("Requisição bem-sucedida")
    print(response.json())  # Exibe os dados retornados
else:
    print(f"Erro na requisição: {response.status_code}")
    print(response.text)  # Exibe o erro detalhado
