from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/events")
async def receive_event(request: Request):
    data = await request.json()  # Lê o corpo da requisição como JSON
    print("Evento recebido:", data)
    return {"success": True}

@app.post("/values")
async def receive_values(request: Request):
    data = await request.json()  # Lê o corpo da requisição como JSON
    print("Valores recebidos:", data)
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9001)
