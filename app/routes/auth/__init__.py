from fastapi import APIRouter
from app.controllers.auth.signup import signup

routes = APIRouter()

@routes.get("/test")
async def test() -> dict:
    return {"message": "test"}

routes.add_api_route('/signup', signup, methods=['POST'])