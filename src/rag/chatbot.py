from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate

class RestaurantChatbot:
    def __init__(self, vector_db):
        # Prompt designed for detailed, source-attributed answers
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "You are a helpful restaurant assistant. "
                "Using ONLY the context below, answer the user's question in detail. "
                "If the answer is not in the context, say you don't know. "
                "At the end, list all restaurant names or sources you used in a section 'Sources:'.\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}\n\n"
                "Answer:"
            )
        )

        # Use google/flan-t5-large (or flan-t5-small/base if needed)
        self.llm = HuggingFacePipeline.from_model_id(
            model_id="google/flan-t5-large",
            task="text2text-generation",
            model_kwargs={"temperature": 0.3, "max_length": 512},
            pipeline_kwargs={"max_new_tokens": 512}
        )

        # Retrieve more chunks for better context
        self.retriever = vector_db.as_retriever(search_kwargs={"k": 7})

        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )

    def query(self, question):
        # Print retrieved context for debugging
        retrieved_docs = self.retriever.get_relevant_documents(question)
        print("\n--- Retrieved Context for Debugging ---")
        for i, doc in enumerate(retrieved_docs):
            print(f"Chunk {i+1}:\n{doc.page_content[:500]}\n")
        print("--- End of Retrieved Context ---\n")

        # Generate answer
        try:
            result = self.qa.invoke({"query": question})
        except AttributeError:
            result = self.qa({"query": question})

        answer = result["result"]
        sources = set()
        for doc in result.get("source_documents", []):
            src = doc.metadata.get("source", doc.metadata.get("name", "Unknown"))
            sources.add(src)
        return {
            "answer": answer,
            "sources": list(sources) if sources else ["No sources found"]
        }
