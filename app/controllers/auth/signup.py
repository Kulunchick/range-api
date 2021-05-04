from app.models.user import User
from fastapi import Request, BackgroundTasks, HTTPException
from fastapi.encoders import jsonable_encoder

async def signup(request: Request, user: User, tasks: BackgroundTasks):
    if (await request.app.mongodb.users.find_one({'email': user.email}, {'_id': 1})):
        raise HTTPException(status_code=409, detail='User already exists')
    tasks.add_task(request.app.mongodb.users.insert_one, user.dict())
    return user