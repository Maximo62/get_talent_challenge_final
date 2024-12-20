import cohere
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class ResponseService:
    def __init__(self, cohere_api_key: str):
        """
        Inicializa el servicio de respuesta con la API de Cohere.
        
        :param cohere_api_key: Clave API para autenticar con Cohere.
        """
        self.api_key = cohere_api_key
        self.client = cohere.ClientV2(self.api_key)  # Inicializa el cliente de Cohere

    async def generate_response(self, context, question):
        """
        Genera una respuesta utilizando el modelo de Cohere.
        
        :param context: Contexto inicial del sistema.
        :param question: Pregunta proporcionada por el usuario.
        :return: Respuesta generada por el modelo.
        """
        try:
            # Llamar a la función que genera la respuesta utilizando Cohere
            respuesta = respuesta_al_usuario(self, context, question)
            return respuesta

        except Exception as e:
            # Manejar errores de la API
            logger.error(f"Error al generar la respuesta: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al generar la respuesta.")

def respuesta_al_usuario(self, historia, pregunta):
    prompt_principal = f"""
        Responde basándote únicamente en la información del contexto proporcionado. No inventes ni asumas información que no esté allí.

        ###
        Instrucciones:
        - Usa el contexto como base de tu respuesta.
        - Nunca uses emojis en tus respuesas.

        ###
        Contexto:
        {historia}

        ###
        Pregunta:
        {pregunta}

        ###
        Respuesta:
    """

    system_prompt = "Responde siempre utilizando el contexto como fuente única de información."

    response1 = self.client.chat(
        model="command-r-plus-04-2024",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_principal}
        ],
        temperature=0,
        seed=1212
    )
    respuesta_inicial = response1.message.content[0].text

    prompt_idioma = f""" 
        ###
        Instrucciones:
        1- Asegúrate de que el siguiente texto esté en español. Si no lo está, tradúcelo.
        Texto: {respuesta_inicial}

        Recuerda, tu respuesta debe ser solamente la traducción, sin incluir el idioma identificado.
    """

    response2 = self.client.chat(
        model="c4ai-aya-expanse-32b",
        messages=[
            {"role": "user", "content": prompt_idioma}
        ],
    )

    respuesta_al_usuario = response2.message.content[0].text
    return respuesta_al_usuario