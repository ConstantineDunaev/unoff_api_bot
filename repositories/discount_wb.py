from mysql import Connection
from schemas.discount_wb import RowDiscountWB
from typing import List


class DiscountWBRepository:
    def __init__(self, connection: Connection):
        self.connection = connection

    async def write_rows(self, rows: List[RowDiscountWB]) -> None:
        query = ("INSERT INTO u_discount_wb (nm_id, vendor_code, discount_on_site, job_id) "
                 "VALUES (%s, %s, %s, %s)")
        values = [row.as_tuple() for row in rows]
        async with self.connection.cursor() as cursor:
            await cursor.executemany(query, values)

