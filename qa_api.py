from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db import get_db
from models import Document
import os
import time
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ✅ Load environment variables
from dotenv import load_dotenv
load_dotenv()

# ✅ Ensure router exists
router = APIRouter()

# ✅ Get Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Missing Groq API Key! Please set GROQ_API_KEY in .env")

# ✅ Set up embeddings (local Ollama model)
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

# ✅ Set up vector database (Chroma)
vectorstore = Chroma(
    collection_name="ollama_embeds",
    embedding_function=embedding_model
)
retriever = vectorstore.as_retriever()

# ✅ Set up LLM (Groq)
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="mixtral-8x7b-32768"  # ✅ Ensure model exists
)

# ✅ Define the RAG prompt template
rag_template = """Answer the question based only on the following context:
{context}
Question: {question}
"""
rag_prompt = ChatPromptTemplate.from_template(rag_template)

# ✅ Define the RAG chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

@router.get("/qa/")
async def answer_question(question: str = Query(...), db: AsyncSession = Depends(get_db)):
    """Fetch relevant document context & generate an answer using Groq"""
    start_time = time.time()

    async with db as session:
        result = await session.execute(select(Document))
        documents = result.scalars().all()

    if not documents:
        return {"error": "No documents found"}

    # ✅ Store document content in vector database
    document_texts = [doc.content for doc in documents]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.create_documents(document_texts)

    vectorstore.add_documents(chunks)  # ✅ Add to Chroma

    # ✅ Invoke the RAG chain
    response = rag_chain.invoke(question)

    # ✅ Measure response time
    end_time = time.time()
    response_time = f"Response time: {end_time - start_time:.2f} seconds."

    return {
        "question": question,
        "answer": response,
        "response_time": response_time
    }
