from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from tor_config import generate_onion_service
import uvicorn
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = FastAPI()

# Defining the path for 'static' and 'templates' directories
static_path = os.path.join(os.path.dirname(__file__), 'static')
templates_path = os.path.join(os.path.dirname(__file__), 'templates')

# Defining the templates folder
templates = Jinja2Templates(directory=templates_path)

# Mounting the 'static' folder to serve static files
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_service(request: Request, port: str = Form(...)):
    # Generating the Onion service using the function defined in tor_config
    hostname = generate_onion_service(port)
    
    # Defining the message based on the result of generating the Onion service
    if hostname:
        message = f"Onion service created successfully: {hostname}"
    else:
        message = "Failed to create the Onion service. Please check the configurations."

    # Returning the response with the message to the page
    return templates.TemplateResponse("index.html", {"request": request, "message": message})

logging.info('Open: http://localhost:8000')

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
