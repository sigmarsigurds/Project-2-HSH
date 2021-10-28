from fastapi.exceptions import HTTPException
from APIModels.order_request_model import OrderRequestModel
from Validations.OrderValidator import OrderValidator
from Validations.MerchantExistsValidation import MerchantExistsValidation


def is_order_valid(order: OrderRequestModel):
    validator = OrderValidator()
    validator.add_validation(MerchantExistsValidation(merchant_id=order.merchant_id))
    try:
        return validator.validate()
    except Exception as e:
        # * Smá yikes
        raise HTTPException(status_code=400, detail=str(e))
