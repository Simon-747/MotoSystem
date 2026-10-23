from pydantic import BaseModel, Field, computed_field


class BillPartInput(BaseModel):
    part_id: int
    quantity: int = Field(gt=0)


class BillPart(BaseModel):
    part_id: int
    quantity: int = Field(gt=0)
    unit_price: float = Field(ge=0)


class BillCreate(BaseModel):
    user_id: int
    maintenance_id: int
    date: str
    description: str
    parts: list[BillPartInput]
    labor_cost: float = Field(ge=0)


class BillBase(BaseModel):
    user_id: int
    maintenance_id: int
    date: str
    description: str
    parts: list[BillPart]
    labor_cost: float = Field(ge=0)

    @computed_field
    @property
    def parts_total(self) -> float:
        return sum(
            part.quantity * part.unit_price
            for part in self.parts
        )

    @computed_field
    @property
    def total(self) -> float:
        return self.parts_total + self.labor_cost


class Bill(BillBase):
    id: int


class BillUpdateInput(BaseModel):
    user_id: int | None = None
    maintenance_id: int | None = None
    date: str | None = None
    description: str | None = None
    parts: list[BillPartInput] | None = None
    labor_cost: float | None = Field(default=None, ge=0)


class BillUpdate(BaseModel):
    user_id: int | None = None
    maintenance_id: int | None = None
    date: str | None = None
    description: str | None = None
    parts: list[BillPart] | None = None
    labor_cost: float | None = Field(default=None, ge=0)
