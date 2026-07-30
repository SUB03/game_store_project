import grpc, asyncio
import payment_service_pb2
import payment_service_pb2_grpc

class PaymentServiceServicer(payment_service_pb2_grpc.PaymentServiceServicer):
    async def MakePayment(self, request: payment_service_pb2.PaymentRequest, context: grpc.aio.ServicerContext) -> payment_service_pb2.PaymentResponse:
        #TODO: mock payment service
        print(f"Processing payment for user: {request.user_id}, app: {request.appid}")
        await asyncio.sleep(0.1)

        return payment_service_pb2.PaymentResponse(
            user_id=request.user_id,
            status = payment_service_pb2.PaymentStatus.PAYMENT_STATUS_SUCCEEDED
        )


async def serve():
    server = grpc.aio.server()
    payment_service_pb2_grpc.add_PaymentServiceServicer_to_server(PaymentServiceServicer(), server)
    server.add_insecure_port('[::]:8002')

    await server.start()
    await server.wait_for_termination()
    await server.stop(grace=5)

if __name__ == "__main__":
    asyncio.run(serve())