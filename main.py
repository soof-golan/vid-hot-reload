from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "764345"}


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
