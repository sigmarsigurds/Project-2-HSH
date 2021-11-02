from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.Models.merchant_model import MerchantModel
from src.Infrastructure.container import Container
from src.Repositories import MerchantRepository

router = APIRouter()


@router.get('/merchants/{merchant_id}', status_code=200)
@inject
async def get_merchants(
        merchant_id: int,
        merchant_repository: MerchantRepository = Depends(Provide[Container.merchant_repository_provider])):

    # TODO: Remove the data wrapper from the respond

    merchant = merchant_repository.get_merchant(merchant_id)

    if merchant is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"data": merchant}


@router.post('/merchants', status_code=201)
@inject
async def save_merchants(
        merchant: MerchantModel,
        merchant_repository: MerchantRepository = Depends(
            Provide[Container.merchant_repository_provider])):

    # TODO: Remove the data wrapper from the respond
    # TODO: Create method should only return id

    merchant = merchant_repository.save_merchant(merchant)

    return {"data": merchant}


# TODO: Crate enpoint merchants/{id}/allows_discount



