import os, asyncio, chromadb
from pprint import pprint

data_path = "storage/chatbot_info"
chroma_path = "./chroma_db"

chroma_client = chromadb.PersistentClient(path=chroma_path)
collection = chroma_client.get_or_create_collection(name="information")

file_paths = []
documents = []
ids = []
id = 0

for file_name in os.listdir(data_path):
    if file_name.endswith(".txt"):
        file_paths.append(file_name)

        file_path = os.path.join(data_path, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            #idfk, i think it loops through the text, hopefully it does.
            sentences = text.split("\n")
            
            for sentence in sentences:
                if sentence.startswith("--comment--"):
                    print("skipped a comment")
                    continue
                documents.append(sentence.strip())
                ids.append("ID" + str(id))
                id += 1
print(f"found files: {" | ".join(file_paths)}\n amount: {len(file_paths)}")

collection.upsert(documents=documents, ids=ids)
print("success")
def query(question):
    results = collection.query(
    query_texts=[question],
    n_results=3
)
    return results["documents"][0]
