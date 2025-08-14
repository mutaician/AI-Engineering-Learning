import os
import sys
from typing import List

import chromadb
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()


# Reuse the same DB path and collection used in 04-vector-db-ingest.py
DB_PATH = "./outputs/research.db"
COLLECTION_NAME = "publications"


def get_collection() -> chromadb.Collection:
	client = chromadb.PersistentClient(DB_PATH)
	# Safe if it already exists; creates otherwise
	return client.get_or_create_collection(
		name=COLLECTION_NAME,
		configuration={"hnsw": {"space": "cosine"}},
	)


def get_embedder() -> OpenAIEmbeddings:
	# Must match the model used during ingestion
	return OpenAIEmbeddings(model="text-embedding-3-small")


def retrieve(query: str, top_k: int = 5, threshold: float = 0.6) -> List[str]:
	"""Return the most relevant chunks below a cosine-distance threshold."""
	collection = get_collection()
	embedder = get_embedder()

	q_emb = embedder.embed_query(query)
	results = collection.query(
		query_embeddings=[q_emb],
		n_results=top_k,
		include=["documents", "distances"],
	)

	docs: List[str] = []
	if not results:
		return docs
	documents_field = results.get("documents")
	distances_field = results.get("distances")
	if not documents_field or not isinstance(documents_field, list) or not documents_field:
		return docs
	docs_raw = documents_field[0] or []
	dists = (distances_field[0] if distances_field and isinstance(distances_field, list) and distances_field else [])

	if dists:
		for doc, dist in zip(docs_raw, dists):
			try:
				if dist < threshold:
					docs.append(doc)
			except Exception:
				continue
		# Fallback: if nothing passed the threshold but we have results, return top_k unfiltered
		if not docs and docs_raw:
			docs.extend(docs_raw[:top_k])
	else:
		# If distances weren't returned, just take top_k docs
		docs.extend(docs_raw[:top_k])
	return docs


def answer_with_context(query: str, context_chunks: List[str]) -> str:
	"""Answer using ChatGroq, grounded in retrieved chunks."""
	context_text = "\n\n---\n\n".join(context_chunks) if context_chunks else "(no relevant context found)"

	system = SystemMessage(
		content=(
			"You are a helpful research assistant. Answer only using the provided context.\n"
			"- If the answer isn't in the context, say you don't know.\n"
			"- Be concise and cite snippets with short quotes when helpful.\n\n"
			f"Context:\n{context_text}\n\n"
		)
	)
	human = HumanMessage(content=query)

	llm = ChatGroq(
		model="llama-3.1-8b-instant",
		temperature=0.2,
		api_key=os.getenv("GROQ_API_KEY"),  # type: ignore
	)

	resp = llm.invoke([system, human])
	content = resp.content
	if isinstance(content, str):
		return content
	# Some providers return list-of-parts; join any text parts
	try:
		parts = []
		for p in content:  # type: ignore[assignment]
			if isinstance(p, str):
				parts.append(p)
			elif isinstance(p, dict) and "text" in p:
				parts.append(str(p.get("text", "")))
		return "".join(parts) if parts else str(content)
	except Exception:
		return str(content)


def rag_qa(query: str, top_k: int = 5, threshold: float = 0.6) -> str:
	chunks = retrieve(query, top_k=top_k, threshold=threshold)
	return answer_with_context(query, chunks)


def main():
	# CLI mode: allow quick one-shot usage via argv
	if len(sys.argv) > 1:
		query = " ".join(sys.argv[1:]).strip()
		print(rag_qa(query))
		return

	# Interactive mode
	print("RAG QA over publications (type 'exit' to quit)")
	try:
		top_k = int(os.getenv("RAG_TOP_K", "5"))
		threshold = float(os.getenv("RAG_THRESHOLD", "0.3"))
	except ValueError:
		top_k, threshold = 5, 0.3

	while True:
		q = input("Question: ").strip()
		if q.lower() in {"exit", "quit"}:
			break
		if not q:
			continue
		print()
		print(rag_qa(q, top_k=top_k, threshold=threshold))
		print()


if __name__ == "__main__":
	main()

