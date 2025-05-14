from endpoints.search import search_products
from endpoints.manufacturers import get_manufacturers
from endpoints.search_summary import search_summary
import json

if __name__ == "__main__":
    try:

        # Exemplo de chamada para obter os dados com base na placa e superbusca
        resultado = search_summary("DME8I14", "AMORTECEDOR", pagina=0, itens_por_pagina=100)

        # Exibir o resultado
        print(resultado)
        
        print("Buscando produtos...")
        resultado = search_products()
        print(json.dumps(resultado, indent=2, ensure_ascii=False))

        print("\nBuscando montadoras...")
        montadoras = get_manufacturers()
        print(json.dumps(montadoras, indent=2, ensure_ascii=False))
            
    except Exception as e:
        print(f"Erro durante execução: {e}")
