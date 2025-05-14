import requests
from api.auth import get_access_token
from config import BASE_URL

def search_summary(veiculo_placa, superbusca, pagina=0, itens_por_pagina=100):
    # Obter token de acesso
    token = get_access_token()
    url = f"{BASE_URL}//superbusca/api/integracao/catalogo/v2/produtos/query/sumario"

    # Definir os cabeçalhos da requisição
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Definir o corpo da requisição
    payload = {
        "veiculoFiltro": {
            "veiculoPlaca": veiculo_placa
        },
        "superbusca": superbusca,
        "pagina": pagina,
        "itensPorPagina": itens_por_pagina
    }

    # Realizar a requisição POST
    response = requests.post(url, headers=headers, json=payload)

    # Verificar se a resposta é bem-sucedida
    response.raise_for_status()
    
    # Obter o conteúdo da resposta
    response_data = response.json()

    # Estruturar o resultado para devolver de forma resumida
    page_result = response_data.get("pageResult", {})
    
    vehicle_info = page_result.get("vehicle", {})
    product_data = page_result.get("data", [])
    
    result = {
        "count": page_result.get("count", 0),
        "vehicle": {
            "montadora": vehicle_info.get("montadora", ""),
            "modelo": vehicle_info.get("modelo", ""),
            "versao": vehicle_info.get("versao", ""),
            "chassi": vehicle_info.get("chassi", ""),
            "motor": vehicle_info.get("motor", ""),
            "combustivel": vehicle_info.get("combustivel", ""),
            "cambio": vehicle_info.get("cambio", ""),
            "carroceria": vehicle_info.get("carroceria", ""),
            "anoFabricacao": vehicle_info.get("anoFabricacao", ""),
            "anoModelo": vehicle_info.get("anoModelo", ""),
            "linha": vehicle_info.get("linha", ""),
            "eixos": vehicle_info.get("eixos", ""),
            "geracao": vehicle_info.get("geracao", "")
        },
        "data": [
            {
                "id": produto["id"],
                "nomeProduto": produto.get("nomeProduto", ""),
                "marca": produto.get("marca", ""),
                "codigoReferencia": produto.get("codigoReferencia", ""),
                "informacoesComplementares": produto.get("informacoesComplementares", ""),
                "imagemReal": produto.get("imagemReal", ""),
                "similares": produto.get("similares", [])
            } for produto in product_data
        ]
    }

    return result
