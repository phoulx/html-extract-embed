from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams


def save(data):
    client = QdrantClient("localhost", port=6333)

    client.recreate_collection(
        collection_name="my_collection",
        vectors_config=VectorParams(size=384, distance=Distance.DOT),
    )

    points = []
    for i, (embedding, other) in enumerate(data):
        points.append(PointStruct(
            id=i+1,
            vector=embedding,
            payload=other
        ))

    operation_info = client.upsert(
        collection_name="my_collection",
        wait=True,
        points=points
    )

    return operation_info.status
