import requests
from config import BASE_URL
from api.auth import get_access_token

def get_manufacturers(pagina=0, itens=100):
    token = get_access_token()
    url = f"{BASE_URL}/superbusca/api/integracao/veiculo/montadoras/query"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"pagina": pagina, "itensPorPagina": itens}
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()
    return r.json()
