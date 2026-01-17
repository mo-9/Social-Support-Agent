from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.core.config import settings

# 1. إعداد نموذج الـ Embeddings (بيحول النص لأرقام)
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

# 2. إعداد الاتصال بـ Qdrant
client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
COLLECTION_NAME = "social_laws"

def get_vector_store():
    # لو الـ Collection مش موجودة، نعملها
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )
    return vector_store

def index_text(text: str, source: str):
    print(f"💾 Indexing document from: {source}")
    vector_store = get_vector_store()
    
    # تقسيم النص لفقرات
    chunks = [t.strip() for t in text.split("\n\n") if t.strip()]
    metadatas = [{"source": source} for _ in chunks]
    
    # الحفظ
    vector_store.add_texts(texts=chunks, metadatas=metadatas)
    print(f"✅ Indexed {len(chunks)} chunks into Qdrant.")

def search_laws(query: str, k: int = 3):
    print(f"🔍 Searching laws for: {query}")
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return results