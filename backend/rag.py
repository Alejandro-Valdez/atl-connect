import json
import chromadb
from chromadb.utils import embedding_functions

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
COLLECTION_NAME = "atl_resources"


def get_collection():
    return chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )


def load_resources_into_db(json_path="../data/resources.json"):
    """Load resource data from JSON into ChromaDB. Run once via seed_db.py."""
    with open(json_path, "r") as f:
        resources = json.load(f)

    collection = get_collection()
    documents, metadatas, ids = [], [], []

    for r in resources:
        doc = (
            f"{r['name']}. {r['description']}. "
            f"Categories: {', '.join(r['category'])}. "
            f"Services: {r['services']}. "
            f"Location: {r['address']}. "
            f"Eligibility: {r['eligibility']}."
        )
        documents.append(doc)
        metadatas.append({
            "name": r["name"],
            "category": ", ".join(r["category"]),
            "address": r["address"],
            "phone": r.get("phone", "N/A"),
            "hours": r.get("hours", "N/A"),
            "services": r.get("services", ""),
            "eligibility": r.get("eligibility", "Open to all"),
            "description": r["description"],
            "transit_access": r.get("transit_access", "N/A"),
            "lat": str(r.get("lat", "")),
            "lng": str(r.get("lng", "")),
        })
        ids.append(r["id"])

    collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
    print(f"Loaded {len(resources)} resources into ChromaDB.")


def get_relevant_resources(query, n_results=5):
    """Query ChromaDB for resources relevant to the user's message."""
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=n_results)
    resources = []
    if results and results["metadatas"]:
        for metadata in results["metadatas"][0]:
            resources.append(metadata)
    return resources


def get_all_resources():
    """Return all resources from the database."""
    collection = get_collection()
    results = collection.get()
    return results["metadatas"] if results["metadatas"] else []
