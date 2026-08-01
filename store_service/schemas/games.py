from pydantic import BaseModel

class RequiresAuth(BaseModel):
    csrf: str

class PurchaseGame(RequiresAuth):
    appid: int

class Price(BaseModel):
    price: float