from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "*",
    "http://s3-gelato-front-end.s3-website-sa-east-1.amazonaws.com/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
