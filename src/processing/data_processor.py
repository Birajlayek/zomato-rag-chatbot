from pathlib import Path
import json
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DataProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2", model_kwargs={"device": "cpu"})

    def process(self):
        docs = []
        for path in Path('data/raw').glob('*.json'):
            with open(path) as f:
                data = json.load(f)
                text = self._format_doc(data)
                docs.extend(self.text_splitter.split_text(text))
        if not docs:
            raise ValueError("No documents found. Please run the scraper first.")
        return Chroma.from_texts(docs, self.embeddings, persist_directory="data/chroma_db")

    def _format_doc(self, data):
        menu = "\n".join([f"- {item['name']} ({item['price']}): {item['description']}" for item in data.get('menu', [])])
        features = ", ".join([f"{k}: {v}" for k, v in data.get('features', {}).items()])
        return f"""
Restaurant: {data.get('name', '')}
Location: {data.get('location', {}).get('address', '')}
Menu:
{menu}
Features: {features}
Hours: {data.get('hours', '')}
Contact: {data.get('contact', {}).get('phone', '')}
"""
