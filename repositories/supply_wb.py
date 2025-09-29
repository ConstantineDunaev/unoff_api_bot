from mysql import Connection
from schemas.supply_wb import RowSupplyDetailWB
from typing import List


class SupplyWBRepository:
    def __init__(self, connection: Connection):
        self.connection = connection

    async def write_rows(self, rows: List[RowSupplyDetailWB]) -> None:
        query = ("""
        INSERT INTO u_supply_wb 
            (job_id, supply_id, supply_date, fact_date, barcode, sa, quantity,
             unloading_quantity, ready_for_sale_quantity, income_quantity, nm_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) as alias
        ON DUPLICATE KEY UPDATE
            job_id = alias.job_id,
            supply_date = alias.supply_date,
            fact_date = alias.fact_date,
            sa = alias.sa,
            quantity = alias.quantity,
            unloading_quantity = alias.unloading_quantity,
            ready_for_sale_quantity = alias.ready_for_sale_quantity,
            income_quantity = alias.income_quantity
        """)
        values = [row.as_tuple() for row in rows]
        async with self.connection.cursor() as cursor:
            await cursor.executemany(query, values)

    async def delete_old_rows(self, script_name: str, market_id: int):
        query = """
            DELETE uwb
            FROM u_supply_wb uwb
            JOIN (
                SELECT job_id
                FROM t_job
                WHERE market_id = %s
                  AND script = %s
                ORDER BY job_id DESC
                LIMIT 10000 OFFSET 1
            ) t ON uwb.job_id = t.job_id
        """
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, (market_id, script_name))
