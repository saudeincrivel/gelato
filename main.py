from api import app
from router import router

app.include_router(router, prefix="/api")  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=443)
