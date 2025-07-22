from fastapi import FastAPI
from app.db.models import UserModel
from app.db.base import table_registry
from app.db.connection import engine
from app.routes import router as router_rotes

app = FastAPI()
app.include_router(router_rotes)
@app.get('/')
def health_check():
    return "OK, it's working"

table_registry.metadata.create_all(bind=engine)
