# endpoints/search.py
import requests
from api.auth import get_access_token
from config import BASE_URL

def search_products(fabricante="BOSCH", placa="DEM8i14", pagina=0, itens=100):
    token = get_access_token()  # Obtenção do token feita no backend
    url = f"{BASE_URL}/superbusca/api/integracao/catalogo/produtos/query"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "produtoFiltro": {"nomeFabricante": fabricante},
        "veiculoFiltro": {"veiculoPlaca": placa},
        "pagina": pagina,
        "itensPorPagina": itens
    }
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    response_data = r.json()  # Obtém a resposta inteira
    # Retorna apenas os dados relevantes, como "count" e os "produtos" dentro de "pageResult"
    page_result = response_data.get("pageResult", {})
    return {
        "count": page_result.get("count", 0),  # Número total de resultados
        "data": [produto["data"] for produto in page_result.get("data", [])]  # Extraindo apenas a parte "data" dos produtos
    }
