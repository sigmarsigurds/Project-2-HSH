from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from buyer_model import BuyerModel
from container import Container
from buyer_repository import BuyerRepository

router = APIRouter()


@router.get("/buyers/{id}", status_code=200)  # get message with id
@inject
async def get_buyer(
    id: int,
    buyer_repository: BuyerRepository = Depends(
        Provide[Container.buyer_repository_provider]
    ),
):
    return buyer_repository.get_buyer(id)


@router.post("/buyers", status_code=201)  # save message and send message event
@inject
async def save_buyer(
    buyer: BuyerModel,
    buyer_repository: BuyerRepository = Depends(
        Provide[Container.buyer_repository_provider]
    ),
):

    return buyer_repository.save_buyer(
        buyer.name, buyer.ssn, buyer.email, buyer.phonenumber
    )

    # save message and send message event
