from modules.difference import calculate_similarity, normalize_text

def rodar_testes():
    testes = [
        ("Olá", "ola"),                 # Teste de acentuação
        ("Como vc esta?", "como você está"), # Teste de similaridade/abreviação
        ("DevOps", "devops"),           # Teste de case sensitive
        ("Python!", "python"),          # Teste de pontuação
        ("Abacaxi", "Carro"),           # Teste de palavras totalmente diferentes
        ("O que é extrativismo?", "o que e extrativismo") # Teste longo
    ]

    print(f"{'INPUT':<25} | {'TARGET':<25} | {'SCORE':<10}")
    print("-" * 65)

    for entrada, alvo in testes:
        score = calculate_similarity(entrada, alvo)
        status = "✅" if score >= 0.7 else "❌"
        print(f"{entrada:<25} | {alvo:<25} | {score:.2f} {status}")

if __name__ == "__main__":
    print("--- TESTANDO MOTOR ALITE (Módulo Difference) ---")
    rodar_testes()