from fastapi import APIRouter

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

# ენდპოინტები დაემატება მოგვიანებით