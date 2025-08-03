from enums import Scripts
from services.discount_wb import process_discount_wb


captions = {
    Scripts.discount_wb: 'Получение скидки WB'
}

functions = {
    Scripts.discount_wb: process_discount_wb
}


