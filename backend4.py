from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()

categories_data = [
    {"id": 1, "name": "Детские стрижки"},
    {"id": 2, "name": "Взрослые стрижки"},
    {"id": 3, "name": "Женские стрижки"},
    {"id": 4, "name": "И многое другое..."},
]

services_data = []


class ServiceCreate(BaseModel):
    categoryId: int = Field(..., description="ID категории")

    title: str = Field(..., min_length=1, max_length=100, description="Название услуги")

    desc: str = Field(..., min_length=1, max_length=100, description="Описание услуги")

    duration: int = Field(..., ge=30, le=180, description="Продолжительность в минутах")

    price: float = Field(..., gt=0, description="Стоимость услуги")


class ServiceResponse(ServiceCreate):
    id: int


@app.post("/services", response_model=ServiceResponse, status_code=201)
def create_service(service: ServiceCreate):
    category_exists = any(cat["id"] == service.categoryId for cat in categories_data)

    if not category_exists:
        raise HTTPException(status_code=404, detail="Category not found")

    new_service = {
        "id": len(services_data) + 1,
        "categoryId": service.categoryId,
        "title": service.title,
        "desc": service.desc,
        "duration": service.duration,
        "price": service.price
    }

    services_data.append(new_service)

    return new_service