from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
from tor_config import generate_onion_service
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="src/onyconnect/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_service(request: Request, port: str = Form(...), directory: str = Form(...)):
    hostname = generate_onion_service(port, directory)
    if hostname:
        message = f"Serviço .onion criado com sucesso: {hostname}"
    else:
        message = "Falha ao criar o serviço .onion. Verifique as configurações."

    return templates.TemplateResponse("index.html", {"request": request, "message": message})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
