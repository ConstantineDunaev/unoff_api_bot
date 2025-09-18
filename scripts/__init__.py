from enums import Scripts
from services.discount_wb import process_discount_wb
from services.supplies_wb import process_supplies_wb


captions = {
    Scripts.discount_wb: 'Получение скидки WB',
    Scripts.supplies_wb: 'Получение поставок WB'
}

functions = {
    Scripts.discount_wb: process_discount_wb,
    Scripts.supplies_wb: process_supplies_wb
}


