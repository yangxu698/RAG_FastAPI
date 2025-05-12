#%%
from dotenv import load_dotenv
import os
# import faiss

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.prompts import PromptTemplate
# from langchain_openai import OpenAIEmbeddings
# from langchain.chains import RetrievalQA
# from langchain.chains import LLMChain

#%%
# Load environment variables from .env file
load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize LLM agent
# llm = ChatOpenAI(openai_api_key=openai_api_key) # temperature=0.0)
llm = ChatGoogleGenerativeAI(
    openai_api_key=google_api_key,
    temperature=0.0,
    model="gemini-2.0-flash",
    max_tokens=1000
)

#%%
# Set up Class for RAG system

class RAGSystem:
    def __init__(self):
        self.retriever = None

    def setup_rag_retriever(self):
        # Create embeddings
        # embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        # openai_api_key=google_api_key,
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-exp-03-07",
            # max_tokens=1000
        )

        # Create vector store
        if 'faiss_index' in os.listdir():
            vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

        else:
            # Load documents
            loader = TextLoader("data/lakes.txt")
            documents = loader.load()

            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=8000, chunk_overlap=200)
            texts_chunks = text_splitter.split_documents(documents)

            vector_store = FAISS.from_documents(texts_chunks, embeddings)
            vector_store.save_local("faiss_index")
        

        # Set up retriever
        self.retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 1}
            )
    
    async def get_rag_response(self, query:str):
        if self.retriever is None:
            self.setup_rag_retriever()

        retrieved_docs = self.retriever.invoke(query)
        
        context = "\n".join([doc.page_content for doc in retrieved_docs])

        prompt_template = PromptTemplate.from_template(
            "Use the following context to answer the question: {ctt}\n\nQuestion: {q}\nAnswer:"
        )

        prompt = prompt_template.invoke(
            {'ctt':context,
            'q':query
            }
        )
        # input_variables=["context", "query"],
        # print(prompt)

        generated_response = llm.invoke(prompt)

        return generated_response
