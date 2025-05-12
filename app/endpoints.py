from fastapi import APIRouter, HTTPException
from app.rag import RAGSystem

rag = RAGSystem()

router = APIRouter()

@router.get('/query')
async def query_rag_system(query:str):
    try:
        response = await rag.get_rag_response(query)
        return {'query': query, 'response': response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
