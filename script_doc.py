# SCRIPT PARA GENERAR DOCUMENTACIÓN DE FORMA AUTOMATICA
import requests
from markdownify import markdownify

def save_openapi_to_markdown(api_url: str, output_file: str):
    """
    Descarga el esquema OpenAPI y lo guarda como Markdown.
    """
    response = requests.get(f"{api_url}/openapi.json")
    response.raise_for_status()

    openapi_schema = response.json()
    title = openapi_schema.get("info", {}).get("title", "API Documentation")
    description = openapi_schema.get("info", {}).get("description", "No description provided.")
    paths = openapi_schema.get("paths", {})

    # Construir Markdown
    md_content = f"# {title}\n\n{description}\n\n## Endpoints\n"
    for path, methods in paths.items():
        md_content += f"### `{path}`\n"
        for method, details in methods.items():
            summary = details.get("summary", "No summary")
            md_content += f"- **{method.upper()}**: {summary}\n"
            if "description" in details:
                md_content += f"  - {details['description']}\n"

    # Guardar en archivo
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Documentación exportada a: {output_file}")

# URL de tu API
api_url = "http://127.0.0.1:8000"  # Cambia esto si tu API está en otro lugar
output_file = "api_documentation.md"

save_openapi_to_markdown(api_url, output_file)
