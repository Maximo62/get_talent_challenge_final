from langchain_text_splitters import RecursiveCharacterTextSplitter

def consumir_archivo(full_text, chunk_size=2100, overlap_ratio=0.2):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=int(chunk_size * overlap_ratio),
        length_function=len,
    )

    # Dividir el texto en chunks
    chunks = text_splitter.split_text(full_text.strip())
    return chunks