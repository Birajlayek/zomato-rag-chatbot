import gradio as gr
from src.rag.chatbot import RestaurantChatbot
from src.processing.data_processor import DataProcessor

def init_system():
    processor = DataProcessor()
    vector_db = processor.process()
    return RestaurantChatbot(vector_db)

chatbot = init_system()

def respond(message, history):
    response = chatbot.query(message)
    sources = "\n".join(response["sources"]) if response["sources"] else "No sources"
    return f"{response['answer']}\n\nSources:\n{sources}"

gr.ChatInterface(
    respond,
    title="Zomato Restaurant Assistant",
    description="Ask about menus, prices, dietary options, and compare restaurants!"
).launch()
