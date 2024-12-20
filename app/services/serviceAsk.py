from app.services.persistence_service import PersistenceService
from app.services.embedding_service import EmbeddingService
from app.services.scrapping_service import ScrapingService
from app.services.retrieve_service import RetrieveService
from app.services.response_service import ResponseService

class ServiceInitializer:
    def __init__(self, cohere_api_key, openai_api_key, persistence_dir, collection_name):
        """
        Inicializa todos los servicios necesarios para la aplicación.
        """
        # Configuración del directorio de persistencia de ChromaDB
        self.persistence_dir = persistence_dir
        
        # Configuración de la API Key para Cohere
        self.cohere_api_key = cohere_api_key
        self.openai_api_key = openai_api_key

        self.collection_name = collection_name
        # Inicializar servicios
        self.persistence_service = self._initialize_persistence_service()
        self.embedding_service = self._initialize_embedding_service()
        self.scraping_service = self._initialize_scraping_service()
        self.retrieve_service = self._initialize_retrieve_service()
        self.response_service = self._initialize_response_service()

    def _initialize_persistence_service(self):
        """
        Inicializa el servicio de persistencia (ChromaDB).
        """
        print("Inicializando el servicio de persistencia (ChromaDB)...")
        return PersistenceService(persist_directory=self.persistence_dir, collection_name=self.collection_name)

    def _initialize_embedding_service(self):
        """
        Inicializa el servicio de embeddings con Cohere.
        """
        print("Inicializando el servicio de Embeddings (Cohere)...")
        return EmbeddingService(api_key=self.cohere_api_key)
    
    def _initialize_scraping_service(self):
        """
        Inicializa el servicio de scraping.
        """
        print("Inicializando el servicio de Scraping...")
        return ScrapingService()

    def _initialize_retrieve_service(self):
        """
        Inicializa el servicio de retrieve.
        """
        print("Inicializando el servicio de Retrieve...")
        return RetrieveService(self.persistence_service, self.embedding_service)
    
    def _initialize_response_service(self):
        """
        Inicializa el servicio de response.
        """
        print("Inicializando el servicio de Response...")
        return ResponseService(self.cohere_api_key)

    def get_services(self):
        """
        Retorna todos los servicios inicializados.
        :return: Diccionario con servicios.
        """
        return {
            "persistence_service": self.persistence_service,
            "embedding_service": self.embedding_service,
            "scraping_service": self.scraping_service,
            "retrieve_service": self.retrieve_service,
            "response_service": self.response_service,
        }
