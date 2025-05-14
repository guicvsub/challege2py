import streamlit as st
import pandas as pd
from datetime import datetime
from endpoints.search import search_products
import os 
from endpoints.manufacturers import get_manufacturers
from algorithms import merge_sort, get_top_k_items, BinarySearchTree
import networkx as nx
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import math

# Carrega variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

# Configuração da página
st.set_page_config(page_title="Consulta de Veículos e Produtos", layout="wide")

# Título do aplicativo
st.title("🚗 Sistema de Consulta de Veículos e Produtos")

# Sidebar para configurações
with st.sidebar:
    st.header("Configurações")
    items_per_page = st.number_input("Itens por página", min_value=1, max_value=100, value=10)
    
# Abas para diferentes funcionalidades
tab1, tab2, tab3 = st.tabs(["Consulta de Produtos", "Lista de Montadoras", "Lojas e Rotas"])

with tab1:
    st.header("Consulta de Produtos por Veículo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fabricante = st.text_input("Fabricante do Produto", value="BOSCH")
    
    with col2:
        placa = st.text_input("Placa do Veículo", value="DEM8i14")
    
    # Opções de ordenação
    st.subheader("Opções de Ordenação")
    sort_col, order_col, k_col = st.columns(3)
    
    with sort_col:
        sort_key = st.selectbox("Ordenar por", 
                              ["codigoReferencia", "nomeProduto", "marca", "csa"], 
                              index=0,
                              format_func=lambda x: {
                                  "codigoReferencia": "Código Referência",
                                  "nomeProduto": "Nome do Produto",
                                  "marca": "Marca",
                                  "csa": "Código CSA"
                              }.get(x, x))
    
    with order_col:
        sort_order = st.selectbox("Ordem", ["Crescente", "Decrescente"], index=0)
    
    with k_col:
        top_k = st.number_input("Top K itens", min_value=1, max_value=100, value=5)
        get_top = st.checkbox("Obter apenas Top K")
    
    if st.button("Buscar Produtos", key="search_products"):
        with st.spinner("Buscando produtos..."):
            try:
                response = search_products(fabricante, placa, 0, items_per_page)
                
                if isinstance(response, dict) and "data" in response:
                    produtos_lista = response["data"]
                    count = len(produtos_lista)
                    
                    if produtos_lista:
                        st.success(f"Encontrados {count} produtos")
                        
                        # Extrair os dados de cada produto
                        produtos = []
                        for item in produtos_lista:
                            if isinstance(item, dict) and "data" in item:
                                produtos.append(item["data"])
                            else:
                                produtos.append(item)
                        
                        # Aplicar ordenação
                        produtos_ordenados = merge_sort(
                            produtos, 
                            key=sort_key, 
                            ascending=(sort_order == "Crescente")
                        )
                        
                        # Aplicar Top K se necessário
                        if get_top:
                            produtos_ordenados = get_top_k_items(
                                produtos_ordenados,
                                key=sort_key,
                                k=top_k,
                                largest=(sort_order == "Decrescente")
                            )
                        
                        # Criar DataFrame com campos relevantes
                        df_data = []
                        for produto in produtos_ordenados:
                            row = {
                                "Código": produto.get("codigoReferencia", ""),
                                "Nome": produto.get("nomeProduto", ""),
                                "Marca": produto.get("marca", ""),
                                "CSA": produto.get("csa", ""),
                                "CNA": produto.get("cna", ""),
                                "Família": produto.get("familia", {}).get("descricao", ""),
                                "Subfamília": produto.get("familia", {}).get("subFamilia", {}).get("descricao", "")
                            }
                            
                            similares = produto.get("similares", [])
                            if similares:
                                row["Similares"] = ", ".join([f"{s['marca']} {s['codigoReferencia']}" for s in similares])
                            
                            df_data.append(row)
                        
                        df = pd.DataFrame(df_data)
                        st.dataframe(df)
                        
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "Baixar como CSV",
                            csv,
                            f"produtos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            "text/csv",
                            key='download-csv'
                        )
                    else:
                        st.warning("Nenhum produto encontrado")
                else:
                    st.error("Estrutura de dados inválida retornada pela API")
            except Exception as e:
                st.error(f"Erro ao buscar produtos: {str(e)}")

    # Autocomplete com BST
    st.subheader("Autocomplete de Fabricantes")
    search_term = st.text_input("Digite o nome do fabricante para sugestões", "")
    
    if search_term:
        fabricantes = ["BOSCH", "VW", "FIAT", "FORD", "GM", "TOYOTA", "HONDA", "HYUNDAI", "VOLVO", "BMW"]
        bst = BinarySearchTree()
        for fab in fabricantes:
            bst.insert(fab, {"fabricante": fab})
        
        suggestions = bst.search_prefix(search_term.upper())
        
        if suggestions:
            st.write("Sugestões de fabricantes:")
            for sug in suggestions[:5]:
                st.write(f"- {sug['fabricante']}")
        else:
            st.write("Nenhuma sugestão encontrada")

