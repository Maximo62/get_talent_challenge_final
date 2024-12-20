class DocumentModel:
    def __init__(self, text, metadata, id, embeddings=None):
        self.text = text
        self.metadata = metadata
        self.id = id
        self.embeddings = embeddings

    def to_dict(self):
        return {
            "text": self.text,
            "metadata": self.metadata,
            "id": self.id,
            "embeddings": self.embeddings
        }