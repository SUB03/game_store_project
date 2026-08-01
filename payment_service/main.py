from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

import grpc, asyncio
import protobuf.payment.payment_service_pb2 as payment_service_pb2
import protobuf.payment.payment_service_pb2_grpc as payment_service_pb2_grpc

from async_yookassa import YooKassaClient
from async_yookassa.models.payment import PaymentRequest, Amount, RedirectConfirmationRequest

class Settings(BaseSettings):
    shopid: str
    ukass_api_key: str = Field(alias="UKASS_API_KEY")
    model_config = SettingsConfigDict(extra="ignore", env_file=".env")

class PaymentServiceServicer(payment_service_pb2_grpc.PaymentServiceServicer):
    def __init__(self, settings: Settings):
        self.settings = settings

    async def MakePayment(
            self,
            request: payment_service_pb2.MakePaymentRequest,
            context: grpc.aio.ServicerContext
    ) -> payment_service_pb2.MakePaymentResponse:
        
        async with YooKassaClient(
            account_id=self.settings.shopid,
            secret_key=self.settings.ukass_api_key
        ):
            yookassa_request = PaymentRequest(
                amount=Amount(value=request.price, currency="RUB")
            ) 
            

        return payment_service_pb2.MakePaymentResponse(
            user_id=request.user_id,
            status = payment_service_pb2.PaymentStatus.PAYMENT_STATUS_SUCCEEDED
        )


async def serve():
    settings = Settings()

    server = grpc.aio.server()
    payment_service_pb2_grpc.add_PaymentServiceServicer_to_server(PaymentServiceServicer(settings), server)
    server.add_insecure_port('[::]:8002')

    await server.start()
    await server.wait_for_termination()
    await server.stop(grace=5)

if __name__ == "__main__":
    asyncio.run(serve())