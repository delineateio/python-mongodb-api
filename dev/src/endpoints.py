from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide
from containers import Container
from models import Customer, Relationship
from data import (
    Repository,
)

router = APIRouter()


@router.get("/healthz", status_code=status.HTTP_200_OK, response_class=Response)
@inject
async def healthz(repository: Repository = Depends(Provide[Container.repository])):
    repository.provider.is_connected()


@router.delete(
    "/reset", status_code=status.HTTP_205_RESET_CONTENT, response_class=Response
)
@inject
async def reset(repository: Repository = Depends(Provide[Container.repository])):
    repository.provider.reset()


@router.get("/customers", status_code=status.HTTP_200_OK)
@inject
async def get_customers(
    repository: Repository = Depends(Provide[Container.repository]),
):
    return repository.provider.get_customers()


@router.post("/customer", status_code=status.HTTP_201_CREATED, response_class=Response)
@inject
async def create_customer(
    customer: Customer, repository: Repository = Depends(Provide[Container.repository])
):
    try:
        repository.provider.create_customer(jsonable_encoder(customer))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST) from err


@router.get("/customers/{handle}", status_code=status.HTTP_200_OK)
@inject
async def get_customer(
    handle: str, repository: Repository = Depends(Provide[Container.repository])
):
    return repository.provider.get_customer(handle)


@router.patch("/customers/{code}", status_code=status.HTTP_200_OK)
@inject
async def update_customer(
    handle: str, repository: Repository = Depends(Provide[Container.repository])
):
    customer = repository.provider.get_customer(handle)
    print(customer)
    # pylint: disable=fixme
    # TODO: update the customer document


@router.get("/customers/{handle}/relationships", status_code=status.HTTP_200_OK)
@inject
def get_relationships(
    handle: str, repository: Repository = Depends(Provide[Container.repository])
):
    customer = repository.provider.get_customer(handle)
    return customer.relationships


@router.post(
    "/customers/{code}/relationship",
    status_code=status.HTTP_201_CREATED,
    response_class=Response,
)
@inject
async def create_relationship(
    handle: str,
    relationship: Relationship,
    repository: Repository = Depends(Provide[Container.repository]),
):
    customer = repository.provider.get_customer(handle)
    customer.relationships.append(relationship)
    # pylint: disable=fixme
    # TODO: update the customer document
