from app.services.serviceAsk import ServiceInitializer
from app.utils.generate_chunks import consumir_archivo
from app.routers import rag
from app.utils.get_env_vars import get_env_vars
from fastapi import FastAPI, Request
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener variables de entorno
variables = get_env_vars()
logger.info(f"Variables de entorno: {variables}")

# Inicialización de los servicios
service_initializer = ServiceInitializer(
    variables["api_key"],
    variables["openai_api_key"],
    variables["dinamic_persistence_dir"],
    variables["collection_name"]
)
services = service_initializer.get_services()

# Extraer servicios necesarios
scraping_service = services["scraping_service"]
embedding_service = services["embedding_service"]
persistence_service = services["persistence_service"]
retrieve_service = services["retrieve_service"]
response_service = services["response_service"]

# Obtener o crear la colección
collection = persistence_service.get_or_create_collection(variables["collection_name"])

# Si la colección está vacía, agregar documentos
if not collection.count(): 
    # Data ingestion
    documentos = scraping_service.scrap_data()

    texts = [] 
    embeddings = []
    metadatas = []
    str_ids = []
    i = 1

    for doc in documentos:
        if doc.text == "Error al descargar el PDF":
            logger.warning("Se encontró un error al descargar el PDF, omitiendo este documento.")
            continue

        # Consumir el texto en chunks
        chunks = consumir_archivo(doc.text)
        for chunk in chunks:
            chunk_id = f"id{i}"
            str_ids.append(chunk_id)
            i += 1

            # Generar embedding para cada chunk
            embed = embedding_service.generate_embeddings([chunk])[0]
            embeddings.append(embed)
            metadatas.append(doc.metadata)

            texts.append(chunk)

    # Verificar que todas las listas tengan la misma longitud
    if len(embeddings) == len(metadatas) == len(str_ids) == len(texts):
        collection.add(
            documents=texts,  
            embeddings=embeddings,
            metadatas=metadatas,
            ids=str_ids
        )

    # Fin Data Ingestion
    
else:
    logger.info(f"Usando colección existente desde caché: {variables['collection_name']}")

app = FastAPI(
    title="Sistema de Recuperación de Respuestas Guiado por Datos (RAG)",
    description=(
        "Este sistema utiliza un enfoque de Recuperación de Respuestas Guiado por Datos (RAG) para responder preguntas "
        "formuladas por los usuarios. Permite buscar en una colección indexada y generar respuestas basadas en documentos relacionados."
    ),
    version="1.0.0"
)


# Middleware para agregar servicios a la solicitud
@app.middleware("http")
async def add_services_to_request(request: Request, call_next):
    request.state.scraping_service = scraping_service
    request.state.embedding_service = embedding_service
    request.state.persistence_service = persistence_service
    request.state.retrieve_service = retrieve_service
    request.state.response_service = response_service
    response = await call_next(request)
    return response


app.include_router(
    rag.router,
    tags=["Consultas"],
    include_in_schema=True
)