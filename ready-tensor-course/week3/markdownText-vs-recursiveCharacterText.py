from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownTextSplitter


PUBLICATION_PATH = "data/publication.md"

text = open(PUBLICATION_PATH).read()

rc_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
md_splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=50)

rc_chunks = rc_splitter.split_text(text)
md_chunks = md_splitter.split_text(text)

print("RecursiveCharacterTextSplitter:", len(rc_chunks), "chunks")
print("MarkdownTextSplitter:", len(md_chunks), "chunks")

print("RC Example:", rc_chunks[0])
print("=="*40)
print("MD Example:", md_chunks[0])

# Seems their is no difference between MarkdownTextSplitter and REcursiveCharacterTextSplitter