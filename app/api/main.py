from fastapi import FastAPI, UploadFile, File
import httpx


app = FastAPI()
OLLAMA_URL = "http://ollama:11434/api/generate"

@app.post("/presentar")
async def presentar(nombre: str):
    # 1. Buscar en RAG
    from rag.embeddings import process_documents
    vector_db = process_documents()
    context = vector_db.similarity_search(nombre, k=3)
    
    # 2. Consultar a Ollama
    prompt = f"""
    Genera una presentación profesional sobre {nombre} usando este contexto:
    {context}
    """
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            OLLAMA_URL,
            json={"model": "deepseek-r1:14b", "prompt": prompt, "stream": False}
        )
    
    return {"presentacion": response.json()["response"]}


@app.post("/upload")
async def upload_persona(file: UploadFile = File(...)):
    # Guardar el archivo subido
    file_path = f"app/rag/data/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Reprocesar RAG
    process_documents()
    
    return {"status": f"Archivo {file.filename} procesado"}