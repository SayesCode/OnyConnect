from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
import os
from tor_config import generate_onion_service
import uvicorn

app = FastAPI()

# Definindo o caminho para os diretórios 'static' e 'templates'
static_path = os.path.join(os.path.dirname(__file__), 'static')
templates_path = os.path.join(os.path.dirname(__file__), 'templates')

# Definindo a pasta de templates
templates = Jinja2Templates(directory=templates_path)

# Montando a pasta 'static' para servir arquivos estáticos
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_service(request: Request, port: str = Form(...), directory: str = Form(...)):
    # Gerando o serviço Onion usando a função definida em tor_config
    hostname = generate_onion_service(port, directory)
    
    # Definindo a mensagem com base no resultado da geração do serviço Onion
    if hostname:
        message = f"Serviço .onion criado com sucesso: {hostname}"
    else:
        message = "Falha ao criar o serviço .onion. Verifique as configurações."

    # Retornando a resposta com a mensagem para a página
    return templates.TemplateResponse("index.html", {"request": request, "message": message})

# Bloco para rodar o servidor Uvicorn diretamente
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
