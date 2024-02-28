from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession

import uvicorn
from fastapi import Depends, FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.routres import contacts, auth, users
from src.config.config import config


app = FastAPI()

origins = ["*"]     #   public; or origins = ["http://localhost:3000"] for some web on localhost:port

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  #     True for JWT tokens
    allow_methods=["*"],  #     [*] for all or ["GET, POST, PUT, DELETE"]
    allow_headers= ["*"]   #     [*] for all or ["Authorization"]
)

app.mount('/static', StaticFiles(directory='src/static'), name='static')

app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=config.REDIS_DOMAIN, port=config.REDIS_PORT, db=0, password=config.REDIS_PASSWORD)
    await FastAPILimiter.init(r)


@app.get('/')
def index():
    return {'message': "Contacts book"}

@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        reult = result.fetchone() 
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)