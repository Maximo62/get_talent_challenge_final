# Sistema de Recuperación de Respuestas Guiado por Datos (RAG)

Este sistema utiliza un enfoque de Recuperación de Respuestas Guiado por Datos (RAG) para responder preguntas formuladas por los usuarios. Permite buscar en una colección indexada y generar respuestas basadas en documentos relacionados.

## Endpoints
### `/query`
- **POST**: Realizar una consulta RAG
  - Este endpoint permite realizar una consulta en el sistema RAG (Recuperación de Respuestas). El cliente envía una pregunta, y el sistema devuelve una respuesta junto con documentos relacionados.
