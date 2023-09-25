from sentence_transformers import SentenceTransformer


def vectorize(data: list[str]):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(data)
    return embeddings

