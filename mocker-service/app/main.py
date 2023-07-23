from fastapi import FastAPI


app = FastAPI()


@app.get("/", tags=["Test endpoint"])
def home():
    return "Placeholder"
