from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException, status, Request
import httpx

router = APIRouter(prefix="/animals",
                   tags=["animals"],
                   responses={
                       status.HTTP_404_NOT_FOUND: {
                           "message": "No se encuentra la ruta"
                       }
                   })

router = APIRouter()
router.mount("/static", StaticFiles(directory="Frontend/static/templates"), name="static")

templates = Jinja2Templates(directory="Frontend/static/templates")

@router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/get-animals", response_class=HTMLResponse)
async def get_animals(request: Request):
    with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/animals/")

    return templates.TemplateResponse("home.html", {"request": request, "animals_list": response.json()})
    
