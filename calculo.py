def calcular_media_necessaria(md1, meta_anual=70):
    """
    Calcula a nota necessária no 2º semestre para alcançar a média anual desejada.
    """
    md2_necessaria = 2 * meta_anual - md1  # Fórmula para calcular a média necessária do 2º semestre
    return md2_necessaria

def calcular_necessario_cp_gs(md2_necessaria, challenge, meta_semestre=70):
    """
    Calcula a média necessária para CP1, CP2, CP3 e Challenge no 2º semestre.
    """
    # Calcular a média do 2º semestre baseada nos 40% de CP e Challenge e 60% de GS
    cp_challenge_necessario = (md2_necessaria - 0.6 * challenge) / 0.4
    
    # Nota necessária para GS (60% do semestre)
    gs_necessario = (md2_necessaria - 0.4 * cp_challenge_necessario) / 0.6
    
    return cp_challenge_necessario, gs_necessario

def calcular_cp_minimo(cp_challenge_necessario):
    """
    Calcula o mínimo necessário para a soma das duas maiores notas dos CPs.
    """
    return cp_challenge_necessario / 2  # Como são 3 CPs, a soma das duas maiores deve alcançar o valor.

# Exemplo de média do 1º semestre (MD1)
md1 = 75  # Média do 1º semestre

# Calcular a média necessária do 2º semestre (MD2)
md2_necessaria = calcular_media_necessaria(md1)

# Exemplo de nota da Challenge (Challenge)
challenge = 60  # Nota da Challenge

# Calcular as notas mínimas necessárias para CPs e GS
cp_challenge_necessario, gs_necessario = calcular_necessario_cp_gs(md2_necessaria, challenge)

# Calcular o mínimo necessário para CP1, CP2, e CP3
cp_minimo = calcular_cp_minimo(cp_challenge_necessario)

# Exibir os resultados
print(f"\n🎯 Para alcançar uma média anual de 70%, você precisa de:")

print(f"1. Média necessária no 2º semestre: {md2_necessaria:.2f}")
print(f"2. Para os CPs e Challenge, a soma das duas maiores notas deve ser: {cp_challenge_necessario:.2f}")
print(f"3. Se dividir igualmente entre CP1 e CP2, cada um deve ter pelo menos: {cp_minimo:.2f}")
print(f"4. Nota mínima na Global Solution (GS): {gs_necessario:.2f}")
