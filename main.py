# from fastapi import FastAPI
# from document_ingestion import router as ingest_router
# from .qa_api import router as qa_router
# app = FastAPI()

# app.include_router(ingest_router, prefix="/documents")
# app.include_router(qa_router, prefix="/qna")

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to Document Management and RAG-based Q&A API"}
from fastapi import FastAPI
from document_ingestion import router as ingest_router
from qa_api import router as qa_router

app = FastAPI()

app.include_router(ingest_router, prefix="/documents")
app.include_router(qa_router, prefix="/qna")

@app.get("/")
def read_root():
    return {"message": "Welcome to Document Management and RAG-based Q&A API"}
