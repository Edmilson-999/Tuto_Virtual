# app.py
from modules.chatbot import gerar_resposta

def main():
    print("=== Tutor Virtual Inteligente ===\n")
    while True:
        pergunta = input("👨‍🎓 Você: ")
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("👋 Até logo!")
            break

        resposta = gerar_resposta(pergunta)
        print(f"🤖 Tutor: {resposta}\n")

if __name__ == "__main__":
    main()
