from app.utils.get_env_vars import get_env_vars
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class QueryRequest(BaseModel):
    question: str = Field(..., examples=["En Córdoba, ¿cuántos hectareas de soja se sembraron en 2017?"])

class QueryResponse(BaseModel):
    answer: str = Field(..., examples=["En 2017, la superficie cultivada con soja en la provincia de Córdoba fue de 4,9 millones de hectáreas."])
    documents: list = Field(..., examples=[
        {
            "id": "id1",
            "text": "Producto no elaborado en la provincia... ",
            "metadata": [
                {
                    "date": "Mayo 2018",
                    "name": "Córdoba",
                    "url": "https://www.argentina.gob.ar/sites/default/files/23_2018_cordoba.pdf"
                }
            ]
        }
    ])

@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Realizar una consulta RAG",
    description=(
        "Este endpoint permite realizar una consulta en el sistema RAG (Recuperación de Respuestas). "
        "El cliente envía una pregunta, y el sistema devuelve una respuesta junto con documentos relacionados."
    ),
    response_description="Respuesta generada basada en documentos relacionados."
)

async def query_rag(request: Request, query_request: QueryRequest):
    """
    Realiza una consulta en el sistema de Recuperación de Respuestas Guiado por Datos (RAG) y devuelve una respuesta basada en documentos relevantes.
    ...
    """
    question = query_request.question
    logger.debug(f"Received question: {question}")

    # Obtener servicios del contenedor
    retrieve_service = request.state.retrieve_service
    response_service = request.state.response_service

    try:
        logger.debug("Embedding service initialized.")
        variables = get_env_vars()
        logger.debug(f"Environment variables: {variables}")

        # Recuperar documentos similares
        results = retrieve_service.retrieve_similar_documents(question, variables["collection_name"], 3)
        if not results:
            raise ValueError("No se encontraron documentos relevantes.")

        logger.debug(f"Results from retrieval service: {results}")

        context = "\n".join(doc["text"] for doc in results)
        answer = await response_service.generate_response(context, question)
        logger.debug(f"Generated answer: {answer}")

        return QueryResponse(
            answer=answer,
            documents=results
        )

    except ValueError as ve:
        logger.error(f"ValueError: {str(ve)}")
        raise HTTPException(status_code=404, detail=str(ve))

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Ocurrió un error inesperado. Por favor, inténtelo de nuevo más tarde.")