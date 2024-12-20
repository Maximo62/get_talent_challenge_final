from dotenv import load_dotenv
import os

# Construir una ruta absoluta a ".env" basado en la ubicación del archivo actual
base_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio del script actual
env_path = os.path.join(base_dir, "..", ".env")  # Ajustar según la ubicación de .env
load_dotenv(env_path)

#load_dotenv("app/.env")

api_key = os.getenv("COHERE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
persistence_dir = os.getenv("PERSISTENCE_DIR")
collection_name = os.getenv("COLLECTION_NAME")

def get_env_vars():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio del archivo actual
    dinamic_persistence_dir = os.path.abspath(os.path.join(base_dir, "../chroma_persistence"))  # Ruta absoluta normalizada

    return {
        "api_key": api_key,
        "openai_api_key": openai_api_key,
        "dinamic_persistence_dir": persistence_dir,
        "absolute_persistence_dir": dinamic_persistence_dir,  # Ruta completamente normalizada
        "collection_name": collection_name
    }
