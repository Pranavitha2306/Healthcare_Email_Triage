import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from openai import  OpenAI
from rag_ingestion import load_documents, chunk_text, generate_embeddings, model


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI-API_KEY"))

pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

index_name = "healthcare-rag"
if not pc.has_index(index_name):
    pc.create_index(
        name = index_name,
        dimension = 384,
        metric = "cosine",
        spec = ServerlessSpec(
            cloud = "aws",
            region = "us-east-1"
        )
    )

index = pc.Index(index_name)

def upload_knowledge():
    documents = load_documents()
    for document in documents:
        print(document["category"], ":", document["source"])
    total_uploaded = 0

    for document in documents:
        text_chunks = chunk_text(document["text"])

        print("Processing:", document["source"])

        for start in range(0, len(text_chunks), 100):
            batch_chunks = text_chunks[start:start+100]
            embeddings = generate_embeddings(batch_chunks)

            vectors = []

            for i, (chunk, embedding) in enumerate(zip(batch_chunks, embeddings), start=start):
                vectors.append({
                    "id": f"{document['source']}-{start + i}",
                    "values": embedding.tolist(),
                    "metadata": {"text":chunk,
                                 "source": document["source"],
                                 "category" : document["category"]
                                     }
                })

            index.upsert(vectors=vectors)
            total_uploaded += len(vectors)
            print("Uploaded:", total_uploaded)

    print("Total vectors uploaded:", total_uploaded)

def retrieve_context(query):
    query_embedding = model.encode(query)

    results = index.query(
        vector = query_embedding.tolist(),
        top_k=20,
        include_metadata = True
)

    for match in results["matches"]:
        print("Similarity score:", match["score"])
        print("Source:", match["metadata"].get("source", "Unknown"))

    similarity_threshold = 0.40

    relevant_matches = [
        match for match in results["matches"]
        if match["score"] >= similarity_threshold
    ]

    if not relevant_matches:
        retrieved_context = "no relevant information found in the knowledge base."
    else:
        retrieved_context = "\n\n".join(
            f"source: {match['metadata'].get('source', 'Unknown')}\n"
            f"Content: {match['metadata']['text']}"
            for match in relevant_matches
        )
    return retrieved_context

if __name__ == "__main__":
    upload_knowledge()
