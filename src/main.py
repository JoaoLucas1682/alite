import pickle
import random
import difflib
import sys
import os
import string
from datetime import datetime

class AlitePTCEngine:
    def __init__(self, binary_file):
        
        
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
        now = datetime.now()
        tags = {
            "time_minutes": now.strftime("%M"),
            "time_seconds": now.strftime("%S"),
            "time_hours": now.strftime("%H"),
            "date": now.strftime("%x"),
            "bot_name": self.bot_name
        }

        for tag, value in tags.items():
            marker = "${" + tag + "}"
            if marker in text:
                text = text.replace(marker, str(value))
        return text

    def select_response(self, key):
        total_responses = self.memory[key]
        used_responses = self.history[key]

        available_stock = [r for r in total_responses if r not in used_responses]

        if not available_stock:
            used_responses.clear()
            available_stock = total_responses

        choice = random.choice(available_stock)
        used_responses.append(choice)
        return choice

    def get_response(self, input_text):
        input_text = input_text.lower().strip()
        found_key = None

        if input_text in self.memory:
            found_key = input_text
        else:
            matches = difflib.get_close_matches(input_text, self.memory.keys(), n=1, cutoff=0.7)
            if matches:
                found_key = matches[0]

        if found_key:
            raw_response = self.select_response(found_key)
            return self.process_tags(raw_response)
            
        return "Desculpe, mas não tenho uma resposta para isso. Tente outra pergunta."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        file_path = "final.ptai" if os.path.exists("final.ptai") else None
        if not file_path:
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