import pickle
import os
import re
from sys import argv

def export():
    if len(argv) < 2:
        print("Uso: python export.py <treino.txt> <(opcional) saída.ptc>")
        return
    input_file = argv[1]
    output_file = argv[2] if len(argv) >=3 else "output.ptai"
    
    config = {
        "bot_name": "Chatbot",
        "model_name": "Generic Chatbot Model v?"
    }
    
    memory = {}

    if not os.path.exists(input_file):
        print(f"Erro: {input_file} não encontrado!")
        return

    with open(input_file, 'r', encoding='utf-8') as file:
        current_questions = []
        
        for line in file:
            line = line.strip()
            
            if line.startswith('!#'):
                name_match = re.search(r"Name:\s*'([^']*)'", line)
                model_match = re.search(r"ModelName:\s*'([^']*)'", line)
                
                if name_match:
                    config["bot_name"] = name_match.group(1)
                if model_match:
                    config["model_name"] = model_match.group(1)
                
                print(f"Configurações detectadas: {config['bot_name']} | {config['model_name']}")
                continue
            
            if not line or line.startswith('#'): continue
            
            if line.startswith('>'):
                content = line[1:].strip()
                current_questions = [question.strip().lower() for question in content.split('|')]
                
                for question in current_questions:
                    if question not in memory:
                        memory[question] = []
            
            elif line.startswith('-') and current_questions:
                response = line[1:].strip()
                for question in current_questions:
                    memory[question].append(response)

    package = {
        "config": config,
        "memory": memory
    }

    with open(output_file, 'wb') as file:
        pickle.dump(package, file)
    
    print(f"Sucesso! {len(memory)} padrões exportados para {output_file}")

if __name__ == "__main__":
    export()