import chromadb
import os


class PersistenceService:
    def __init__(self, persist_directory="../chroma_persistence", collection_name="rag_documentos"):
        absolute_persist_directory = os.path.abspath(persist_directory)
        print(f"Intentando crear el directorio de persistencia en: {absolute_persist_directory}")
        try:
            os.makedirs(absolute_persist_directory, exist_ok=True)
            print(f"Directorio de persistencia creado o ya existente: {absolute_persist_directory}")
        except OSError as e:
            print(f"Error al crear el directorio de persistencia: {e}")
            raise RuntimeError(f"No se pudo crear el directorio de persistencia: {e}")

        self.client = chromadb.PersistentClient(path=absolute_persist_directory)
        self.persist_directory = absolute_persist_directory
        self._collection = self.get_or_create_collection(collection_name)
        print(f"Servicio de persistencia inicializado en: {self.persist_directory}")

    def get_or_create_collection(self, nombre):
        all_collections = self.client.list_collections()
        
        # Verificar si la colección ya existe
        for col in all_collections:
            if col.name == nombre:
                print(f"Colección '{nombre}' encontrada. Devolviendo la instancia existente.")
                return self.client.get_collection(name=nombre)

        # Si no existe, crear una nueva colección
        print(f"Colección '{nombre}' no encontrada. Creando una nueva colección.")
        return self.client.create_collection(name=nombre)
