from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat(user_id: str, message: str):
    # Aquí integrarás la lógica del modelo y el historial
    return {"response": "Respuesta generada por el modelo"}