with tab2:
    st.header("Lista de Montadoras de Veículos")
    
    if st.button("Buscar Montadoras", key="search_manufacturers"):
        with st.spinner("Buscando montadoras..."):
            try:
                response = get_manufacturers(0, items_per_page)
                
                if isinstance(response, dict) and "data" in response:
                    montadoras = response["data"]
                    count = len(montadoras)
                    
                    if montadoras:
                        st.success(f"Encontradas {count} montadoras")
                        
                        df = pd.DataFrame(montadoras)
                        st.dataframe(df)
                        
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "Baixar como CSV",
                            csv,
                            f"montadoras_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            "text/csv",
                            key='download-manufacturers'
                        )
                    else:
                        st.warning("Nenhuma montadora encontrada")
                else:
                    st.error("Estrutura de dados inválida retornada pela API")
            except Exception as e:
                st.error(f"Erro ao buscar montadoras: {str(e)}")

with tab3:
    st.header("🚚 Sistema de Rotas e Lojas Próximas")
    
    # Dados simulados de lojas
    lojas_simuladas = {
        "Loja Centro": {"endereco": "Rua XV de Novembro, 1000, Centro, Curitiba", "lat": -25.4284, "lon": -49.2673},
        "Loja Batel": {"endereco": "Avenida do Batel, 1500, Batel, Curitiba", "lat": -25.4352, "lon": -49.2945},
        "Loja Portão": {"endereco": "Avenida República Argentina, 3000, Portão, Curitiba", "lat": -25.4658, "lon": -49.2901},
        "Loja Santa Felicidade": {"endereco": "Avenida Manoel Ribas, 5000, Santa Felicidade, Curitiba", "lat": -25.4190, "lon": -49.3056},
        "Loja Boqueirão": {"endereco": "Rua da Cidadania Boqueirão, Boqueirão, Curitiba", "lat": -25.4820, "lon": -49.2897}
    }
    
    def calcular_distancia(coord1, coord2):
        return geodesic(coord1, coord2).km
    
    def criar_grafo_lojas(endereco_comprador, lojas):
        geolocator = Nominatim(user_agent="ancora_route_planner")
        try:
            location = geolocator.geocode(endereco_comprador)
            if not location:
                return None, None
            
            comprador_coords = (location.latitude, location.longitude)
            G = nx.Graph()
            G.add_node("Comprador", pos=comprador_coords, endereco=endereco_comprador)
            
            for nome, info in lojas.items():
                loja_coords = (info["lat"], info["lon"])
                distancia = calcular_distancia(comprador_coords, loja_coords)
                G.add_node(nome, pos=loja_coords, endereco=info["endereco"])
                G.add_edge("Comprador", nome, weight=distancia)
            
            return G, comprador_coords
        except Exception as e:
            st.error(f"Erro na geocodificação: {str(e)}")
            return None, None
    
    def calcular_rota_otimizada(grafo, ponto_partida, pontos_entrega):
        try:
            nodes = list(grafo.nodes())
            for i in range(len(nodes)):
                for j in range(i+1, len(nodes)):
                    if nodes[i] != "Comprador" and nodes[j] != "Comprador":
                        coord1 = grafo.nodes[nodes[i]]["pos"]
                        coord2 = grafo.nodes[nodes[j]]["pos"]
                        distancia = calcular_distancia(coord1, coord2)
                        grafo.add_edge(nodes[i], nodes[j], weight=distancia)
            
            for ponto in pontos_entrega:
                if ponto not in grafo:
                    return None, f"Ponto de entrega não encontrado: {ponto}"
            
            caminho = [ponto_partida]
            pontos_restantes = set(pontos_entrega)
            
            while pontos_restantes:
                ultimo_ponto = caminho[-1]
                menor_distancia = math.inf
                proximo_ponto = None
                
                for ponto in pontos_restantes:
                    try:
                        distancia = nx.shortest_path_length(grafo, ultimo_ponto, ponto, weight='weight')
                        if distancia < menor_distancia:
                            menor_distancia = distancia
                            proximo_ponto = ponto
                    except nx.NetworkXNoPath:
                        continue
                
                if proximo_ponto is None:
                    return None, "Não foi possível encontrar um caminho para todos os pontos"
                
                caminho.append(proximo_ponto)
                pontos_restantes.remove(proximo_ponto)
            
            rota_detalhada = []
            distancia_total = 0
            
            for i in range(len(caminho)-1):
                origem = caminho[i]
                destino = caminho[i+1]
                trecho = nx.shortest_path(grafo, origem, destino, weight='weight')
                
                for j in range(len(trecho)-1):
                    de = trecho[j]
                    para = trecho[j+1]
                    distancia = grafo.edges[de, para]['weight']
                    distancia_total += distancia
                    rota_detalhada.append({
                        "De": de,
                        "Para": para,
                        "Distância (km)": round(distancia, 2),
                        "Endereço Origem": grafo.nodes[de]["endereco"],
                        "Endereço Destino": grafo.nodes[para]["endereco"]
                    })
            
            return pd.DataFrame(rota_detalhada), round(distancia_total, 2)
        except Exception as e:
            return None, str(e)
    
    # Seção 1: Lojas mais próximas
    st.subheader("1. Encontrar Lojas Próximas")
    endereco_comprador = st.text_input("Digite seu endereço completo:", "Rua Marechal Deodoro, 500, Centro, Curitiba")
    
    if st.button("Buscar Lojas Próximas"):
        with st.spinner("Calculando distâncias..."):
            grafo_lojas, comprador_coords = criar_grafo_lojas(endereco_comprador, lojas_simuladas)
            
            if grafo_lojas is None:
                st.error("Não foi possível geocodificar o endereço. Por favor, tente um endereço mais completo.")
            else:
                distancias = []
                for loja in lojas_simuladas:
                    distancia = grafo_lojas.edges["Comprador", loja]["weight"]
                    distancias.append({
                        "Loja": loja,
                        "Distância (km)": round(distancia, 2),
                        "Endereço": lojas_simuladas[loja]["endereco"]
                    })
                
                df_distancias = pd.DataFrame(distancias).sort_values("Distância (km)")
                st.dataframe(df_distancias)
                
                st.subheader("Mapa de Lojas Próximas")
                mapa_data = {
                    "latitude": [comprador_coords[0]] + [lojas_simuladas[loja]["lat"] for loja in lojas_simuladas],
                    "longitude": [comprador_coords[1]] + [lojas_simuladas[loja]["lon"] for loja in lojas_simuladas],
                    "tipo": ["Comprador"] + ["Loja"] * len(lojas_simuladas),
                    "nome": ["Você"] + list(lojas_simuladas.keys())
                }
                st.map(pd.DataFrame(mapa_data), zoom=12)
    
    # Seção 2: Rota de entregas
    st.subheader("2. Planejamento de Rota de Entregas")
    ponto_partida = st.selectbox("Ponto de partida:", ["Comprador"] + list(lojas_simuladas.keys()))
    pontos_entrega = st.multiselect("Pontos de entrega:", list(lojas_simuladas.keys()))
    
    if st.button("Calcular Rota Otimizada") and pontos_entrega:
        with st.spinner("Calculando melhor rota..."):
            grafo_lojas, _ = criar_grafo_lojas(endereco_comprador, lojas_simuladas)
            rota_df, distancia_total = calcular_rota_otimizada(grafo_lojas, ponto_partida, pontos_entrega)
            
            if rota_df is not None:
                st.success(f"Rota calculada com sucesso! Distância total: {distancia_total} km")
                st.dataframe(rota_df)
                
                pontos_rota = []
                for _, row in rota_df.iterrows():
                    pontos_rota.append({
                        "latitude": grafo_lojas.nodes[row["De"]]["pos"][0],
                        "longitude": grafo_lojas.nodes[row["De"]]["pos"][1],
                        "ponto": row["De"]
                    })
                
                ultimo_ponto = rota_df.iloc[-1]["Para"]
                pontos_rota.append({
                    "latitude": grafo_lojas.nodes[ultimo_ponto]["pos"][0],
                    "longitude": grafo_lojas.nodes[ultimo_ponto]["pos"][1],
                    "ponto": ultimo_ponto
                })
                
                st.subheader("Mapa da Rota")
                st.map(pd.DataFrame(pontos_rota), zoom=12)
            else:
                st.error(f"Erro ao calcular rota: {distancia_total}")

# Rodapé
st.divider()
st.caption(f"© {datetime.now().year} - Sistema de Consulta de Veículos e Produtos")