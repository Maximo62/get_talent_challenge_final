import cohere
import os

class EmbeddingService:
    def __init__(self, api_key=None, model="embed-multilingual-v3.0"):
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("Se requiere la API Key de Cohere. Configúrala en COHERE_API_KEY o pásala directamente.")
        self.client = cohere.ClientV2(self.api_key)
        self.model = model

    def generate_embeddings(self, textos):
        response = self.client.embed(
            texts=textos,
            model="embed-multilingual-light-v3.0",
            input_type="search_document",
            embedding_types=["float"],
        )
        return response.embeddings.float_