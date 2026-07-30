from fastapi import HTTPException, routing, Depends
import grpc

from store_service.engine import engine
from store_service.models.models import games

import store_service.protobuf.payment_service_pb2_grpc
import store_service.protobuf.payment_service_pb2

router = routing.APIRouter(
    prefix="/store",
    tags=["store"]
)

@router.get("/games")
async def get_games(page: int = 1, per_page: int = 10):
    if page < 1 or per_page < 1:
        raise HTTPException(status_code=400, detail="page and per_page must be >= 1")
    
    async with engine.begin() as conn:
        result = await conn.execute(games.select().order_by(games.c.recommendations.desc()).limit(per_page).offset((page - 1) * per_page))
        result = result.mappings().all()
    return result

@router.post("/purchase_game")
async def purchase_game(app_id: int):
    channel = grpc.aio.insecure_channel("localhost:8002")
    stub = store_service.protobuf.payment_service_pb2_grpc.PaymentServiceStub(channel)

    request = store_service.protobuf.payment_service_pb2.PaymentRequest(
        user_id="1",
        appid=str(app_id),
    )

    try:
        response: store_service.protobuf.payment_service_pb2.PaymentResponse = await stub.MakePayment(request)
    except grpc.aio.AioRpcError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Payment service error: {e.code()} - {e.details()}",
        )
    finally:
        await channel.close()

    return {
        "user_id": response.user_id,
        "status": response.status,
    }