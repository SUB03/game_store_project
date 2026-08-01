import grpc
from fastapi import HTTPException

from store_service.engine import engine
from store_service.models import games
import store_service.protobuf.payment.payment_service_pb2_grpc as ps_pb2_grpc
import store_service.protobuf.payment.payment_service_pb2 as ps_pb2
import store_service.protobuf.users.users_service_pb2_grpc as us_pb2_grpc
import store_service.protobuf.users.users_service_pb2 as us_pb2

async def make_payment(username: str, appid: int, price: str) -> ps_pb2.MakePaymentResponse:
    channel = grpc.aio.insecure_channel("payment_service:8002")
    stub = ps_pb2_grpc.PaymentServiceStub(channel)

    request = ps_pb2.MakePaymentRequest(
        username=username,
        appid=appid,
        price=price
    )

    try:
        response: ps_pb2.MakePaymentResponse = await stub.MakePayment(request)
    except grpc.aio.AioRpcError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Payment service error: {e.code()} - {e.details()}",
        )
    finally:
        await channel.close()

    return response

async def has_game(username: str, appid: int) -> us_pb2.HasGameResponse:
    channel = grpc.aio.insecure_channel("users_service:8003")
    stub = us_pb2_grpc.UserServiceStub(channel)

    request = us_pb2.HasGameRequest(
        username=username,
        appid=appid
    )

    try:
        response: us_pb2.HasGameResponse = await stub.HasGame(request)
    except grpc.aio.AioRpcError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Users service error: {e.code()} - {e.details()}",
        )
    finally:
        await channel.close()

    return response.result

async def get_price(appid: int):
    async with engine.begin() as conn:
        result = await conn.execute(games.select().where(games.c.appid==appid))
        result = result.fetchone()
    return result