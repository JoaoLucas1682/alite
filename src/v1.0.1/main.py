import pickle
import random
from modules.difference import calculate_similarity
import sys
import os
import string
from datetime import datetime

class AlitePTCEngine:
    def __init__(self, binary_file):
        self.default_response = "No momento não possuo essa informação em meu banco de dados."
        
        if not os.path.exists(binary_file):
            print(f"Erro: Arquivo {binary_file} não encontrado!")
            sys.exit(1)
            
        try:
            with open(binary_file, 'rb') as file:
                data = pickle.load(file)
                
            if isinstance(data, dict) and "config" in data and "memory" in data:
                self.config = data["config"]
                self.memory = data["memory"]
            else:
                self.config = {"bot_name": "Chatbot", "model_name": "Generic Chatbot Model"}
                self.memory = data

            self.bot_name = self.config.get("bot_name", "Chatbot")
            self.model_name = self.config.get("model_name", "Unknown")
            
            self.history = {key: [] for key in self.memory.keys()}
            
            print(f"{self.bot_name} iniciado | Modelo: {self.model_name}")
            print(f"{len(self.memory)} conhecimentos carregados.")
            
        except Exception as e:
            print(f"Erro ao ler o cérebro: {e}")
            sys.exit(1)

    def generate_random_ascii(self, length=15):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def process_tags(self, text):
        if "${" not in text:
            return text

        now = datetime.now()
        tags = {
            "time_minutes": now.strftime("%M"),
            "time_seconds": now.strftime("%S"),
            "time_hours": now.strftime("%H"),
            "date_year": now.strftime("%Y"),
            "twonumber_year": now.strftime("%y"),
            "date": now.strftime("%x"),
            "yearday": now.strftime("%j"),
            "bot_name": self.bot_name
        }

        for tag, value in tags.items():
            marker = "${" + tag + "}"
            if marker in text:
                text = text.replace(marker, str(value))
        return text

    def select_response(self, key):
        total_responses = self.memory[key]
        used_list = self.history[key]
        used_set = set(used_list)

        available_stock = [r for r in total_responses if r not in used_set]

        if not available_stock:
            used_list.clear()
            available_stock = total_responses

        choice = random.choice(available_stock)
        used_list.append(choice)
        return choice

    def get_response(self, input_text):
        input_text = input_text.strip()
        found_key = None

        if input_text in self.memory:
            found_key = input_text
        else:
            best_key = None
            highest_score = 0
            
            for key in self.memory.keys():
                score = calculate_similarity(input_text, key)
                
                if score > highest_score and score >= 0.7:
                    highest_score = score
                    best_key = key
            
                if highest_score >= 0.92:
                    break

            found_key = best_key
        if found_key:
            raw_response = self.select_response(found_key)
            return self.process_tags(raw_response)
            
        return self.default_response

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.ptc>")
        sys.exit(1)
    else:
        file_path = sys.argv[1]

    ai = AlitePTCEngine(file_path)
    
    print(f"\n--- {ai.bot_name} - CONVERSA ---")
    print("Dica: Digite '@cbexit' sem aspas para encerrar.\n")

    while True:
        try:
            user_input = input("Você > ")
            if user_input.lower() in ['@cbexit']:
                print(f"SISTEMA > Encerrando a conversa. Até mais!")
                break
            if not user_input.strip():
                continue

            response = ai.get_response(user_input)
            print(f"{ai.bot_name} > {response.replace('\\n', '\n')}")
            
        except KeyboardInterrupt:
            print("\nEncerrando...")
            break