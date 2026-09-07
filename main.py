from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

API_KEY = "cloudwise123"


class Business(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=100)
    category: str = Field(min_length=2, max_length=50)
    location: str = Field(min_length=2, max_length=100)


businesses = [
    Business(id=1, name="Tech Solutions Ltd", category="Technology", location="Nairobi"),
    Business(id=2, name="Green Foods", category="Food", location="Mombasa"),
    Business(id=3, name="Creative Designs", category="Design", location="Kisumu"),
    Business(id=4, name="Digital Hub", category="Technology", location="Nakuru"),
    Business(id=5, name="Smart Finance", category="Finance", location="Nairobi"),
    Business(id=6, name="Coastal Traders", category="Retail", location="Mombasa"),
]


@app.get("/")
def get_business():
    return {"message": "The CloudWise Business API is running!"}


@app.get("/businesses")
def get_businesses(
    page: int = 1,
    limit: int = 2,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be at least 1")

    if limit < 1 or limit > 10:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 10")

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": len(businesses),
        "businesses": businesses[start:end]
    }