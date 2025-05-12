from fastapi import FastAPI, UploadFile, File
from langchain_community.llms import Ollama
from rag.embeddings import process_documents, load_vector_db
import httpx


app = FastAPI()
OLLAMA_URL = "http://ollama:11434/api/generate"



llm = Ollama(
    base_url="http://ollama:11434",  # Nombre del servicio en docker-compose
    model="deepseek-r1:14b"
)

@app.post("/presentar")
async def presentar(pregunta: str, usar_contexto: bool = False):
    print(pregunta)
    print("---------------")
    print("soy el contexto")
    print(usar_contexto)

    if usar_contexto:
        vector_db = load_vector_db()
        context = vector_db.similarity_search(pregunta, k=3)
        prompt = f"""
        
        {context}

        Pregunta: {pregunta}
        """
        print("SOY  LA PREGUNTA CON CONTEXTO")
        print(prompt)
    else:
        prompt = f"""
        {pregunta}
        """
        print("SOY  LA PREGUNTA sin CONTEXTO")
        print(prompt)
    # 1. Buscar en RAG

    # vector_db = load_vector_db()
    # context = vector_db.similarity_search(nombre, k=3)
    
    # # 2. Consultar a Ollama
    # prompt = f"""
    # Genera una presentación profesional sobre {nombre} usando este contexto:
    # {context}
    # """
    # print("SOY EL CONTEXTOOOOO")
    # print(context)
    async with httpx.AsyncClient(timeout=httpx.Timeout(300.0)) as client:
        response = await client.post(
            OLLAMA_URL,
            json={"model": "deepseek-r1:14b", "prompt": prompt, "stream": False}
        )
    
    return {"presentacion": response.json()["response"]}
    #return {"presentacion": "holas"}


@app.post("/upload")
async def upload_persona(file: UploadFile = File(...)):
    # Guardar el archivo subido
    print("hola")
    file_path = f"/app/rag/data/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Reprocesar RAG
    process_documents()
    
    return {"status": f"Archivo {file.filename} procesado"}