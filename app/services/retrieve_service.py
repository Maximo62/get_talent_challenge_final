import logging

logger = logging.getLogger(__name__)

class RetrieveService:
    def __init__(self, persistence_service, embedding_service, similarity_metric="cosine"):
        """
        Inicializa el servicio de recuperación.

        Args:
            persistence_service (PersistenceService): Instancia del servicio de persistencia.
            embedding_service (EmbeddingService): Instancia del servicio de embeddings.
            similarity_metric (str): Métrica de similaridad a usar ("cosine" o "euclidean").
        """
        self.persistence_service = persistence_service
        self.embedding_service = embedding_service
        self.similarity_metric = similarity_metric

    def retrieve_similar_documents(self, query, collection_name, top_k=2):
        """
        Recupera los documentos más similares a la consulta proporcionada.

        Args:
            query (str): Pregunta del usuario.
            collection_name (str): Nombre de la colección a consultar.
            top_k (int): Número de documentos más similares a recuperar.

        Returns:
            list[dict]: Lista de documentos relevantes con sus metadatas, IDs y puntuaciones.
        """
        try:
            # Generar embedding de la consulta
            query_embedding = self.embedding_service.generate_embeddings([query])[0]

            # Obtener la colección de ChromaDB
            collection = self.persistence_service.get_or_create_collection(collection_name)
            if not collection:
                raise ValueError(f"La colección '{collection_name}' no existe.")

            # Realizar la consulta en la colección
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )

            # Imprimir los resultados para depuración
            logger.debug(f"Resultados de la consulta: {results}")

            # Verificar que se hayan encontrado resultados
            if not results.get("ids") or not results.get("documents"):
                logger.warning("No se encontraron documentos relevantes.")
                return []

            # Construir la lista de documentos relevantes
            documents = []
            ids = results.get("ids", [])
            documents_data = results.get("documents", [])
            distances = results.get("distances", [])

            # Asegurarse de que hay resultados para procesar
            if len(ids) == 0 or len(documents_data) == 0:
                logger.warning("No se encontraron documentos relevantes.")
                return []

            for i in range(min(len(ids[0]), len(documents_data[0]))): 
                documents.append({
                    "id": ids[0][i],
                    "text": documents_data[0][i],
                    "metadata": results.get("metadatas", [None])[i] if len(results.get("metadatas", [])) > i else None,
                    "score": 1 - distances[0][i] if self.similarity_metric == "cosine" else distances[0][i],
                })

            return documents

        except Exception as e:
            logger.error(f"Error al recuperar documentos: {str(e)}")
            return []