from fastapi import FastAPI
import uvicorn
from app.db.models import UserModel
from app.db.base import table_registry
from app.db.connection import engine
from app.routes import user_router,test_router

app = FastAPI()
app.include_router(user_router)
app.include_router(test_router)
@app.get('/')
def health_check():
    return "OK, it's working"

table_registry.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
