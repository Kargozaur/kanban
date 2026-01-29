from pydantic import BaseModel, Field
from typing import Annotated


class Pagination(BaseModel):
    limit: Annotated[
        int,
        Field(
            default=10,
            ge=1,
            le=20,
            description="Limit for both database queries and the endpoints. \n "
            "Dependency for the endpoints is managed by PaginationDep.",
        ),
    ]
    offset: Annotated[
        int,
        Field(
            default=0,
            ge=0,
            description="Offset for both database queries and Endpoints. \n "
            "Dependency for the endpoints is managed by PaginationDep",
        ),
    ]
