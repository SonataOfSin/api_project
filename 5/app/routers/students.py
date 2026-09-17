from fastapi import APIRouter

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

# ენდპოინტები დაემატება მოგვიანებით