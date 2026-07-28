from fastapi import routing

router = routing.APIRouter(
    "store",
    tags=["store"]
)