from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI
from app.api.chat import router as chat_router

app = FastAPI()

# Register all routes in the chat router.
app.include_router(chat_router)
