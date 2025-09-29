from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class SupplyWB:
    supply_id: int
    supply_date: datetime
    fact_date: datetime

    def __post_init__(self):
        if isinstance(self.supply_date, str):
            self.supply_date = datetime.fromisoformat(self.supply_date).replace(tzinfo=None)
        if isinstance(self.fact_date, str):
            self.fact_date = datetime.fromisoformat(self.fact_date).replace(tzinfo=None)

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class SupplyDetailWB:
    barcode: str
    sa: str
    quantity: int
    unloading_quantity: int
    ready_for_sale_quantity: int
    income_quantity: int
    nm_id: int

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class RowSupplyDetailWB(SupplyWB, SupplyDetailWB):
    job_id: int

    def as_tuple(self):
        return (self.job_id,
                self.supply_id,
                self.supply_date,
                self.fact_date,
                self.barcode,
                self.sa,
                self.quantity,
                self.unloading_quantity,
                self.ready_for_sale_quantity,
                self.income_quantity,
                self.nm_id)
