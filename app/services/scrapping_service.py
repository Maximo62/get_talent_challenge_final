from app.models.model_documento import DocumentModel
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
import os
import uuid

class ScrapingService:
    @staticmethod
    def scrap_data():
        url = 'https://www.argentina.gob.ar/informes-provinciales/caracterizacion-productiva'
        url_limpia = 'https://www.argentina.gob.ar/'

        respuesta = requests.get(url)

        if respuesta.status_code == 200:
            print("Conexión exitosa")
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            document_models = []
            total_caracteres = 0

            provincias_interes = ['córdoba', 'santa fe']
            # provincias_interes = ['buenos aires', 'formosa']

            # Buscar todas las filas de la tabla
            for tr in soup.find_all('tr'):
                provincia_td = tr.find('td', {'data-label': ' Provincia'})
                informe_td = tr.find('td', {'data-label': 'Informe '})

                # Verificar si es una fila de interés
                if provincia_td and informe_td and provincia_td.text.strip().lower() in provincias_interes:
                    # Extraer datos
                    nombre = provincia_td.text.strip()
                    fecha = tr.find('td', {'data-label': 'Última actualización'}).text.strip()
                    url = informe_td.find('a')['href']
                    if url.startswith('blank:#/'):
                        url = url.replace('blank:#/', '')
                    
                    # Manejar enlaces relativos
                    pdf_url = url if url.startswith('http') else url_limpia + url.lstrip('/')
                    print(f"Descargando: {pdf_url} para la provincia {nombre}")

                    # Descargar el PDF
                    response_pdf = requests.get(pdf_url)

                    if response_pdf.status_code == 200:
                        temp_pdf_path = f"temp_{nombre.replace(' ', '_')}.pdf"

                        # Guardar el archivo temporalmente
                        with open(temp_pdf_path, 'wb') as f:
                            f.write(response_pdf.content)

                        # Extraer texto del PDF
                        pdf_text = ""
                        try:
                            reader = PdfReader(temp_pdf_path)
                            for page in reader.pages:
                                pdf_text += page.extract_text()
                        except Exception as e:
                            print(f"Error al procesar el PDF de {nombre}: {e}")
                            pdf_text = "Error al extraer texto"

                        # Contar caracteres del texto extraído
                        total_caracteres += len(pdf_text.strip())

                        # Eliminar el archivo temporal
                        os.remove(temp_pdf_path)
                    else:
                        print(f"Error al descargar el informe {nombre}")
                        pdf_text = "Error al descargar el PDF"

                    # Crear el modelo de documento
                    document_model = DocumentModel(
                        text=pdf_text.strip(),
                        metadata={"name": nombre, "date": fecha, "url": pdf_url},
                        id=str(uuid.uuid4())  # Generar un ID único
                    )

                    document_models.append(document_model)

            if not document_models:
                print("No se encontraron informes para las provincias seleccionadas.")
                return []
            
            print(f"Total de documentos procesados: {len(document_models)}")
            print(f"Total de caracteres extraídos: {total_caracteres}")
            return document_models
        else:
            print('Hubo un error al obtener los informes')
            return []
