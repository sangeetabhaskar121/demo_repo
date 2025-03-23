from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from models import Document
from pdfminer.high_level import extract_text
import json
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer

# ✅ Load environment variables
load_dotenv()

router = APIRouter()

# ✅ Use a local embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def extract_text_from_file(file: UploadFile):
    """Extract text from .txt or .pdf file"""
    if file.filename.endswith(".txt"):
        content = file.file.read().decode("utf-8")
    elif file.filename.endswith(".pdf"):
        content = extract_text(file.file)
    else:
        raise ValueError("Unsupported file format. Please upload a .txt or .pdf file.")
    
    return content

def generate_local_embedding(text):
    """
    Uses SentenceTransformers to generate embeddings for the given text.
    """
    return embedding_model.encode(text).tolist()  # Convert numpy array to list

@router.post("/upload/")
async def upload_document(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        text_content = extract_text_from_file(file)

        # ✅ Generate Embeddings using sentence-transformers
        embedding_vector = generate_local_embedding(text_content)
        embedding_json = json.dumps(embedding_vector)

        # ✅ Store in DB
        new_doc = Document(name=file.filename, content=text_content, embedding=embedding_json)
        db.add(new_doc)
        await db.commit()
        
        return {"message": "Document uploaded successfully"}
    
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
