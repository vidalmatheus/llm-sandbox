import os
import sys
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

loader = TextLoader('data.txt')
index = VectorstoreIndexCreator().from_loaders([loader])

query = sys.argv[1]
print(index.query(query, llm=llm))
