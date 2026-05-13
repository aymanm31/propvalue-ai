from fastapi import FastAPI

app = FastAPI(title="PropValue AI", version="0.1.0")

@app.get("/")
def root():
    return {"status": "PropValue AI backend is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}