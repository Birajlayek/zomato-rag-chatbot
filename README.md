Zomato Gen AI RAG Chatbot - Quick Start

How it works:
-------------
- Scrapes restaurant data (menu, prices, features, etc.) from real websites.
- Builds a searchable knowledge base.
- Uses a chatbot (with free Hugging Face models) to answer your questions using that data.

How to run:
-----------
1. Clone repo & install:
   git clone <your-repo-url>
   cd zomato_rag
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Scrape data:
   Edit src/scrape_restaurants.py with URLs, then:
   python src/scrape_restaurants.py

3. Build knowledge base:
   python -c "from src.processing.data_processor import DataProcessor; DataProcessor().process()"

4. Start chatbot:
   python -m src.interface.app
   (Open the shown URL in your browser)

Example questions:
------------------
- Which restaurant has gluten-free options?
- Compare vegetarian options at Restaurant A and B.

Note:
-----
- The bot answers only from the data you scraped and processed.
- All code and models are free/open-source.

