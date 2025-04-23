"""Script de consulta interactiva con OpenAI mediante prompt_toolkit y dotenv."""

import openai 
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from dotenv import load_dotenv
import os

# Cargar variables desde el archivo .env
load_dotenv()

# Configurar la API key
openai.api_key = os.getenv("OPENAI_API_KEY")


session = PromptSession(history=InMemoryHistory())

print("Asistente interactivo con ChatGPT. Escribe tu consulta o deja en blanco para salir.\n")

try:
    messages = []

    while True:
        user_input = session.prompt("Tú: ")

        if user_input.strip() == "":
            print("Saliendo. ¡Hasta luego!")
            break

        messages.append({"role": "user", "content": user_input})

        print("Procesando respuesta...\n")

        response = openai.ChatCompletion.create(
            model="gpt-4.1",  
            messages=messages
        )

        reply = response['choices'][0]['message']['content']
        print(f"ChatGPT: {reply}\n")

        messages.append({"role": "assistant", "content": reply})

except KeyboardInterrupt:
    print("\nInterrumpido por el usuario.")
except Exception as e:
    print(f"Ocurrió un error: {e}")