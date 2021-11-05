from pydantic import BaseModel, Field
from APIModels.credit_card_model import CreditCardModel


class OrderPaymentInformationModel(BaseModel):
    order_id: int = Field(..., alias="orderId")
    buyer_email: str = Field(..., alias="buyerEmail")
    merchant_email: str = Field(..., alias="merchantEmail")
    product_id: int = Field(..., alias="productId")
    merchant_id: int = Field(..., alias="merchantId")
    credit_card: CreditCardModel = Field(..., alias="creditCard")
    quantity: int = 1
