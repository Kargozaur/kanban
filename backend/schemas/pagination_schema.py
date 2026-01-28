from pydantic import BaseModel, Field


class Pagination(BaseModel):
    limit: int = Field(
        default=10,
        ge=1,
        le=20,
        description="Limit for both database queries and Endpoints. Dependancy inside the endpoint manage by PaginationDep",
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Offset for both database queries and Endpoints. Dependancy inside the endpoint manage by PaginationDep ",
    )
