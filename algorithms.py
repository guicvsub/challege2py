import heapq
from typing import List, Dict

def merge_sort(data: List[Dict], key: str, ascending: bool = True) -> List[Dict]:
    """Implementação do Merge Sort para ordenar dicionários por uma chave específica."""
    if len(data) <= 1:
        return data
    
    mid = len(data) // 2
    left = merge_sort(data[:mid], key, ascending)
    right = merge_sort(data[mid:], key, ascending)
    
    return merge(left, right, key, ascending)

def merge(left: List[Dict], right: List[Dict], key: str, ascending: bool) -> List[Dict]:
    """Função auxiliar para o Merge Sort."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if ascending:
            condition = left[i][key] <= right[j][key]
        else:
            condition = left[i][key] >= right[j][key]
        
        if condition:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def get_top_k_items(data: List[Dict], key: str, k: int, largest: bool = True) -> List[Dict]:
    """Usa heap para obter os K maiores ou menores itens por uma chave específica."""
    if largest:
        return heapq.nlargest(k, data, key=lambda x: x[key])
    else:
        return heapq.nsmallest(k, data, key=lambda x: x[key])

class BinarySearchTree:
    """Árvore de busca binária para autocomplete."""
    def __init__(self):
        self.root = None
    
    def insert(self, value: str, data: Dict):
        """Insere um valor na árvore."""
        if not self.root:
            self.root = BSTNode(value, data)
        else:
            self.root.insert(value, data)
    
    def search_prefix(self, prefix: str) -> List[Dict]:
        """Busca todos os itens com um determinado prefixo."""
        if not self.root:
            return []
        return self.root.search_prefix(prefix)

class BSTNode:
    """Nó da árvore de busca binária."""
    def __init__(self, value: str, data: Dict):
        self.value = value.lower()
        self.data = data
        self.left = None
        self.right = None
    
    def insert(self, value: str, data: Dict):
        """Insere um novo valor na subárvore."""
        value_lower = value.lower()
        if value_lower < self.value:
            if self.left:
                self.left.insert(value_lower, data)
            else:
                self.left = BSTNode(value_lower, data)
        else:
            if self.right:
                self.right.insert(value_lower, data)
            else:
                self.right = BSTNode(value_lower, data)
    
    def search_prefix(self, prefix: str) -> List[Dict]:
        """Busca por prefixo na subárvore."""
        prefix = prefix.lower()
        results = []
        
        # Verifica se o nó atual começa com o prefixo
        if self.value.startswith(prefix):
            results.append(self.data)
        
        # Decide em qual subárvore continuar a busca
        if prefix < self.value or self.value.startswith(prefix):
            if self.left:
                results.extend(self.left.search_prefix(prefix))
        
        if prefix > self.value or self.value.startswith(prefix):
            if self.right:
                results.extend(self.right.search_prefix(prefix))
        
        return results