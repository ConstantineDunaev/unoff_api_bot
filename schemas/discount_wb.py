from dataclasses import dataclass, astuple


@dataclass
class DiscountWB:
    nm_id: int
    vendor_code: str
    discount_on_site: int


@dataclass
class RowDiscountWB(DiscountWB):
    job_id: int

    def as_tuple(self):
        return astuple(self)
