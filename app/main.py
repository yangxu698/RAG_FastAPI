#%%
from fastapi import FastAPI
from app.endpoints import router
from fastapi.middleware.cors import CORSMiddleware

origins = [
        "http://localhost:3000",  # Example: Frontend URL
        "http://127.0.0.1:8000",
        "*" # Allows all origins, not recommended for production
    ]

app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

app.include_router(router)